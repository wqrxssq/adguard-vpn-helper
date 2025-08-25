from datetime import date, timedelta
from src.db import repository as repository_module

def test_refresh_expired(repo, monkeypatch):
    real_today = date.today()

    repo.add_account(7, "old@e.com", 0)

    updated_first = repo.refresh_expired()
    assert updated_first == 0, "На день окончания обновления не должно быть"

    acc1 = repo.list_accounts(7)[0]
    assert acc1.date_end == real_today.isoformat()
    assert acc1.date_start == (real_today - timedelta(days=30)).isoformat()

    class FakeDate(date):
        @classmethod
        def today(cls):
            return real_today + timedelta(days=1)

    monkeypatch.setattr(repository_module, "date", FakeDate)

    updated_second = repo.refresh_expired()
    assert updated_second == 1, "После перехода на следующий день запись должна обновиться"

    acc2 = repo.list_accounts(7)[0]
    assert acc2.is_used == 0
    assert acc2.date_start == (real_today + timedelta(days=1)).isoformat()
    assert acc2.date_end == (real_today + timedelta(days=1) + timedelta(days=30)).isoformat()
