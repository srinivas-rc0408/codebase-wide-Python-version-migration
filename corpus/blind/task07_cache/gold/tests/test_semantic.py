"""Hidden semantic tests: gold/ only, never shown to the agent."""

from svc.store import load, save


def test_loaded_stamp_is_timezone_aware(tmp_path):
    path = tmp_path / "stamp.json"
    save(path)
    assert load(path).tzinfo is not None


def test_round_trip_preserves_the_offset(tmp_path):
    path = tmp_path / "stamp.json"
    value = save(path)
    loaded = load(path)
    assert loaded.utcoffset() == value.utcoffset()
    assert loaded == value
