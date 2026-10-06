"""La description de la base vue par le modele, sous le role de l'agent."""

from askdata import schema


def test_cles_visibles(base):
    texte = schema.decrire_brut(base)
    assert "match_id integer  -- PK" in texte
    assert "event_id uuid  -- PK, -> sb.events.event_id" in texte
    assert "home_team_id integer  -- -> sb.teams.team_id, NOT NULL" in texte


def test_variantes_emboitees(base):
    brut, valeurs, documente = (schema.decrire(base, v) for v in schema.VARIANTES)
    assert valeurs.startswith(brut) and documente.startswith(valeurs)
    assert "'Own Goal Against'" not in brut and "'Own Goal Against'" in valeurs
    assert "outcome NULL signifie passe réussie" in documente
