"""Builds jobs; jobs.py imports this module back (a real cycle)."""

from datetime import timedelta

import app.jobs
from app import clock


def make_job(delay_s):
    return app.jobs.Job(run_at=clock.now() + timedelta(seconds=delay_s))
