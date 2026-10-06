"""Comparaison d'un resultat obtenu a un resultat de reference.

On compare des resultats, pas des requetes : deux SQL differents qui
renvoient la meme reponse sont tous deux justes. Ce qui est tolere, et ce qui
ne l'est pas :

- l'ordre et le nom des colonnes ne comptent pas. Chaque colonne cle de la
  reference doit se retrouver, par ses valeurs, dans une colonne distincte du
  resultat obtenu ;
- les colonnes en plus sont tolerees (l'agent renvoie souvent le nom et la
  mesure quand on demande le nom) ;
- un nombre arrondi est accepte s'il est exactement l'arrondi de la
  reference au nombre de decimales qu'il affiche. 66,5 est juste pour
  66,5079 ; 67 ne l'est pas, et 206 n'est jamais juste pour 205 ;
- sur une question de proportion, 0,665 et 66,5 sont acceptes tous les deux ;
- le nombre de lignes compte, sauf en forme "premier", ou seules les N
  premieres lignes obtenues sont lues (N = lignes de la reference).

Limite connue : une colonne en plus qui contiendrait par hasard la bonne
valeur ferait passer une reponse fausse. Les tests de meta-evaluation
(tests/test_meta.py) mesurent ce risque sur des requetes fausses reelles.
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from decimal import Decimal

from .db import Resultat

MAX_COMBINAISONS = 5_000


@dataclass(frozen=True)
class Verdict:
    juste: bool
    diagnostic: str
    detail: str = ""


# Diagnostics, du plus au moins informatif :
#   exact             juste
#   vide              aucune ligne obtenue
#   egalite_tronquee  une partie seulement des ex aequo (LIMIT 1 sur une egalite)
#   cardinalite       pas le bon nombre de lignes
#   ordre             les bonnes lignes, pas dans l'ordre demande
#   entites           une colonne texte (equipe, joueur) introuvable
#   valeurs           les colonnes texte sont la, une mesure est fausse
#   lignes            chaque colonne se retrouve, mais pas les combinaisons

PROXIMITE = ("egalite_tronquee", "ordre", "lignes", "cardinalite", "valeurs",
             "entites", "vide")


def _est_nombre(v) -> bool:
    return isinstance(v, (int, float, Decimal)) and not isinstance(v, bool)


def _decimales(v) -> int:
    """Nombre de decimales affichees : celui qui dit a quel pas v a ete arrondi."""
    if isinstance(v, Decimal):
        exposant = v.as_tuple().exponent
        return max(0, -exposant) if isinstance(exposant, int) else 0
    if isinstance(v, float):
        texte = repr(v)
        if "e" in texte or "." not in texte:
            return 0
        return len(texte.split(".")[1].rstrip("0"))
    return 0


def _nombres_egaux(a, b) -> bool:
    fa, fb = float(a), float(b)
    if math.isclose(fa, fb, rel_tol=1e-9, abs_tol=1e-9):
        return True
    # L'un des deux est-il l'autre arrondi ? Au-dela de 8 decimales, la valeur
    # n'a pas ete arrondie a la main, c'est la precision du calcul.
    for exact, arrondi in ((fa, b), (fb, a)):
        d = _decimales(arrondi)
        if 1 <= d <= 8 and abs(exact - float(arrondi)) <= 0.5 * 10 ** -d * (1 + 1e-9):
            return True
    return False


def valeurs_egales(ref, obt, echelle_pourcentage: bool = False) -> bool:
    if ref is None or obt is None:
        return ref is None and obt is None
    if isinstance(ref, bool) or isinstance(obt, bool):
        return ref is obt
    if _est_nombre(ref) and _est_nombre(obt):
        if _nombres_egaux(ref, obt):
            return True
        if echelle_pourcentage:
            return (_nombres_egaux(float(ref) * 100, obt)
                    or _nombres_egaux(float(ref) / 100, obt))
        return False
    if isinstance(ref, str) and isinstance(obt, str):
        return ref.strip().casefold() == obt.strip().casefold()
    return str(ref) == str(obt)


def _apparier(attendus: list, obtenus: list, egal, inclusion: bool = False) -> bool:
    """Multi-ensembles egaux (ou attendus contient obtenus si inclusion).

    Appariement glouton. Avec une tolerance numerique la relation n'est pas
    transitive, mais les ecarts toleres sont trop fins pour que deux valeurs
    distinctes d'une reference tombent dans la meme tolerance.
    """
    if not inclusion and len(attendus) != len(obtenus):
        return False
    restants = list(attendus)
    for o in obtenus:
        for i, a in enumerate(restants):
            if egal(a, o):
                del restants[i]
                break
        else:
            return False
    return True


def comparer(reference: Resultat, obtenu: Resultat, forme: str = "ensemble",
             cles: tuple[tuple[str, ...], ...] | None = None,
             echelle_pourcentage: bool = False) -> Verdict:
    if not reference.lignes:
        raise ValueError("une reference vide ne permet aucune comparaison")
    if not obtenu.lignes:
        return Verdict(False, "vide", "aucune ligne obtenue")

    alternatives = cles or (reference.colonnes,)
    echecs = []
    for alt in alternatives:
        v = _comparer_selon(reference, obtenu, forme, alt, echelle_pourcentage)
        if v.juste:
            return v
        echecs.append(v)
    # Entre plusieurs alternatives, le diagnostic le plus proche de la bonne
    # reponse est le plus utile : "egalite_tronquee" sur les noms d'equipes dit
    # plus que "valeurs" sur un match_id que l'agent n'a pas renvoye.
    return min(echecs, key=lambda v: PROXIMITE.index(v.diagnostic))


def _comparer_selon(reference: Resultat, obtenu: Resultat, forme: str,
                    cles: tuple[str, ...], echelle: bool) -> Verdict:
    manquantes = [c for c in cles if c not in reference.colonnes]
    if manquantes:
        raise ValueError(f"colonnes cles absentes de la reference : {manquantes}")

    idx = [reference.colonnes.index(c) for c in cles]
    attendues = [tuple(l[i] for i in idx) for l in reference.lignes]
    n_ref = len(attendues)

    if forme == "premier":
        lues = list(obtenu.lignes[:n_ref])
        inclusion = len(lues) < n_ref
    else:
        lues = list(obtenu.lignes)
        inclusion = False
        if len(lues) != n_ref:
            return Verdict(False, "cardinalite",
                           f"{len(lues)} lignes obtenues, {n_ref} attendues")

    def egal(a, b):
        return valeurs_egales(a, b, echelle)

    def egal_ligne(a, b):
        return all(egal(x, y) for x, y in zip(a, b, strict=True))

    def colonne(j):
        return [ligne[j] for ligne in lues]

    n_col = len(obtenu.colonnes)

    # Colonnes candidates pour chaque cle, d'apres leurs seules valeurs.
    candidates = []
    for k in range(len(cles)):
        attendu_k = [a[k] for a in attendues]
        if forme == "ordonne":
            cands = [j for j in range(n_col)
                     if egal_ligne(attendu_k, colonne(j))]
        else:
            cands = [j for j in range(n_col)
                     if _apparier(attendu_k, colonne(j), egal, inclusion)]
        candidates.append(cands)

    sans_candidate = [k for k, c in enumerate(candidates) if not c]
    if sans_candidate:
        if forme == "ordonne":
            # Les bonnes valeurs dans le desordre ?
            v = _comparer_selon(reference, obtenu, "ensemble", cles, echelle)
            if v.juste:
                return Verdict(False, "ordre", "lignes justes, ordre different")
        texte = any(isinstance(attendues[0][k], str) for k in sans_candidate)
        noms = ", ".join(cles[k] for k in sans_candidate)
        return Verdict(False, "entites" if texte else "valeurs",
                       f"introuvable dans le resultat : {noms}")

    for n, combinaison in enumerate(itertools.product(*candidates)):
        if n >= MAX_COMBINAISONS:
            break
        if len(set(combinaison)) < len(combinaison):
            continue
        projetees = [tuple(ligne[j] for j in combinaison) for ligne in lues]
        if forme == "ordonne":
            ok = all(egal_ligne(a, b) for a, b in zip(attendues, projetees, strict=True))
        else:
            ok = _apparier(attendues, projetees, egal_ligne, inclusion)
        if ok:
            if inclusion:
                return Verdict(False, "egalite_tronquee",
                               f"{len(lues)} ligne(s) sur {n_ref} ex aequo")
            return Verdict(True, "exact")

    return Verdict(False, "lignes", "chaque colonne existe, pas les combinaisons")
