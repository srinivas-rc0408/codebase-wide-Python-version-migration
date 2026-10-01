from pkg.core import job


def test_job() -> None:
    assert job() == 1 and job.when.year >= 2020
