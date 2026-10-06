import pytest

from askdata.garde import RequeteRefusee, squelette, verifier


@pytest.mark.parametrize("sql", [
    "SELECT 1",
    "  with t as (select 1) select * from t  ",
    "(SELECT 1) UNION (SELECT 2)",
    "SELECT 1;",
    "SELECT 1 ;  \n -- fin\n",
    "SELECT * FROM sb.events WHERE type = 'Substitution'",
    "SELECT 'drop table x; delete' AS texte",
    "SELECT 1 -- ; drop table x",
    "SELECT 1 /* update /* imbrique */ ; */",
    "SELECT $$ ; insert $$",
    "SELECT \"set\" FROM (SELECT 1 AS \"set\") t",
    "SELECT * FROM sb.matches FETCH FIRST 3 ROWS ONLY",
])
def test_requetes_acceptees(sql):
    verifier(sql)


@pytest.mark.parametrize("sql, motif", [
    ("", "vide"),
    ("SELECT 1; SELECT 2", "une seule"),
    ("DROP TABLE sb.teams", "SELECT"),
    ("UPDATE sb.teams SET team_name = 'x'", "SELECT"),
    ("WITH x AS (DELETE FROM sb.teams RETURNING *) SELECT * FROM x", "delete"),
    ("SELECT * INTO copie FROM sb.teams", "into"),
    ("SELECT pg_sleep(30)", "pg_sleep"),
    ("SELECT set_config('statement_timeout', '0', false)", "set_config"),
    ("SELECT pg_read_file('postgresql.conf')", "pg_read_file"),
])
def test_requetes_refusees(sql, motif):
    with pytest.raises(RequeteRefusee, match=motif):
        verifier(sql)


def test_point_virgule_final_retire():
    assert verifier("SELECT 1;  ") == "SELECT 1"
    assert verifier("SELECT ';'") == "SELECT ';'"


def test_squelette_conserve_les_longueurs():
    sql = "SELECT 'a''b', \"c\" /* d */ -- e\n FROM t"
    assert len(squelette(sql)) == len(sql)
    assert "a" not in squelette(sql).replace("FROM", "")


def test_dsn_affichable_masque_le_mot_de_passe():
    from askdata.db import dsn_affichable
    assert dsn_affichable("host=h password=s3cr=t user=u") == "host=h password=*** user=u"
    assert dsn_affichable("host=h user=u") == "host=h user=u"
