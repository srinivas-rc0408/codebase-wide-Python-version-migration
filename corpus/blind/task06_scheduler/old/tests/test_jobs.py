from app import jobs, scheduler


def test_past_job_is_due() -> None:
    assert jobs.due(scheduler.make_job(-60))


def test_future_job_is_not_due() -> None:
    assert not jobs.due(jobs.schedule(3600))
