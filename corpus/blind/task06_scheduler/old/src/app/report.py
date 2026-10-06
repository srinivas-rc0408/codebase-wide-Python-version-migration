"""Operational report."""

from app import clock, config


def age_days():
    return (clock.now() - config.EPOCH).days
