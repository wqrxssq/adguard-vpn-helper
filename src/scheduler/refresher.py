import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import threading
from typing import Callable

logger = logging.getLogger(__name__)

class Refresher:
    def __init__(self, repo, hour: int = 0, minute: int = 10):
        self.repo = repo
        self.scheduler = BackgroundScheduler()
        self.trigger = CronTrigger(hour=hour, minute=minute)

    def start(self):
        self.scheduler.add_job(self._job, trigger=self.trigger, id="refresh_accounts", replace_existing=True)
        self.scheduler.start()
        logger.info("Refresher started")

    def shutdown(self):
        self.scheduler.shutdown(wait=False)

    def _job(self):
        try:
            updated = self.repo.refresh_expired()
            logger.info(f"Refresher: updated {updated} accounts")
        except Exception as e:
            logger.exception("Error in refresher job")
