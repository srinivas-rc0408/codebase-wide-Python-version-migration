"""Hidden semantic tests: gold/ only, never shown to the agent."""

from app import clock, config


def test_clock_is_timezone_aware() -> None:
    assert clock.now().tzinfo is not None


def test_epoch_is_timezone_aware() -> None:
    assert config.EPOCH.tzinfo is not None
