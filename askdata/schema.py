"""Description de la base telle que le modele la voit.

Trois niveaux, qui sont aussi les trois variantes du prompt comparees par
l'evaluation :

- brut       les tables, leurs colonnes, leurs types et leurs cles, lus dans
             information_schema. C'est ce qu'un outil generique fournit.
- valeurs    le niveau brut, plus les valeurs des colonnes texte peu variees
             et l'arborescence des champs jsonb, extraites automatiquement.
- documente  le niveau valeurs, plus le dictionnaire de donnees ecrit a la
             main (askdata/dictionnaire.md) : les conventions du format
             StatsBomb et du football qu'aucune introspection ne retrouve.

Les deux premiers niveaux ne demandent aucun travail humain. L'ecart entre
valeurs et documente mesure ce que rapporte la documentation metier.
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from .db import Base

VARIANTES = ("brut", "valeurs", "documente")
SCHEMA = "sb"
SEUIL_VALEURS = 40          # au-dela, une colonne texte n'est pas enumeree
SEUIL_VALEURS_JSONB = 15
DICTIONNAIRE = Path(__file__).with_name("dictionnaire.md")


def _colonnes(base: Base) -> dict[str, list[tuple[str, str, bool]]]:
    r = base.executer(f"""
        SELECT table_name, column_name, data_type, is_nullable = 'YES'
        FROM information_schema.columns
        WHERE table_schema = '{SCHEMA}'
        ORDER BY table_name, ordinal_position
    """)
    tables = defaultdict(list)
    for table, colonne, type_, nullable in r.lignes:
        tables[table].append((colonne, type_, nullable))
    return dict(tables)


def _cles(base: Base) -> tuple[set, dict]:
    """Colonnes de cle primaire, et cle etrangere -> table.colonne cible.

    Lu dans pg_catalog et non dans information_schema : ce dernier ne montre
    les contraintes qu'aux roles qui ont un droit autre que SELECT, donc pas
    au role en lecture seule de l'agent, qui verrait un schema sans cles.
    """
    r = base.executer(f"""
        SELECT c.contype, cl.relname, a.attname, fcl.relname, fa.attname
        FROM pg_constraint c
        JOIN pg_class cl ON cl.oid = c.conrelid
        JOIN pg_namespace n ON n.oid = cl.relnamespace
        CROSS JOIN LATERAL unnest(c.conkey, c.confkey) AS k(attnum, fattnum)
        JOIN pg_attribute a ON a.attrelid = c.conrelid AND a.attnum = k.attnum
        LEFT JOIN pg_class fcl ON fcl.oid = c.confrelid
        LEFT JOIN pg_attribute fa ON fa.attrelid = c.confrelid AND fa.attnum = k.fattnum
        WHERE n.nspname = '{SCHEMA}' AND c.contype IN ('p', 'f')
    """)
    primaires, etrangeres = set(), {}
    for type_, table, colonne, cible_table, cible_col in r.lignes:
        if type_ == "p":
            primaires.add((table, colonne))
        elif cible_table:
            etrangeres[(table, colonne)] = f"{SCHEMA}.{cible_table}.{cible_col}"
    return primaires, etrangeres


def _volumes(base: Base, tables) -> dict[str, int]:
    union = " UNION ALL ".join(
        f"SELECT '{t}', count(*) FROM {SCHEMA}.{t}" for t in tables)
    return dict(base.executer(union).lignes)


def decrire_brut(base: Base) -> str:
    tables = _colonnes(base)
    primaires, etrangeres = _cles(base)
    volumes = _volumes(base, tables)
    blocs = []
    for table, colonnes in tables.items():
        lignes = []
        for colonne, type_, nullable in colonnes:
            notes = []
            if (table, colonne) in primaires:
                notes.append("PK")
            if (table, colonne) in etrangeres:
                notes.append(f"-> {etrangeres[(table, colonne)]}")
            if not nullable and (table, colonne) not in primaires:
                notes.append("NOT NULL")
            suffixe = f"  -- {', '.join(notes)}" if notes else ""
            lignes.append(f"  {colonne} {type_}{suffixe}")
        blocs.append(f"{SCHEMA}.{table} ({volumes[table]} lignes)\n" + "\n".join(lignes))
    return "\n\n".join(blocs)


def _valeurs_texte(base: Base) -> list[str]:
    tables = _colonnes(base)
    sorties = []
    for table, colonnes in tables.items():
        for colonne, type_, _ in colonnes:
            if type_ != "text":
                continue
            r = base.executer(f"""
                SELECT {colonne}, count(*) FROM {SCHEMA}.{table}
                WHERE {colonne} IS NOT NULL
                GROUP BY {colonne} ORDER BY count(*) DESC
                LIMIT {SEUIL_VALEURS + 1}
            """)
            if 0 < len(r.lignes) <= SEUIL_VALEURS:
                valeurs = ", ".join(f"'{v}'" for v, _ in r.lignes)
                sorties.append(f"{SCHEMA}.{table}.{colonne} : {valeurs}")
    return sorties


def _arborescence_jsonb(base: Base) -> list[str]:
    """Chemins des feuilles de events.details, par type d'evenement.

    related_events (liste d'identifiants) est omis : present partout, il
    n'apprend rien. Pour les feuilles 'name', on liste les valeurs si elles
    sont peu nombreuses.
    """
    r = base.executer(f"""
        WITH RECURSIVE noeuds(type, chemin, valeur) AS (
            SELECT e.type, ARRAY[k.key], k.value
            FROM {SCHEMA}.events e, jsonb_each(e.details) k
            WHERE e.details IS NOT NULL AND k.key <> 'related_events'
          UNION ALL
            SELECT n.type, n.chemin || k.key, k.value
            FROM noeuds n, jsonb_each(n.valeur) k
            WHERE jsonb_typeof(n.valeur) = 'object' AND cardinality(n.chemin) < 4
        )
        SELECT type, array_to_string(chemin, '.') AS chemin,
               jsonb_typeof(valeur) AS genre,
               count(DISTINCT valeur) AS n_distinctes,
               array_agg(DISTINCT valeur #>> '{{}}') FILTER (
                   WHERE jsonb_typeof(valeur) = 'string') AS exemples
        FROM noeuds
        WHERE jsonb_typeof(valeur) <> 'object'
        GROUP BY type, chemin, jsonb_typeof(valeur)
        ORDER BY type, chemin
    """)
    par_type = defaultdict(list)
    for type_, chemin, genre, n_distinctes, exemples in r.lignes:
        acces = "details -> '" + "' -> '".join(chemin.split(".")) + "'"
        texte = f"    {acces} ({genre})"
        if exemples and n_distinctes <= SEUIL_VALEURS_JSONB and chemin.endswith("name"):
            texte += " : " + ", ".join(f"'{v}'" for v in sorted(exemples))
        par_type[type_].append(texte)
    return [f"  type = '{t}'\n" + "\n".join(c) for t, c in par_type.items()]


def decrire(base: Base, variante: str) -> str:
    if variante not in VARIANTES:
        raise ValueError(f"variante inconnue : {variante}")
    parties = ["## Tables\n\n" + decrire_brut(base)]
    if variante in ("valeurs", "documente"):
        parties.append("## Valeurs des colonnes texte\n\n" + "\n".join(_valeurs_texte(base)))
        parties.append("## Champs de sb.events.details (jsonb), par type d'evenement\n\n"
                       + "\n".join(_arborescence_jsonb(base)))
    if variante == "documente":
        parties.append(DICTIONNAIRE.read_text(encoding="utf-8").strip())
    return "\n\n".join(parties)
