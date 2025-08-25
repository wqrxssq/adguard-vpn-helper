import sys
import os
import pytest
from src.db.repository import Repository

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
sys.path.insert(0, SRC)

@pytest.fixture
def repo(tmp_path):
    dbfile = tmp_path / "test.db"
    url = f"sqlite:///{dbfile}"
    r = Repository(url)
    return r
