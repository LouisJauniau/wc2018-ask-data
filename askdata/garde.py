"""Filtre des requetes produites par l'agent, avant execution.

Ce filtre ne protege pas la base : c'est le role en lecture seule et la
transaction READ ONLY qui la protegent (voir db.py). Il sert a refuser tot,
avec un message que le modele comprend, ce qui echouerait de toute facon, et
a interdire deux instructions dans un meme appel, que psycopg2 executerait en
ne rendant que le resultat de la derniere.

L'analyse se fait sur un squelette du SQL ou chaines et commentaires sont
effaces, pour qu'un mot interdit dans une chaine ('Substitution', 'Set
Piece') ne declenche rien.
"""

from __future__ import annotations

import re


class RequeteRefusee(ValueError):
    pass


MOTS_INTERDITS = frozenset("""
    insert update delete merge drop alter create truncate grant revoke copy
    call do lock vacuum reindex cluster refresh comment set reset listen
    notify prepare execute deallocate declare begin commit rollback savepoint
    discard load import into
""".split())

FONCTIONS_INTERDITES = re.compile(
    r"\b(pg_\w+|set_config|dblink\w*|lo_\w+|current_setting)\s*\(", re.IGNORECASE)


def squelette(sql: str) -> str:
    """Le SQL avec chaines, identifiants entre guillemets et commentaires
    remplaces par des espaces. Les longueurs sont conservees."""
    sortie = []
    i, n = 0, len(sql)
    while i < n:
        c = sql[i]
        if c == "-" and sql.startswith("--", i):
            fin = sql.find("\n", i)
            fin = n if fin == -1 else fin
            sortie.append(" " * (fin - i))
            i = fin
        elif c == "/" and sql.startswith("/*", i):
            # Les commentaires bloc s'imbriquent en PostgreSQL.
            profondeur, j = 1, i + 2
            while j < n and profondeur:
                if sql.startswith("/*", j):
                    profondeur, j = profondeur + 1, j + 2
                elif sql.startswith("*/", j):
                    profondeur, j = profondeur - 1, j + 2
                else:
                    j += 1
            sortie.append(" " * (j - i))
            i = j
        elif c in ("'", '"'):
            j = i + 1
            while j < n:
                if sql[j] == c:
                    if j + 1 < n and sql[j + 1] == c:  # guillemet double echappe
                        j += 2
                        continue
                    break
                j += 1
            j = min(j + 1, n)
            sortie.append(c + " " * (j - i - 2) + c if j - i >= 2 else " ")
            i = j
        elif c == "$":
            m = re.match(r"\$([A-Za-z_]\w*)?\$", sql[i:])
            if m:
                balise = m.group(0)
                fin = sql.find(balise, i + len(balise))
                fin = n if fin == -1 else fin + len(balise)
                sortie.append(" " * (fin - i))
                i = fin
            else:
                sortie.append(c)
                i += 1
        else:
            sortie.append(c)
            i += 1
    return "".join(sortie)


def verifier(sql: str) -> str:
    """Retourne la requete prete a executer, ou leve RequeteRefusee."""
    if not sql or not sql.strip():
        raise RequeteRefusee("requete vide")

    sq = squelette(sql)
    instructions = [s for s in sq.split(";") if s.strip()]
    if len(instructions) > 1:
        raise RequeteRefusee("une seule instruction par appel")

    premier = re.match(r"\s*\(*\s*([A-Za-z]+)", sq)
    if not premier or premier.group(1).lower() not in ("select", "with", "values", "table"):
        raise RequeteRefusee("seules les requetes SELECT (ou WITH ... SELECT) sont permises")

    mots = {m.lower() for m in re.findall(r"[A-Za-z_]+", sq)}
    interdits = sorted(mots & MOTS_INTERDITS)
    if interdits:
        raise RequeteRefusee(f"mot-cle interdit en lecture seule : {', '.join(interdits)}")

    fonction = FONCTIONS_INTERDITES.search(sq)
    if fonction:
        raise RequeteRefusee(f"fonction systeme interdite : {fonction.group(1)}")

    # Retire le point-virgule final, et lui seul.
    fin = len(sq.rstrip())
    if sq[:fin].endswith(";"):
        return sql[: fin - 1].rstrip()
    return sql.strip()
