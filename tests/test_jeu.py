import pytest

from askdata import jeu


def test_le_jeu_se_charge_et_reste_equilibre():
    qs = jeu.charger()
    assert len(qs) >= 50
    for split in jeu.SPLITS:
        partie = [q for q in qs if q.split == split]
        # Chaque split contient des questions de chaque categorie.
        assert {q.categorie for q in partie} == set(jeu.CATEGORIES), split


def test_questions_ambigues_documentees():
    for q in jeu.charger():
        if q.ambigue:
            assert q.ambiguite


def test_validation(tmp_path):
    f = tmp_path / "q.toml"
    f.write_text('[[question]]\nid = "x"\nquestion = "?"\ncategorie = "comptage"\n'
                 'split = "dev"\n', encoding="utf-8")
    with pytest.raises(jeu.JeuInvalide, match="exactement une reference"):
        jeu.charger(f)


def test_filtrer():
    qs = jeu.charger()
    assert all(q.split == "dev" for q in jeu.filtrer(qs, "dev"))
    assert [q.id for q in jeu.filtrer(qs, ids=["nb_matchs"])] == ["nb_matchs"]
    with pytest.raises(jeu.JeuInvalide):
        jeu.filtrer(qs, ids=["inexistante"])


def test_chaque_piege_est_documente():
    catalogue = (jeu.RACINE / "evals" / "PIEGES.md").read_text(encoding="utf-8")
    utilises = {p for q in jeu.charger() for p in q.pieges}
    absents = sorted(p for p in utilises if f"**`{p}`**" not in catalogue)
    assert not absents, f"pieges absents de PIEGES.md : {absents}"


def test_arbitrages_valides():
    from askdata import arbitrages
    charges = arbitrages.charger(ids_valides={q.id for q in jeu.charger()})
    assert all(len(a.sql_empreinte) == 16 for a in charges.values())
