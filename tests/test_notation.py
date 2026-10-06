"""Classement des issues, a partir de traces fabriquees, sur la vraie base."""

import pytest

from askdata import jeu
from askdata.agent import Etape, Trace
from askdata.evaluation import Noteur

Q = {q.id: q for q in jeu.charger()}


def trace(qid, statut="reponse", sql="", ambiguite=False, etapes=()):
    return Trace(id=qid, repetition=0, question=Q[qid].question, mode="agent",
                 final={"statut": statut, "sql": sql, "ambiguite": ambiguite,
                        "interpretation": "", "reponse": ""},
                 etapes=list(etapes))


@pytest.fixture
def noteur(base):
    return Noteur(base)


def test_juste_et_faux_silencieux(noteur):
    n = noteur.noter(Q["buts_france"], trace("buts_france", sql="SELECT 14 AS buts"))
    assert n.issue == "juste"
    n = noteur.noter(Q["buts_france"], trace("buts_france", sql="SELECT 12"))
    assert n.issue == "faux_silencieux" and n.diagnostic == "valeurs"
    assert "attendu" in n.detail


def test_erreur_execution_et_abstention(noteur):
    n = noteur.noter(Q["buts_france"], trace("buts_france", sql="SELECT nimporte FROM sb.matches"))
    assert n.issue == "erreur_execution" and n.diagnostic.startswith("42703")
    n = noteur.noter(Q["buts_france"], trace("buts_france", statut="clarification"))
    assert n.issue == "abstention_a_tort"


def test_erreur_intermediaire_rattrapee(noteur):
    t = trace("nb_matchs", sql="SELECT 64",
              etapes=[Etape("SELECT x", erreur="42703: ..."), Etape("SELECT 64", n_lignes=1)])
    n = noteur.noter(Q["nb_matchs"], t)
    assert n.issue == "juste" and n.n_erreurs_intermediaires == 1 and n.n_requetes == 2


def test_ambigue(noteur):
    q = Q["victoires_russie"]
    n = noteur.noter(q, trace(q.id, sql="SELECT 3", ambiguite=True))
    assert n.issue == "signalee" and n.acceptable and n.interpretation == "tirs au but compris"
    n = noteur.noter(q, trace(q.id, sql="SELECT 2"))
    assert n.issue == "non_signalee" and n.acceptable
    n = noteur.noter(q, trace(q.id, sql="SELECT 5", ambiguite=True))
    assert n.issue == "signalee" and n.acceptable is False
    n = noteur.noter(q, trace(q.id, statut="clarification"))
    assert n.issue == "signalee" and n.acceptable is None


def test_hors_perimetre(noteur):
    q = Q["france_2022"]
    assert noteur.noter(q, trace(q.id, statut="hors_perimetre")).issue == "abstention_juste"
    assert noteur.noter(q, trace(q.id, sql="SELECT 14")).issue == "hallucination"


def test_faux_signalement_sur_question_claire(noteur):
    n = noteur.noter(Q["nb_matchs"], trace("nb_matchs", sql="SELECT 64", ambiguite=True))
    assert n.issue == "juste" and n.signalee


def test_incident(noteur):
    t = Trace(id="nb_matchs", repetition=0, question="", mode="agent", incident="max_tours")
    n = noteur.noter(Q["nb_matchs"], t)
    assert n.issue == "incident" and n.diagnostic == "max_tours"


def test_arbitrage_ne_vise_que_la_requete_arbitree(base):
    from askdata.arbitrages import Arbitrage, empreinte_sql

    sql = "SELECT 'Total' AS e, 23 AS n UNION ALL SELECT 'France', 8"
    cle = ("tirs_finale", empreinte_sql(sql))
    noteur = Noteur(base, {cle: Arbitrage(*cle, "juste", "total present", "2026-10-06")})

    n = noteur.noter(Q["tirs_finale"], trace("tirs_finale", sql=sql))
    assert n.issue == "juste" and n.issue_auto == "faux_silencieux"
    assert n.arbitrage == "total present"

    # Meme requete reformatee : meme empreinte, meme arbitrage.
    n = noteur.noter(Q["tirs_finale"], trace("tirs_finale", sql=sql.replace(" ", "\n  ") + ";"))
    assert n.issue == "juste"

    # Autre requete sur la meme question : pas d'arbitrage.
    n = noteur.noter(Q["tirs_finale"], trace("tirs_finale", sql="SELECT 'Total', 24"))
    assert n.issue == "faux_silencieux" and not n.arbitrage
