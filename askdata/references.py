"""Empreintes des resultats de reference (evals/references.json).

La verite terrain est du code, elle peut donc changer sans qu'on le voie :
une reference modifiee par megarde, une base rechargee differemment. On
fige le resultat de chaque reference ; tests/test_references.py echoue si
l'un d'eux bouge. Apres une modification voulue : python -m askdata figer.
"""

from __future__ import annotations

import hashlib
import json
from decimal import Decimal

from .db import Base
from .jeu import RACINE, Question

FICHIER = RACINE / "evals" / "references.json"


def _canonique(v):
    """Representation stable d'une cellule. Les flottants sont ramenes a 9
    chiffres significatifs pour ne pas dependre du dernier bit du calcul."""
    if isinstance(v, (float, Decimal)) and not isinstance(v, bool):
        return f"{float(v):.9g}"
    return v


def empreinte(colonnes, lignes) -> str:
    lignes_canon = sorted(json.dumps([_canonique(v) for v in l], ensure_ascii=False,
                                     default=str) for l in lignes)
    brut = json.dumps([list(colonnes), lignes_canon], ensure_ascii=False)
    return hashlib.sha256(brut.encode()).hexdigest()[:16]


def cle(q: Question, i: int) -> str:
    return q.id if len(q.references) == 1 else f"{q.id}#{i}"


def calculer(questions: list[Question], base: Base) -> dict:
    sortie = {}
    for q in questions:
        for i, ref in enumerate(q.references):
            r = base.executer(ref.sql)
            sortie[cle(q, i)] = {
                "n_lignes": len(r.lignes),
                "apercu": r.apercu(3),
                "empreinte": empreinte(r.colonnes, r.lignes),
            }
    return sortie
