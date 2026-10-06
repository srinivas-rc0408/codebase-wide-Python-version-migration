"""Job records; scheduler.py imports this module back (a real cycle)."""

from dataclasses import dataclass
from datetime import datetime

import app.scheduler
from app import clock


@dataclass
class Job:
    run_at: datetime


def due(job):
    return clock.now() >= job.run_at


def schedule(delay_s):
    return app.scheduler.make_job(delay_s)
