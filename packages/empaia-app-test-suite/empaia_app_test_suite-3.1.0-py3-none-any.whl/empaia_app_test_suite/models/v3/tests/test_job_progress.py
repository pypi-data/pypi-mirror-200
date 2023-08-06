from uuid import uuid4

import pytest
from pydantic import ValidationError

from ..job import Job, PutJobProgress


def test_default_job_has_no_progress():
    job = Job(
        id=uuid4(),
        app_id=uuid4(),
        creator_id="uid",
        creator_type="SCOPE",
        inputs={},
        outputs={},
        status="RUNNING",
        created_at=0,
    )
    assert job.progress is None


def test_job_cant_have_negative_progress():
    with pytest.raises(ValidationError):
        Job(
            id=uuid4(),
            app_id=uuid4(),
            creator_id="uid",
            creator_type="SCOPE",
            inputs={},
            outputs={},
            status="RUNNING",
            created_at=0,
            progress=-1.0,
        )


def test_job_cant_have_progress_greater_1():
    with pytest.raises(ValidationError):
        Job(
            id=uuid4(),
            app_id=uuid4(),
            creator_id="uid",
            creator_type="SCOPE",
            inputs={},
            outputs={},
            status="RUNNING",
            created_at=0,
            progress=1.2,
        )


def test_job_can_have_progress_between_0_and_1():
    job = Job(
        id=uuid4(),
        app_id=uuid4(),
        creator_id="uid",
        creator_type="SCOPE",
        inputs={},
        outputs={},
        status="RUNNING",
        created_at=0,
        progress=0.33,
    )
    assert job.progress == pytest.approx(0.33)


def test_put_job_progress_requires_field_between_0_and_1():
    with pytest.raises(ValidationError):
        PutJobProgress()
    with pytest.raises(ValidationError):
        PutJobProgress(progress=-0.5)
    with pytest.raises(ValidationError):
        PutJobProgress(progress=1.2)
    update = PutJobProgress(progress=0.75)
    assert update.progress == pytest.approx(0.75)
