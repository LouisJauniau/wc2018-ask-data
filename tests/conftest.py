"""Les tests marques `base` ont besoin de la base wc2018 (variable WC_DSN).
Ils sont sautes, avec un message, si elle est injoignable."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from askdata.db import DSN, Base  # noqa: E402


@pytest.fixture(scope="session")
def base():
    b = Base(DSN)
    try:
        b.executer("SELECT 1")
    except Exception as e:  # base absente, mauvais DSN, serveur arrete
        pytest.skip(f"base wc2018 injoignable ({e.__class__.__name__}) : definir WC_DSN")
    yield b
    b.fermer()
