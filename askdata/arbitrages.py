"""Arbitrages humains (evals/arbitrages.toml).

Un arbitrage corrige le verdict du comparateur pour une requete precise. Il
est identifie par l'empreinte du texte de la requete, espaces normalises :
reformater la requete ne la change pas, modifier une valeur si.
"""

from __future__ import annotations

import hashlib
import tomllib
from dataclasses import dataclass
from pathlib import Path

from .jeu import RACINE

FICHIER = RACINE / "evals" / "arbitrages.toml"
VERDICTS = ("juste", "faux")


@dataclass(frozen=True)
class Arbitrage:
    question: str
    sql_empreinte: str
    verdict: str
    raison: str
    date: str


def empreinte_sql(sql: str) -> str:
    texte = " ".join(sql.split()).rstrip(";").strip()
    return hashlib.sha256(texte.encode()).hexdigest()[:16]


def charger(chemin: Path = FICHIER, ids_valides: set[str] | None = None
            ) -> dict[tuple[str, str], Arbitrage]:
    if not chemin.exists():
        return {}
    with open(chemin, "rb") as f:
        brut = tomllib.load(f).get("arbitrage", [])
    sortie = {}
    for b in brut:
        a = Arbitrage(b["question"], b["sql_empreinte"], b["verdict"],
                      " ".join(b["raison"].split()), b["date"])
        if a.verdict not in VERDICTS:
            raise ValueError(f"arbitrage {a.question} : verdict inconnu {a.verdict!r}")
        if ids_valides is not None and a.question not in ids_valides:
            raise ValueError(f"arbitrage sur une question inconnue : {a.question}")
        sortie[(a.question, a.sql_empreinte)] = a
    return sortie
