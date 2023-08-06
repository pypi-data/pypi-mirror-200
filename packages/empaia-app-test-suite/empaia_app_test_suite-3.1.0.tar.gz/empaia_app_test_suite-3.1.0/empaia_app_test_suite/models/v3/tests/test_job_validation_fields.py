import uuid

from ..job import Job, JobQuery, JobValidationStatus, PutJobValidationStatus


def test_default_job_validation_field_values():
    job = Job(
        id=uuid.uuid4(),
        app_id=uuid.uuid4(),
        creator_id="uid",
        creator_type="SCOPE",
        inputs={},
        outputs={},
        status="ASSEMBLY",
        created_at=0,
    )
    assert job.input_validation_status == JobValidationStatus.NONE
    assert job.output_validation_status == JobValidationStatus.NONE
    assert not job.input_validation_error_message
    assert not job.output_validation_error_message


def test_explicit_job_validation_field_values():
    job = Job(
        id=uuid.uuid4(),
        app_id=uuid.uuid4(),
        creator_id="uid",
        creator_type="SCOPE",
        inputs={},
        outputs={},
        status="ASSEMBLY",
        created_at=0,
        input_validation_status=JobValidationStatus.ERROR,
        input_validation_error_message="input id not found",
        output_validation_status=JobValidationStatus.ERROR,
        output_validation_error_message="output id not found",
    )
    assert job.input_validation_status == JobValidationStatus.ERROR
    assert job.output_validation_status == JobValidationStatus.ERROR
    assert job.input_validation_error_message == "input id not found"
    assert job.output_validation_error_message == "output id not found"


def test_put_job_validation_status_model():
    validation_status_update = PutJobValidationStatus(
        validation_status=JobValidationStatus.ERROR, error_message="Something went wrong"
    )
    assert validation_status_update.validation_status == JobValidationStatus.ERROR
    assert validation_status_update.error_message == "Something went wrong"

    validation_status_update = PutJobValidationStatus(validation_status=JobValidationStatus.COMPLETED)
    assert validation_status_update.validation_status == JobValidationStatus.COMPLETED
    assert not validation_status_update.error_message


def test_query_supports_validation_statuses():
    query = JobQuery(
        input_validation_statuses=[JobValidationStatus.NONE], output_validation_statuses=[JobValidationStatus.NONE]
    )
    assert query.input_validation_statuses == [JobValidationStatus.NONE]
    assert query.input_validation_statuses == [JobValidationStatus.NONE]
    query = JobQuery()
    assert not query.input_validation_statuses
    assert not query.output_validation_statuses
