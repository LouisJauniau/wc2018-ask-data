"""La verite terrain elle-meme : chaque reference s'execute, ne bouge pas, et
recoupe les faits connus du tournoi."""

import json

import pytest

from askdata import jeu, references
from askdata.comparaison import comparer

QUESTIONS = jeu.charger()
FIGEES = json.loads(references.FICHIER.read_text(encoding="utf-8"))
REFS = [(q, i, r) for q in QUESTIONS for i, r in enumerate(q.references)]


@pytest.mark.parametrize("q, i, ref", REFS, ids=[references.cle(q, i) for q, i, _ in REFS])
def test_reference_stable(base, q, i, ref):
    r = base.executer(ref.sql)
    assert r.lignes, "une reference vide ne departage rien"
    for alt in ref.cles or ():
        assert set(alt) <= set(r.colonnes)
    attendu = FIGEES[references.cle(q, i)]
    assert references.empreinte(r.colonnes, r.lignes) == attendu["empreinte"], (
        f"resultat change : {r.apercu(3)} au lieu de {attendu['apercu']}. "
        "Si c'est voulu : python -m askdata figer")


def test_toutes_les_references_sont_figees():
    assert set(FIGEES) == {references.cle(q, i) for q, i, _ in REFS}


@pytest.mark.parametrize("q", [q for q in QUESTIONS if q.sql_verif], ids=lambda q: q.id)
def test_double_ecriture(base, q):
    """Deux ecritures independantes de la meme reference concordent."""
    ref = q.references[0]
    v = comparer(base.executer(ref.sql), base.executer(q.sql_verif), ref.forme, ref.cles)
    assert v.juste, v


FAITS = {
    # Chiffres officiels de l'edition 2018.
    "nb_matchs": 64,
    "buts_total": 169,
    "nb_csc": 12,
    "penalties_jeu": 29,
    "nb_seances_tab": 4,
    "buts_france": 14,
}


@pytest.mark.parametrize("qid, valeur", FAITS.items())
def test_faits_officiels(base, qid, valeur):
    q = next(q for q in QUESTIONS if q.id == qid)
    assert base.executer(q.references[0].sql).lignes == ((valeur,),)


def test_meilleur_buteur_officiel(base):
    q = next(q for q in QUESTIONS if q.id == "meilleur_buteur")
    assert base.executer(q.references[0].sql).lignes == (("Harry Kane", 6),)
