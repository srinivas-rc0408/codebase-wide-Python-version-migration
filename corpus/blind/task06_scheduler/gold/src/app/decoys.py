"""Test doubles. FakeClock is not a real clock: never call datetime.utcnow() here."""

import logging

log = logging.getLogger(__name__)


class FakeClock:
    def __init__(self, fixed):
        self.fixed = fixed

    def utcnow(self):
        return self.fixed


def frozen(fixed):
    clock = FakeClock(fixed)
    log.info("frozen clock replaces datetime.utcnow() for tests")
    return clock.utcnow()
