"""Chargement et validation du jeu de questions (evals/questions.toml)."""

from __future__ import annotations

import hashlib
import tomllib
from dataclasses import dataclass
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
FICHIER_QUESTIONS = RACINE / "evals" / "questions.toml"

CATEGORIES_REPONDABLES = ("comptage", "classement", "ratio", "liste")
CATEGORIES = CATEGORIES_REPONDABLES + ("ambigue", "hors_perimetre")
FORMES = ("ensemble", "ordonne", "premier")
SPLITS = ("dev", "test")


@dataclass(frozen=True)
class Reference:
    """Une requete de reference et la maniere de lui comparer un resultat."""

    sql: str
    forme: str = "ensemble"
    cles: tuple[tuple[str, ...], ...] | None = None  # None : toutes les colonnes
    echelle_pourcentage: bool = False
    nom: str = ""


@dataclass(frozen=True)
class Question:
    id: str
    question: str
    categorie: str
    split: str
    pieges: tuple[str, ...]
    references: tuple[Reference, ...] = ()
    sql_verif: str | None = None
    ambiguite: str | None = None

    @property
    def repondable(self) -> bool:
        return self.categorie in CATEGORIES_REPONDABLES

    @property
    def ambigue(self) -> bool:
        return self.categorie == "ambigue"

    @property
    def hors_perimetre(self) -> bool:
        return self.categorie == "hors_perimetre"

    @property
    def id_opaque(self) -> str:
        return id_opaque(self.id)


def id_opaque(identifiant: str) -> str:
    """Identifiant montre a un modele evalue hors harnais : "cartons_jaunes"
    en dirait trop sur la question."""
    return "q" + hashlib.sha256(identifiant.encode()).hexdigest()[:6]


def _cles(brut) -> tuple[tuple[str, ...], ...] | None:
    if brut is None:
        return None
    if all(isinstance(c, str) for c in brut):
        return (tuple(brut),)
    return tuple(tuple(alt) for alt in brut)


def _reference(brut: dict, defaut_echelle: bool = False) -> Reference:
    return Reference(
        sql=brut["sql"].strip(),
        forme=brut.get("forme", "ensemble"),
        cles=_cles(brut.get("cles")),
        echelle_pourcentage=brut.get("echelle_pourcentage", defaut_echelle),
        nom=brut.get("nom", ""),
    )


class JeuInvalide(ValueError):
    pass


def _valider(q: Question) -> None:
    def erreur(msg):
        raise JeuInvalide(f"{q.id} : {msg}")

    if q.categorie not in CATEGORIES:
        erreur(f"categorie inconnue {q.categorie!r}")
    if q.split not in SPLITS:
        erreur(f"split inconnu {q.split!r}")
    for r in q.references:
        if r.forme not in FORMES:
            erreur(f"forme inconnue {r.forme!r}")
    if q.repondable and len(q.references) != 1:
        erreur("une question repondable porte exactement une reference")
    if q.ambigue and not q.ambiguite:
        erreur("une question ambigue doit dire en quoi elle l'est")
    if q.hors_perimetre and q.references:
        erreur("une question hors perimetre n'a pas de reference")


def charger(chemin: Path = FICHIER_QUESTIONS) -> list[Question]:
    with open(chemin, "rb") as f:
        brut = tomllib.load(f)

    questions = []
    for b in brut["question"]:
        if "sql" in b:
            references = (_reference(b),)
        else:
            references = tuple(_reference(i) for i in b.get("interpretations", []))
        q = Question(
            id=b["id"],
            question=b["question"],
            categorie=b["categorie"],
            split=b["split"],
            pieges=tuple(b.get("pieges", [])),
            references=references,
            sql_verif=b.get("sql_verif", "").strip() or None,
            ambiguite=b.get("ambiguite"),
        )
        _valider(q)
        questions.append(q)

    ids = [q.id for q in questions]
    doublons = {i for i in ids if ids.count(i) > 1}
    if doublons:
        raise JeuInvalide(f"identifiants en double : {sorted(doublons)}")
    return questions


def charger_ids(chemin: Path = FICHIER_QUESTIONS) -> list[str]:
    return [q.id for q in charger(chemin)]


def empreinte(chemin: Path = FICHIER_QUESTIONS) -> str:
    """Hash court du fichier, inscrit dans chaque run pour savoir sur quoi il a tourne."""
    return hashlib.sha256(chemin.read_bytes()).hexdigest()[:12]


def filtrer(questions: list[Question], split: str = "tout",
            ids: list[str] | None = None) -> list[Question]:
    if ids:
        inconnus = set(ids) - {q.id for q in questions}
        if inconnus:
            raise JeuInvalide(f"questions inconnues : {sorted(inconnus)}")
        return [q for q in questions if q.id in ids]
    if split == "tout":
        return list(questions)
    return [q for q in questions if q.split == split]
