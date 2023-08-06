from uuid import uuid4

import pytest
from pydantic import ValidationError

from ..job import JobQuery, PostJob


def test_default_job_mode_is_standalone():
    job = PostJob(app_id=uuid4(), creator_id="uid", creator_type="SCOPE")
    assert job.mode == "STANDALONE"


def test_valid_job_modes():
    job = PostJob(app_id=uuid4(), creator_id="uid", creator_type="SCOPE", mode="STANDALONE")
    assert job.mode == "STANDALONE"
    job = PostJob(app_id=uuid4(), creator_id="uid", creator_type="SERVICE", mode="PREPROCESSING")
    assert job.mode == "PREPROCESSING"
    job = PostJob(app_id=uuid4(), creator_id="uid", creator_type="SCOPE", mode="POSTPROCESSING")
    assert job.mode == "POSTPROCESSING"


def test_preprocessing_jobs_must_have_service_creator_type():
    with pytest.raises(ValidationError):
        PostJob(app_id=uuid4(), creator_id="uid", creator_type="SCOPE", mode="PREPROCESSING")
    with pytest.raises(ValidationError):
        PostJob(app_id=uuid4(), creator_id="uid", creator_type="USER", mode="PREPROCESSING")


def test_nonpreprocessing_jobs_must_not_have_service_creator_type():
    with pytest.raises(ValidationError):
        PostJob(app_id=uuid4(), creator_id="uid", creator_type="SERVICE", mode="STANDALONE")
    with pytest.raises(ValidationError):
        PostJob(app_id=uuid4(), creator_id="uid", creator_type="SERVICE", mode="POSTPROCESSING")


def test_default_jobs_are_containerized():
    job = PostJob(app_id=uuid4(), creator_id="uid", creator_type="SCOPE")
    assert job.containerized


def test_standalone_jobs_cant_be_uncontainerized():
    with pytest.raises(ValidationError):
        PostJob(app_id=uuid4(), creator_id="uid", creator_type="SCOPE", mode="STANDALONE", containerized=False)


def test_preprocessing_jobs_cant_be_uncontainerized():
    with pytest.raises(ValidationError):
        PostJob(app_id=uuid4(), creator_id="uid", creator_type="SCOPE", mode="PREPROCESSING", containerized=False)


def test_postprocessing_jobs_can_be_containerized_or_not():
    job = PostJob(app_id=uuid4(), creator_id="uid", creator_type="SCOPE", mode="POSTPROCESSING", containerized=False)
    assert job.mode == "POSTPROCESSING" and not job.containerized
    job = PostJob(app_id=uuid4(), creator_id="uid", creator_type="SCOPE", mode="POSTPROCESSING", containerized=True)
    assert job.mode == "POSTPROCESSING" and job.containerized
    job = PostJob(app_id=uuid4(), creator_id="uid", creator_type="SCOPE", mode="POSTPROCESSING")
    assert job.mode == "POSTPROCESSING" and job.containerized


def test_query_accepts_optional_but_valid_modes():
    query = JobQuery()
    assert query.modes is None
    with pytest.raises(ValidationError):
        JobQuery(modes=[])
    query = JobQuery(modes=["PREPROCESSING", "POSTPROCESSING"])
    assert query.modes == ["PREPROCESSING", "POSTPROCESSING"]
