"""Lancement d'un run et notation de ses traces.

Les deux etapes sont separees. Un run produit traces.jsonl, ce que le
modele a fait. La notation relit les traces, reexecute chaque requete finale
et la compare a la reference, puis ecrit notes.jsonl. On peut donc corriger
le comparateur ou une reference et renoter un run sans rappeler le modele.

Issue d'une question, selon sa categorie :

  repondable      juste | faux_silencieux | erreur_execution
                  | abstention_a_tort | incident
  ambigue         signalee | non_signalee | incident
                  (plus : la reponse correspond-elle a une interpretation ?)
  hors_perimetre  abstention_juste | hallucination | incident

faux_silencieux est la categorie qui compte le plus : la requete s'execute,
l'utilisateur recoit un chiffre, et le chiffre est faux. Rien ne l'en
avertit.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import threading
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from pathlib import Path

from . import agent, arbitrages, comparaison, garde, jeu, prompt
from .db import DSN, Base, ErreurSQL, Resultat
from .llm import Fournisseur

RACINE_RUNS = jeu.RACINE / "runs"


# ---------------------------------------------------------------------------
# lancement
# ---------------------------------------------------------------------------

def _nom_run(fournisseur: Fournisseur, variante: str, mode: str) -> str:
    horodatage = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    modele = fournisseur.modele.replace("/", "-")
    return f"{horodatage}_{modele}_{variante}_{mode}"


def _deja_faits(chemin: Path) -> set[tuple[str, int]]:
    if not chemin.exists():
        return set()
    faits = set()
    for ligne in chemin.read_text(encoding="utf-8").splitlines():
        if ligne.strip():
            t = json.loads(ligne)
            faits.add((t["id"], t["repetition"]))
    return faits


def lancer(questions: list[jeu.Question], fournisseur: Fournisseur, variante: str,
           mode: str, repetitions: int = 1, paralleles: int = 4,
           dossier: Path | None = None, dsn: str = DSN, journal=print) -> Path:
    """Fait tourner l'agent sur les questions. Reprend un run interrompu si
    dossier pointe vers un run existant."""
    base = Base(dsn)
    systeme = prompt.construire(base, variante, mode)
    base.fermer()

    dossier = dossier or RACINE_RUNS / _nom_run(fournisseur, variante, mode)
    dossier.mkdir(parents=True, exist_ok=True)
    (dossier / "prompt.txt").write_text(systeme, encoding="utf-8")
    config = {
        "fournisseur": fournisseur.nom,
        "modele": fournisseur.modele,
        "effort": getattr(fournisseur, "effort", None),
        "variante": variante,
        "mode": mode,
        "repetitions": repetitions,
        "questions": [q.id for q in questions],
        "jeu_empreinte": jeu.empreinte(),
        "prompt_empreinte": hashlib.sha256(systeme.encode()).hexdigest()[:12],
        "debut": dt.datetime.now().isoformat(timespec="seconds"),
    }
    if fournisseur.nom == "rejeu":
        config["rejeu"] = {
            "lignes_invalides": len(fournisseur.lignes_invalides),
            "normalisations": dict(Counter(fournisseur.normalisations)),
        }
    precedente = dossier / "config.json"
    if precedente.exists():
        # Reprise : les traces deja ecrites doivent venir de la meme
        # configuration, sinon le run melangerait deux experiences.
        ancienne = json.loads(precedente.read_text(encoding="utf-8"))
        for cle in ("modele", "variante", "mode", "prompt_empreinte", "jeu_empreinte"):
            if ancienne.get(cle) != config[cle]:
                raise ValueError(f"reprise refusee : {cle} a change "
                                 f"({ancienne.get(cle)} -> {config[cle]})")
        config["debut"] = ancienne["debut"]
    (dossier / "config.json").write_text(
        json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")

    fichier = dossier / "traces.jsonl"
    faits = _deja_faits(fichier)
    a_faire = [(q, r) for q in questions for r in range(repetitions)
               if (q.id, r) not in faits]
    journal(f"{len(a_faire)} executions a faire, {len(faits)} deja faites -> {dossier}")
    invalides = getattr(fournisseur, "lignes_invalides", [])
    if invalides:
        journal(f"  attention : {len(invalides)} ligne(s) illisible(s) dans le fichier rejoue")
    normalisations = getattr(fournisseur, "normalisations", [])
    if normalisations:
        journal(f"  {len(normalisations)} statut(s) hors schema normalise(s)")

    verrou = threading.Lock()
    local = threading.local()

    def executer(q: jeu.Question, r: int) -> agent.Trace:
        if not hasattr(local, "base"):
            local.base = Base(dsn)
        return agent.repondre(q.question, fournisseur, local.base, systeme, mode,
                              identifiant=q.id, repetition=r)

    with ThreadPoolExecutor(max_workers=paralleles) as pool:
        futurs = {pool.submit(executer, q, r): (q, r) for q, r in a_faire}
        for n, futur in enumerate(as_completed(futurs), start=1):
            trace = futur.result()
            with verrou, open(fichier, "a", encoding="utf-8") as f:
                f.write(agent.resume_json(trace) + "\n")
            statut = trace.incident or (trace.final or {}).get("statut", "?")
            journal(f"  [{n:>3}/{len(a_faire)}] {trace.id:<28} {statut}")
    return dossier


# ---------------------------------------------------------------------------
# notation
# ---------------------------------------------------------------------------

@dataclass
class Note:
    id: str
    repetition: int
    categorie: str
    split: str
    pieges: list[str]
    issue: str
    diagnostic: str = ""
    detail: str = ""
    statut: str | None = None
    signalee: bool = False
    acceptable: bool | None = None       # questions ambigues seulement
    interpretation: str = ""             # celle qui correspond, le cas echeant
    sql: str = ""
    n_requetes: int = 0
    n_erreurs_intermediaires: int = 0
    usage: dict | None = None
    duree_s: float = 0.0
    issue_auto: str = ""                 # verdict du comparateur, avant arbitrage
    arbitrage: str = ""                  # raison, si un humain a corrige le verdict


class Noteur:
    """Execute references et requetes obtenues, avec un cache des references."""

    def __init__(self, base: Base, arbitrages: dict | None = None):
        self.base = base
        self.arbitrages = arbitrages or {}
        self._references: dict[str, Resultat] = {}

    def reference(self, sql: str) -> Resultat:
        if sql not in self._references:
            self._references[sql] = self.base.executer(sql)
        return self._references[sql]

    def executer_obtenu(self, sql: str) -> tuple[Resultat | None, str]:
        """Resultat de la requete de l'agent, ou None et le diagnostic d'erreur."""
        try:
            return self.base.executer(garde.verifier(sql)), ""
        except garde.RequeteRefusee as e:
            return None, f"garde: {e}"
        except ErreurSQL as e:
            return None, f"{e.sqlstate or '?'}: {e.message}"

    def correspondances(self, q: jeu.Question,
                        obtenu: Resultat) -> list[tuple[jeu.Reference, comparaison.Verdict]]:
        sortie = []
        for ref in q.references:
            v = comparaison.comparer(self.reference(ref.sql), obtenu, ref.forme,
                                     ref.cles, ref.echelle_pourcentage)
            sortie.append((ref, v))
        return sortie

    def noter(self, q: jeu.Question, t: agent.Trace) -> Note:
        final = t.final or {}
        statut = final.get("statut")
        sql = (final.get("sql") or "").strip()
        note = Note(
            id=q.id, repetition=t.repetition, categorie=q.categorie, split=q.split,
            pieges=list(q.pieges), issue="", statut=statut, sql=sql,
            signalee=statut == "clarification" or bool(final.get("ambiguite")),
            n_requetes=len(t.etapes),
            n_erreurs_intermediaires=sum(1 for e in t.etapes if e.erreur),
            usage=asdict(t.usage), duree_s=t.duree_s,
        )

        if t.final is None:
            note.issue, note.diagnostic = "incident", t.incident or "pas_de_reponse"
            return note

        if q.hors_perimetre:
            note.issue = "hallucination" if statut == "reponse" else "abstention_juste"
            return note

        obtenu, erreur = (None, "pas de requete")
        if statut == "reponse" and sql:
            obtenu, erreur = self.executer_obtenu(sql)

        if q.ambigue:
            note.issue = "signalee" if note.signalee else "non_signalee"
            if obtenu is not None and q.references:
                justes = [ref for ref, v in self.correspondances(q, obtenu) if v.juste]
                note.acceptable = bool(justes)
                note.interpretation = justes[0].nom if justes else ""
            elif statut == "reponse" and q.references:
                note.acceptable = False
                note.diagnostic = erreur
            return note

        # Question repondable.
        if statut != "reponse" or not sql:
            note.issue, note.diagnostic = "abstention_a_tort", statut or ""
            return note
        if obtenu is None:
            note.issue, note.diagnostic = "erreur_execution", erreur
            return note
        (ref, verdict), = self.correspondances(q, obtenu)
        note.issue = "juste" if verdict.juste else "faux_silencieux"
        note.diagnostic = verdict.diagnostic
        if not verdict.juste:
            attendu = self.reference(ref.sql)
            note.detail = (f"{verdict.detail} | attendu {attendu.colonnes} "
                           f"{attendu.apercu(3)} | obtenu {obtenu.colonnes} {obtenu.apercu(3)}")
        note.issue_auto = note.issue
        a = self.arbitrages.get((q.id, arbitrages.empreinte_sql(sql)))
        if a is not None:
            note.issue = "juste" if a.verdict == "juste" else "faux_silencieux"
            note.arbitrage = a.raison
        return note


def lire_traces(dossier: Path) -> list[agent.Trace]:
    lignes = (dossier / "traces.jsonl").read_text(encoding="utf-8").splitlines()
    return [agent.Trace.depuis_dict(json.loads(l)) for l in lignes if l.strip()]


def noter_run(dossier: Path, questions: list[jeu.Question] | None = None,
              dsn: str = DSN) -> list[Note]:
    questions = {q.id: q for q in (questions or jeu.charger())}
    base = Base(dsn)
    noteur = Noteur(base, arbitrages.charger(ids_valides=set(jeu.charger_ids())))
    notes = []
    try:
        for t in sorted(lire_traces(dossier), key=lambda t: (t.id, t.repetition)):
            if t.id not in questions:
                continue  # question retiree du jeu depuis le run
            notes.append(noteur.noter(questions[t.id], t))
    finally:
        base.fermer()
    with open(dossier / "notes.jsonl", "w", encoding="utf-8") as f:
        for n in notes:
            f.write(json.dumps(asdict(n), ensure_ascii=False) + "\n")
    return notes


def lire_notes(dossier: Path) -> list[Note]:
    lignes = (dossier / "notes.jsonl").read_text(encoding="utf-8").splitlines()
    return [Note(**json.loads(l)) for l in lignes if l.strip()]
