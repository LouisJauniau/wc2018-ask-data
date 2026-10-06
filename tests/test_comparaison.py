"""Le comparateur, sur des resultats construits a la main."""

from decimal import Decimal

from askdata.comparaison import comparer, valeurs_egales
from askdata.db import Resultat


def R(colonnes, *lignes):
    return Resultat(tuple(colonnes), tuple(tuple(l) for l in lignes))


# --- valeurs ----------------------------------------------------------------

def test_entiers_exacts():
    assert valeurs_egales(205, 205)
    assert not valeurs_egales(205, 206)
    assert valeurs_egales(14, 14.0)
    assert valeurs_egales(14, Decimal("14"))


def test_arrondi_accepte_s_il_est_l_arrondi_exact():
    assert valeurs_egales(0.6650793, 0.67)
    assert valeurs_egales(0.6650793, Decimal("0.665"))
    assert valeurs_egales(66.507936, 66.5)
    assert not valeurs_egales(0.6650793, 0.66)


def test_arrondi_a_l_entier_refuse_pour_une_valeur_non_entiere():
    assert not valeurs_egales(66.507936, 67)
    assert not valeurs_egales(66.507936, Decimal("67"))


def test_arrondi_dans_les_deux_sens():
    # Une reference arrondie (cas d'une constante dans la requete de l'agent).
    assert valeurs_egales(Decimal("21.08"), 21.081061692)


def test_echelle_pourcentage_seulement_si_demandee():
    assert not valeurs_egales(0.894, 89.4)
    assert valeurs_egales(0.89389, 89.4, echelle_pourcentage=True)
    assert valeurs_egales(89.389, 0.894, echelle_pourcentage=True)


def test_textes_et_null():
    assert valeurs_egales("France", " france ")
    assert not valeurs_egales("France", "Allemagne")
    assert valeurs_egales(None, None)
    assert not valeurs_egales(None, 0)
    assert not valeurs_egales(True, 1)


# --- resultats ----------------------------------------------------------------

def test_colonnes_dans_un_autre_ordre_et_colonne_en_plus():
    ref = R(["equipe", "n"], ["Croatia", 54])
    obt = R(["n_tirs", "pays", "id"], [54, "Croatia", 785])
    assert comparer(ref, obt).juste


def test_cles_restreintes():
    ref = R(["equipe", "n"], ["Croatia", 54])
    obt = R(["pays", "tirs"], ["Croatia", 55])
    assert not comparer(ref, obt).juste
    assert comparer(ref, obt, cles=(("equipe",),)).juste


def test_resultat_vide():
    v = comparer(R(["n"], [3]), R(["n"]))
    assert not v.juste and v.diagnostic == "vide"


def test_cardinalite():
    v = comparer(R(["j"], ["a"], ["b"]), R(["j"], ["a"]))
    assert not v.juste and v.diagnostic == "cardinalite"


def test_premier_lit_seulement_les_premieres_lignes():
    ref = R(["equipe"], ["Croatia"])
    obt = R(["equipe", "n"], ["Croatia", 54], ["Brazil", 39], ["France", 35])
    assert comparer(ref, obt, forme="premier").juste
    obt_faux = R(["equipe", "n"], ["Brazil", 39], ["Croatia", 54])
    assert not comparer(ref, obt_faux, forme="premier").juste


def test_egalite_tronquee():
    ref = R(["m"], [1], [2], [3])
    v = comparer(ref, R(["m"], [2]), forme="premier")
    assert not v.juste and v.diagnostic == "egalite_tronquee"


def test_egalite_complete_dans_le_desordre():
    ref = R(["m"], [1], [2], [3])
    assert comparer(ref, R(["m"], [3], [1], [2]), forme="premier").juste


def test_ordre():
    ref = R(["j"], ["a"], ["b"], ["c"])
    assert comparer(ref, R(["j"], ["a"], ["b"], ["c"]), forme="ordonne").juste
    v = comparer(ref, R(["j"], ["c"], ["a"], ["b"]), forme="ordonne")
    assert not v.juste and v.diagnostic == "ordre"


def test_entites_ou_valeurs():
    ref = R(["equipe", "n"], ["Croatia", 54])
    assert comparer(ref, R(["e", "n"], ["Brazil", 54])).diagnostic == "entites"
    assert comparer(ref, R(["e", "n"], ["Croatia", 55])).diagnostic == "valeurs"


def test_combinaisons_de_lignes():
    # Chaque colonne a les bonnes valeurs, mais pas associees aux bonnes lignes.
    ref = R(["e", "n"], ["a", 1], ["b", 2])
    v = comparer(ref, R(["e", "n"], ["a", 2], ["b", 1]))
    assert not v.juste and v.diagnostic == "lignes"


def test_deux_colonnes_cles_ne_peuvent_pas_viser_la_meme_colonne():
    ref = R(["dom", "ext"], ["France", "France"])
    assert not comparer(ref, R(["e"], ["France"])).juste
    assert comparer(ref, R(["a", "b"], ["France", "France"])).juste


def test_cles_alternatives():
    ref = R(["match_id", "dom", "ext"], [1, "England", "Panama"])
    assert comparer(ref, R(["id"], [1]), cles=(("match_id",), ("dom", "ext"))).juste
    assert comparer(ref, R(["x", "y"], ["Panama", "England"]),
                    cles=(("match_id",), ("dom", "ext"))).juste


def test_doublons_comptent():
    ref = R(["j"], ["a"], ["b"])
    assert not comparer(ref, R(["j"], ["a"], ["a"])).juste
