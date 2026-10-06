"""Acces en lecture seule a la base wc2018.

Trois protections empilees, de la plus forte a la plus faible :

1. le role de connexion n'a que le droit SELECT sur le schema sb
   (sql/role_lecteur.sql) ;
2. chaque requete tourne dans une transaction READ ONLY, annulee ensuite ;
3. statement_timeout coupe une requete trop longue.

Le filtre de garde.py vient en plus. Il sert a renvoyer a l'agent un message
clair, il ne protege pas la base : c'est le role qui la protege.
"""

from __future__ import annotations

import datetime as dt
import os
import re
import uuid
from dataclasses import dataclass
from decimal import Decimal

import psycopg2

# Par defaut, le role en lecture seule cree par sql/role_lecteur.sql, sur la
# base locale. Son mot de passe se range dans le fichier pgpass de PostgreSQL.
DSN_DEFAUT = "host=localhost dbname=wc2018 user=wc_lecteur"
DSN = os.environ.get("WC_DSN", DSN_DEFAUT)


def dsn_affichable(dsn: str) -> str:
    """Le DSN sans son mot de passe, pour un message d'erreur."""
    return re.sub(r"(password\s*=\s*)\S+", lambda m: m.group(1) + "***", dsn)


@dataclass(frozen=True)
class Resultat:
    colonnes: tuple[str, ...]
    lignes: tuple[tuple, ...]
    tronque: bool = False

    def apercu(self, n: int = 5) -> list[list]:
        """Les n premieres lignes, serialisables en JSON."""
        return [[_vers_json(v) for v in ligne] for ligne in self.lignes[:n]]


class ErreurSQL(Exception):
    """Erreur renvoyee par PostgreSQL. sqlstate vaut None hors PostgreSQL."""

    def __init__(self, message: str, sqlstate: str | None = None):
        super().__init__(message)
        self.message = message
        self.sqlstate = sqlstate


def _normaliser(valeur):
    """Ramene une cellule a un type comparable.

    Les Decimal sont gardes tels quels : leur nombre de decimales dit si la
    valeur a ete arrondie, ce dont le comparateur a besoin.
    """
    if isinstance(valeur, (dt.date, dt.time, dt.datetime)):
        return valeur.isoformat()
    if isinstance(valeur, dt.timedelta):
        return valeur.total_seconds()
    if isinstance(valeur, uuid.UUID):
        return str(valeur)
    if isinstance(valeur, memoryview):
        return bytes(valeur).hex()
    return valeur


def _vers_json(valeur):
    if isinstance(valeur, Decimal):
        return float(valeur)
    if isinstance(valeur, (dict, list, str, int, float, bool)) or valeur is None:
        return valeur
    return str(valeur)


class ErreurConnexion(Exception):
    """La base est injoignable ou refuse le role : rien ne sert de continuer."""


class Base:
    """Une connexion, une requete a la fois. Un fil d'execution = une Base."""

    def __init__(self, dsn: str = DSN, timeout_ms: int = 10_000, max_lignes: int = 5_000):
        self.dsn = dsn
        self.timeout_ms = timeout_ms
        self.max_lignes = max_lignes
        self._conn = None

    def _connexion(self):
        if self._conn is None or self._conn.closed:
            try:
                self._conn = psycopg2.connect(self.dsn)
            except psycopg2.OperationalError as e:
                raise ErreurConnexion(str(e).strip().splitlines()[0]) from None
            except UnicodeDecodeError:
                # Un serveur aux messages en francais sous Windows les envoie
                # en cp1252, que psycopg2 ne sait pas decoder : le vrai
                # message (le plus souvent un refus d'authentification) est
                # perdu.
                raise ErreurConnexion(
                    "le serveur a refuse la connexion avec un message illisible "
                    "(encodage) ; le plus souvent un mot de passe refuse") from None
            self._conn.set_session(readonly=True, autocommit=False)
        return self._conn

    def executer(self, sql: str) -> Resultat:
        conn = self._connexion()
        try:
            with conn.cursor() as cur:
                cur.execute("SET LOCAL statement_timeout = %s", (self.timeout_ms,))
                cur.execute(sql)
                if cur.description is None:
                    raise ErreurSQL("la requete ne renvoie pas de lignes")
                colonnes = tuple(d.name for d in cur.description)
                lignes = cur.fetchmany(self.max_lignes + 1)
        except psycopg2.Error as e:
            conn.rollback()
            message = (e.pgerror or str(e)).strip().splitlines()[0]
            raise ErreurSQL(message, e.pgcode) from None
        else:
            conn.rollback()
        tronque = len(lignes) > self.max_lignes
        lignes = lignes[: self.max_lignes]
        return Resultat(
            colonnes=colonnes,
            lignes=tuple(tuple(_normaliser(v) for v in ligne) for ligne in lignes),
            tronque=tronque,
        )

    def fermer(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None
