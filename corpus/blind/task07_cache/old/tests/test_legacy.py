from svc import legacy


def test_decoy_method_is_unchanged():
    assert legacy.legacy_now() == 42
    assert legacy.LegacyClock(7).utcnow() == 7


def test_decoy_docstring_is_unchanged():
    assert "datetime.utcnow()" in legacy.__doc__
