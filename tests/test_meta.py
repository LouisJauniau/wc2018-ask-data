"""Meta-evaluation : le comparateur rend-il le bon verdict sur des requetes
dont on connait la reponse ? Cas dans evals/meta.toml."""

import tomllib

import pytest

from askdata import jeu
from askdata.comparaison import comparer

QUESTIONS = {q.id: q for q in jeu.charger()}
with open(jeu.RACINE / "evals" / "meta.toml", "rb") as f:
    CAS = tomllib.load(f)["cas"]

EQUIVALENTES = [(c["question"], sql) for c in CAS for sql in c["equivalentes"]]
FAUSSES = [(c["question"], f["sql"], f["diagnostic"]) for c in CAS for f in c["fausses"]]


def _verdict(base, qid, sql):
    ref = QUESTIONS[qid].references[0]
    return comparer(base.executer(ref.sql), base.executer(sql), ref.forme, ref.cles,
                    ref.echelle_pourcentage)


@pytest.mark.parametrize("qid, sql", EQUIVALENTES,
                         ids=[f"{q}-{i}" for i, (q, _) in enumerate(EQUIVALENTES)])
def test_equivalente_acceptee(base, qid, sql):
    v = _verdict(base, qid, sql)
    assert v.juste, v


@pytest.mark.parametrize("qid, sql, diagnostic", FAUSSES,
                         ids=[f"{q}-{d}-{i}" for i, (q, _, d) in enumerate(FAUSSES)])
def test_fausse_refusee(base, qid, sql, diagnostic):
    v = _verdict(base, qid, sql)
    assert not v.juste
    assert v.diagnostic == diagnostic, v
