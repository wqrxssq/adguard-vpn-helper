import tempfile
import os
from datetime import date, timedelta

import pytest

from src.db.repository import Repository
from src.db.models import Account

@pytest.fixture
def repo(tmp_path):
    dbfile = tmp_path / "test.db"
    url = f"sqlite:///{dbfile}"
    r = Repository(url)
    return r

def test_add_and_list(repo):
    repo.add_account(123, "a@example.com", 10)
    accs = repo.list_accounts(123)
    assert len(accs) == 1
    a = accs[0]
    assert a.email == "a@example.com"
    today = date.today()
    assert a.date_end == (today + timedelta(days=10)).isoformat()

def test_mark_and_delete(repo):
    repo.add_account(1, "x@e.com", 5)
    assert repo.mark_used(1, "x@e.com") is True
    acc = repo.list_accounts(1)[0]
    assert acc.is_used == 1
    assert repo.delete_account(1, "x@e.com") is True
    assert repo.list_accounts(1) == []

def test_find_free(repo):
    repo.add_account(5, "a@e.com", 20)
    repo.add_account(5, "b@e.com", 2)
    free = repo.find_free(5)
    assert free.email == "b@e.com"  # ближайший по date_end

def test_refresh_expired(repo):
    repo.add_account(7, "old@e.com", 0)
    updated = repo.refresh_expired() # должен обновиться TODO: на деле должен стать -1
    assert updated >= 1
    acc = repo.list_accounts(7)[0]
    assert acc.is_used == 0
    assert acc.date_start == date.today().isoformat()
