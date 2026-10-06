"""Un run de bout en bout, avec le fournisseur rejeu : lancement, reprise,
notation, rapport."""

import json

import pytest

from askdata import evaluation, jeu, rapport
from askdata.db import DSN
from askdata.llm import FournisseurRejeu


@pytest.fixture
def reponses(tmp_path):
    f = tmp_path / "reponses.jsonl"
    lignes = [
        {"id": "nb_matchs", "statut": "reponse", "sql": "SELECT 64"},
        {"id": jeu.id_opaque("buts_france"), "statut": "reponse", "sql": "SELECT 12"},
        {"id": "affluence_finale", "statut": "hors_perimetre", "sql": ""},
    ]
    f.write_text("\n".join(json.dumps(l) for l in lignes), encoding="utf-8")
    return f


def test_run_complet_et_reprise(base, tmp_path, reponses):
    questions = jeu.filtrer(jeu.charger(), ids=["nb_matchs", "buts_france",
                                                 "affluence_finale", "tirs_croatie"])
    dossier = tmp_path / "run"
    silence = lambda *_: None  # noqa: E731

    evaluation.lancer(questions, FournisseurRejeu(reponses, "test"), "brut", "direct",
                      paralleles=1, dossier=dossier, dsn=DSN, journal=silence)
    issues = {n.id: n.issue for n in evaluation.noter_run(dossier, questions, DSN)}
    assert issues == {"nb_matchs": "juste", "buts_france": "faux_silencieux",
                      "affluence_finale": "abstention_juste", "tirs_croatie": "incident"}

    texte = rapport.rapport_run(dossier)
    assert "1/3 (33 %)" in texte          # exactitude sur les trois repondables
    assert "### buts_france" in texte      # l'echec est detaille

    # Reprise a l'identique : rien a refaire.
    evaluation.lancer(questions, FournisseurRejeu(reponses, "test"), "brut", "direct",
                      paralleles=1, dossier=dossier, dsn=DSN, journal=silence)
    assert len(evaluation.lire_traces(dossier)) == 4

    # Reprise avec une autre configuration : refusee.
    with pytest.raises(ValueError, match="variante"):
        evaluation.lancer(questions, FournisseurRejeu(reponses, "test"), "documente",
                          "direct", paralleles=1, dossier=dossier, dsn=DSN, journal=silence)
