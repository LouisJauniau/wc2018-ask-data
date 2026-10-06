"""La boucle de l'agent : question -> (requetes exploratoires) -> reponse.

L'agent ne renvoie pas un resultat, il renvoie une trace : chaque requete
essayee, chaque erreur, la reponse finale, les jetons et la duree. La
notation se fait ensuite a partir de la trace, en reexecutant la requete
finale : on ne croit pas l'agent sur parole quant a ce que sa requete
renvoie.
"""

from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field

from . import garde
from .db import Base, ErreurSQL
from .llm import Fournisseur, ResultatOutil, Usage
from .prompt import outils

LIGNES_MONTREES = 20
MAX_TOURS = 8
ERREURS_FATALES = ("AuthenticationError", "PermissionDeniedError", "NotFoundError")


def est_fatale(e: Exception) -> bool:
    """Erreur qui toucherait toutes les questions de la meme facon : cle
    refusee ou absente, modele inconnu. Elle doit arreter le run, pas le
    remplir d'incidents. Sans aucune cle, le SDK Anthropic leve un TypeError
    au premier appel, reconnaissable a son message."""
    return (type(e).__name__ in ERREURS_FATALES
            or (isinstance(e, TypeError) and "authentication method" in str(e)))


@dataclass
class Etape:
    sql: str
    erreur: str | None = None
    n_lignes: int | None = None


@dataclass
class Trace:
    id: str
    repetition: int
    question: str
    mode: str
    final: dict | None = None
    etapes: list[Etape] = field(default_factory=list)
    tours: int = 0
    usage: Usage = field(default_factory=Usage)
    duree_s: float = 0.0
    incident: str | None = None

    def vers_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def depuis_dict(cls, d: dict) -> "Trace":
        d = dict(d)
        d["etapes"] = [Etape(**e) for e in d.get("etapes", [])]
        d["usage"] = Usage(**d.get("usage", {}))
        return cls(**d)


def _formater(colonnes, lignes, total, tronque) -> str:
    """Resultat d'une requete tel que le modele le lit : compact et borne."""
    entete = " | ".join(colonnes)
    corps = "\n".join(" | ".join("NULL" if v is None else str(v) for v in l)
                      for l in lignes[:LIGNES_MONTREES])
    reste = total - min(total, LIGNES_MONTREES)
    fin = f"\n... {reste} lignes de plus" if reste else ""
    if tronque:
        fin += " (resultat tronque cote serveur)"
    return f"{total} ligne(s)\n{entete}\n{corps}{fin}"


def _executer_outil_sql(appel_id: str, arguments: dict, base: Base,
                        etapes: list[Etape]) -> ResultatOutil:
    sql = arguments.get("sql", "")
    etape = Etape(sql=sql)
    etapes.append(etape)
    try:
        propre = garde.verifier(sql)
        r = base.executer(propre)
    except garde.RequeteRefusee as e:
        etape.erreur = f"garde: {e}"
        return ResultatOutil(appel_id, f"Requete refusee : {e}", erreur=True)
    except ErreurSQL as e:
        etape.erreur = f"{e.sqlstate}: {e.message}"
        return ResultatOutil(appel_id, f"Erreur PostgreSQL ({e.sqlstate}) : {e.message}",
                             erreur=True)
    etape.n_lignes = len(r.lignes)
    return ResultatOutil(appel_id, _formater(r.colonnes, r.lignes, len(r.lignes), r.tronque))


def repondre(question: str, fournisseur: Fournisseur, base: Base | None, systeme: str,
             mode: str = "agent", identifiant: str = "", repetition: int = 0,
             max_tours: int = MAX_TOURS) -> Trace:
    trace = Trace(id=identifiant, repetition=repetition, question=question, mode=mode)
    debut = time.monotonic()
    try:
        session = fournisseur.ouvrir(systeme, outils(mode), identifiant)
        tour = session.envoyer(question)
        relance = False
        while True:
            trace.tours += 1
            trace.usage = trace.usage + tour.usage
            if tour.arret in ("refus", "max_tokens"):
                trace.incident = f"arret_{tour.arret}"
                break
            if not tour.appels:
                # Le modele a repondu en texte libre. Une seule relance.
                if relance:
                    trace.incident = "pas_de_reponse"
                    break
                relance = True
                tour = session.envoyer("Donne ta réponse en appelant l'outil repondre.")
                continue

            resultats = []
            for appel in tour.appels:
                if appel.nom == "repondre":
                    trace.final = appel.arguments
                    r = ResultatOutil(appel.id, "ok")
                elif appel.nom == "executer_sql" and mode == "agent":
                    r = _executer_outil_sql(appel.id, appel.arguments, base, trace.etapes)
                else:
                    r = ResultatOutil(appel.id, f"outil inconnu : {appel.nom}", erreur=True)
                resultats.append(r)
            if trace.final is not None:
                break
            if trace.tours >= max_tours:
                trace.incident = "max_tours"
                break
            if trace.tours == max_tours - 1:
                resultats[-1].contenu += "\n\nDernier tour : appelle maintenant l'outil repondre."
            tour = session.renvoyer(resultats)
    except Exception as e:
        # Une question qui plante ne doit pas arreter le run, sauf si toutes
        # planteront de la meme facon : cle refusee, modele inconnu.
        if est_fatale(e):
            raise
        trace.incident = f"exception: {type(e).__name__}: {e}"[:500]
    trace.duree_s = round(time.monotonic() - debut, 2)
    return trace


def resume_json(trace: Trace) -> str:
    return json.dumps(trace.vers_dict(), ensure_ascii=False)
