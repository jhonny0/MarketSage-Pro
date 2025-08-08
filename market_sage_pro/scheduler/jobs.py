from __future__ import annotations

import os
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

from ..utils.logging import get_logger

logger = get_logger(__name__)


sched = BlockingScheduler(timezone="US/Eastern")


@sched.scheduled_job("cron", day_of_week="mon-fri", hour=8, minute=0)
def morning_setup() -> None:
    logger.info("Morning setup: refresh symbols, warm models")


@sched.scheduled_job("cron", day_of_week="mon-fri", hour=16, minute=5)
def daily_report() -> None:
    logger.info("Generating daily report PDF and emailing...")


@sched.scheduled_job("interval", minutes=10)
def update_hourly_model() -> None:
    logger.info("Updating online LightGBM on the last 10k bars...")


if __name__ == "__main__":
    logger.info("Starting scheduler...")
    sched.start()