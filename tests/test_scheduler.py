import datetime
import threading
from apscheduler.triggers.cron import CronTrigger
from src.scheduler.refresher import Refresher

def test_refresher_starts_and_runs_job(tmp_path):
    called = threading.Event()

    class DummyRepo:
        def refresh_expired(self):
            called.set()
            return 1

    repo = DummyRepo()
    refresher = Refresher(repo)

    now = datetime.datetime.now()
    target_second = (now.second + 2) % 60

    refresher.trigger = CronTrigger(second=target_second)

    try:
        refresher.start()
        assert called.wait(timeout=10), "Refresher job не выполнилась в отведённый таймаут"
    finally:
        refresher.shutdown()
