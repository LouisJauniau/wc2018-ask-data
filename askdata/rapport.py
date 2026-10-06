"""Agregation des notes d'un ou plusieurs runs en rapport Markdown.

Chaque taux est donne avec son effectif et un intervalle de Wilson a 95 %.
Sur une cinquantaine de questions, un point de pourcentage ne veut rien
dire ; l'intervalle evite de lire un ecart de 4 points comme un progres.
"""

from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from pathlib import Path

from .evaluation import Note, lire_notes
from .llm import Usage, cout


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (math.nan, math.nan)
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    demi = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, centre - demi), min(1.0, centre + demi))


def taux(k: int, n: int, ic: bool = True) -> str:
    if n == 0:
        return "n/a"
    texte = f"{k}/{n} ({100 * k / n:.0f} %)"
    if ic:
        bas, haut = wilson(k, n)
        texte += f" [{100 * bas:.0f}-{100 * haut:.0f}]"
    return texte


def mesures(notes: list[Note]) -> dict:
    """Les chiffres de synthese d'un run, en effectifs."""
    rep = [n for n in notes if n.categorie not in ("ambigue", "hors_perimetre")]
    amb = [n for n in notes if n.categorie == "ambigue"]
    hp = [n for n in notes if n.categorie == "hors_perimetre"]
    issues = Counter(n.issue for n in rep)
    avec_erreur = [n for n in rep if n.n_erreurs_intermediaires > 0]
    amb_avec_sql = [n for n in amb if n.acceptable is not None]
    usage = Usage()
    for n in notes:
        usage = usage + Usage(**(n.usage or {}))
    return {
        "n_rep": len(rep),
        "juste": issues["juste"],
        "juste_auto": sum((n.issue_auto or n.issue) == "juste" for n in rep),
        "arbitrees": sum(bool(n.arbitrage) for n in rep),
        "faux_silencieux": issues["faux_silencieux"],
        "erreur_execution": issues["erreur_execution"],
        "abstention_a_tort": issues["abstention_a_tort"],
        "incident": issues["incident"] + sum(n.issue == "incident" for n in amb + hp),
        "faux_signalement": sum(n.signalee for n in rep),
        "n_amb": len(amb),
        "amb_signalee": sum(n.issue == "signalee" for n in amb),
        "n_amb_sql": len(amb_avec_sql),
        "amb_acceptable": sum(bool(n.acceptable) for n in amb_avec_sql),
        "n_hp": len(hp),
        "hp_abstention": sum(n.issue == "abstention_juste" for n in hp),
        "hp_hallucination": sum(n.issue == "hallucination" for n in hp),
        "n_avec_erreur": len(avec_erreur),
        "rattrapees": sum(n.issue == "juste" for n in avec_erreur),
        "requetes_moy": (sum(n.n_requetes for n in notes) / len(notes)) if notes else 0,
        "duree_moy": (sum(n.duree_s for n in notes) / len(notes)) if notes else 0,
        "usage": usage,
    }


def _tableau(entetes: list[str], lignes: list[list]) -> str:
    sortie = ["| " + " | ".join(entetes) + " |",
              "|" + "|".join("---" for _ in entetes) + "|"]
    sortie += ["| " + " | ".join(str(c) for c in l) + " |" for l in lignes]
    return "\n".join(sortie)


def _cellule_code(texte: str, longueur: int = 160) -> str:
    texte = " ".join(texte.split())
    if len(texte) > longueur:
        texte = texte[: longueur - 3] + "..."
    return texte.replace("|", "\\|")


def rapport_run(dossier: Path) -> str:
    config = json.loads((dossier / "config.json").read_text(encoding="utf-8"))
    notes = lire_notes(dossier)
    m = mesures(notes)
    c = cout(config["modele"], m["usage"])
    u = m["usage"]

    s = [f"# Run {dossier.name}", ""]
    s.append(_tableau(["Paramètre", "Valeur"], [
        ["fournisseur / modèle", f"{config['fournisseur']} / {config['modele']}"],
        ["variante du prompt", config["variante"]],
        ["mode", config["mode"]],
        ["répétitions", config["repetitions"]],
        ["jeu / prompt", f"{config['jeu_empreinte']} / {config['prompt_empreinte']}"],
        ["date", config["debut"]],
    ]))
    if "rejeu" in config:
        r = config["rejeu"]
        corrections = ", ".join(f"{k} ({v})" for k, v in r["normalisations"].items()) or "aucune"
        s += ["", f"Réponses rejouées depuis un fichier. Lignes illisibles : "
              f"{r['lignes_invalides']}. Corrections de format : {corrections}."]
    s += ["", "## Synthèse", ""]
    s.append(_tableau(["Mesure", "Effectif (IC 95 %)"], [
        ["**Exactitude**, questions répondables", taux(m["juste"], m["n_rep"])],
        *([["Exactitude du comparateur seul, avant arbitrage humain",
            taux(m["juste_auto"], m["n_rep"])]] if m["arbitrees"] else []),
        ["**Faux silencieux** : s'exécute, renvoie un faux résultat",
         taux(m["faux_silencieux"], m["n_rep"])],
        ["Part de faux parmi les réponses qui s'exécutent",
         taux(m["faux_silencieux"], m["juste"] + m["faux_silencieux"])],
        ["Erreurs d'exécution (requête finale)", taux(m["erreur_execution"], m["n_rep"])],
        ["Abstentions à tort", taux(m["abstention_a_tort"], m["n_rep"])],
        ["Ambiguïtés signalées", taux(m["amb_signalee"], m["n_amb"])],
        ["Réponse conforme à une interprétation (ambiguës)",
         taux(m["amb_acceptable"], m["n_amb_sql"])],
        ["Faux signalements : question claire jugée ambiguë",
         taux(m["faux_signalement"], m["n_rep"])],
        ["Hors périmètre : abstention juste", taux(m["hp_abstention"], m["n_hp"])],
        ["Hors périmètre : réponse inventée", taux(m["hp_hallucination"], m["n_hp"])],
        ["Incidents (pas de réponse, refus, exception)", m["incident"]],
    ]))
    if config["mode"] == "agent":
        s += ["", f"Requêtes par question : {m['requetes_moy']:.1f}. "
              f"Questions répondables passées par une erreur : {m['n_avec_erreur']}, "
              f"dont {m['rattrapees']} finies justes."]
    s += ["", f"Jetons : {u.entree} en entrée, {u.cache_lecture} lus en cache, "
          f"{u.sortie} en sortie, {u.appels} appels. "
          + (f"Coût estimé : {c:.3f} $. " if c is not None else "")
          + f"Durée moyenne par question : {m['duree_moy']:.1f} s."]

    # Par split : le split test n'a pas servi a regler le prompt.
    s += ["", "## Par split", ""]
    lignes = []
    for split in ("dev", "test"):
        ms = mesures([n for n in notes if n.split == split])
        lignes.append([split, taux(ms["juste"], ms["n_rep"]),
                       taux(ms["faux_silencieux"], ms["n_rep"], ic=False),
                       taux(ms["amb_signalee"], ms["n_amb"], ic=False),
                       taux(ms["hp_abstention"], ms["n_hp"], ic=False)])
    s.append(_tableau(["Split", "Exactitude", "Faux silencieux", "Ambiguïtés signalées",
                       "Hors périmètre refusé"], lignes))

    rep = [n for n in notes if n.categorie not in ("ambigue", "hors_perimetre")]
    s += ["", "## Par catégorie", ""]
    par_cat = defaultdict(list)
    for n in rep:
        par_cat[n.categorie].append(n)
    s.append(_tableau(["Catégorie", "Justes", "Faux silencieux", "Erreurs"], [
        [cat, taux(sum(n.issue == "juste" for n in ns), len(ns), ic=False),
         sum(n.issue == "faux_silencieux" for n in ns),
         sum(n.issue == "erreur_execution" for n in ns)]
        for cat, ns in sorted(par_cat.items())]))

    s += ["", "## Par piège", "",
          "Taux d'échec des questions répondables qui portent le piège. Une question "
          "porte souvent plusieurs pièges : ces lignes ne s'additionnent pas.", ""]
    par_piege = defaultdict(list)
    for n in rep:
        for p in n.pieges:
            par_piege[p].append(n)
    echecs = {p: sum(n.issue != "juste" for n in ns) for p, ns in par_piege.items()}
    # Taux d'echec decroissant ; a taux egal, le piege le plus frequent d'abord.
    ordre = sorted(par_piege, key=lambda p: (-echecs[p] / len(par_piege[p]), -len(par_piege[p])))
    s.append(_tableau(["Piège", "Questions", "Échecs"], [
        [p, len(par_piege[p]), taux(echecs[p], len(par_piege[p]), ic=False)] for p in ordre]))

    fs = Counter(n.diagnostic for n in rep if n.issue == "faux_silencieux")
    if fs:
        s += ["", "## Forme des faux silencieux", ""]
        s.append(_tableau(["Diagnostic", "Nombre"], fs.most_common()))

    arbitrees = [n for n in notes if n.arbitrage]
    if arbitrees:
        s += ["", "## Verdicts corrigés à la main", "",
              "Voir evals/arbitrages.toml. Le verdict du comparateur est donné entre "
              "parenthèses.", ""]
        for n in arbitrees:
            s.append(f"### {n.id} : {n.issue} (comparateur : {n.issue_auto}, {n.diagnostic})")
            s.append(f"\n{n.arbitrage}\n\n```sql\n{n.sql}\n```\n")

    echecs = [n for n in notes if n.issue not in ("juste", "signalee", "abstention_juste")]
    if echecs:
        s += ["", "## Détail des échecs", ""]
        for n in echecs:
            s.append(f"### {n.id} (rép. {n.repetition}) : {n.issue}"
                     + (f", {n.diagnostic}" if n.diagnostic else ""))
            if n.detail:
                s.append(f"\n{_cellule_code(n.detail, 600)}")
            if n.sql:
                s.append(f"\n```sql\n{n.sql}\n```")
            s.append("")
    return "\n".join(s) + "\n"


SYMBOLES = {
    "juste": "ok", "faux_silencieux": "FAUX", "erreur_execution": "err",
    "abstention_a_tort": "abst", "incident": "inc", "signalee": "sig",
    "non_signalee": "-", "abstention_juste": "ok", "hallucination": "HALL",
}


def rapport_comparatif(dossiers: list[Path]) -> str:
    runs = []
    for d in dossiers:
        config = json.loads((d / "config.json").read_text(encoding="utf-8"))
        runs.append((d, config, lire_notes(d)))

    s = ["# Comparaison de runs", ""]
    lignes = []
    for d, config, notes in runs:
        m = mesures(notes)
        c = cout(config["modele"], m["usage"])
        lignes.append([
            f"`{d.name}` ({config['modele']}, {config['variante']}, {config['mode']})",
            taux(m["juste"], m["n_rep"]),
            taux(m["faux_silencieux"], m["n_rep"], ic=False),
            taux(m["erreur_execution"], m["n_rep"], ic=False),
            taux(m["amb_signalee"], m["n_amb"], ic=False),
            taux(m["faux_signalement"], m["n_rep"], ic=False),
            taux(m["hp_abstention"], m["n_hp"], ic=False),
            f"{c:.2f} $" if c is not None else "n/a",
        ])
    s.append(_tableau(["Run", "Exactitude", "Faux silencieux", "Erreurs",
                       "Ambiguïtés signalées", "Faux signalements",
                       "Hors périmètre refusé", "Coût"], lignes))

    s += ["", "## Question par question", "",
          "ok juste, FAUX faux silencieux, err erreur d'exécution, abst abstention à "
          "tort, sig ambiguïté signalée, - ambiguïté non signalée, HALL réponse "
          "inventée hors périmètre. Plusieurs répétitions : une issue par répétition.", ""]
    ids = sorted({n.id for _, _, notes in runs for n in notes})
    categories = {n.id: n.categorie for _, _, notes in runs for n in notes}
    entetes = ["Question", "Cat."] + [d.name for d, _, _ in runs]
    lignes = []
    for qid in ids:
        ligne = [qid, categories[qid][:5]]
        for _, _, notes in runs:
            issues = [SYMBOLES.get(n.issue, n.issue) for n in notes if n.id == qid]
            ligne.append(" ".join(issues) or "")
        lignes.append(ligne)
    s.append(_tableau(entetes, lignes))
    return "\n".join(s) + "\n"
