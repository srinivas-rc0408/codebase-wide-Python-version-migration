from svc.session import is_fresh
from svc.store import save


def test_fresh_save_is_fresh(tmp_path):
    path = tmp_path / "stamp.json"
    save(path)
    assert is_fresh(path, 60) is True
