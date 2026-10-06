from app import config


def test_boot_time_is_the_unix_epoch() -> None:
    assert config.boot_time().year == 1970


def test_epoch_date() -> None:
    assert (config.EPOCH.year, config.EPOCH.month, config.EPOCH.day) == (2020, 1, 1)
