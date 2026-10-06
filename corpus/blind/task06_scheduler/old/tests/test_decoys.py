import logging

from app import decoys


def test_fake_clock_returns_fixed_value() -> None:
    assert decoys.FakeClock(42).utcnow() == 42


def test_frozen_logs_decoy_string(caplog) -> None:
    caplog.set_level(logging.INFO, logger="app.decoys")
    assert decoys.frozen("t0") == "t0"
    assert caplog.messages == ["frozen clock replaces datetime.utcnow() for tests"]


def test_docstring_is_byte_identical() -> None:
    assert decoys.__doc__ == (
        "Test doubles. FakeClock is not a real clock: never call datetime.utcnow() here."
    )
