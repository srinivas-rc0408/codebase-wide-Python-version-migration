from svc.store import load, save


def test_round_trip_is_equal(tmp_path):
    path = tmp_path / "stamp.json"
    value = save(path)
    assert load(path) == value
