import pytest

from py_ead_validation.exceptions import JobValidationError, JobValidationPreconditionError


@pytest.mark.parametrize(
    "job_status",
    [("NONE"), ("ASSEMBLY"), ("READY"), ("SCHEDULED"), ("RUNNING"), ("COMPLETED"), ("ERROR")],
)
@pytest.mark.asyncio
async def test_validate_inputs_requires_at_least_ready(job_validator, job_id, scoped_job_creator_id, job_status):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "io": {},
        "modes": {"standalone": {"inputs": [], "outputs": []}},
    }
    job = {
        "id": job_id,
        "inputs": {},
        "outputs": {},
        "status": job_status,
        "created_at": "1623349180",
        "creator_type": "SCOPE",
        "creator_id": scoped_job_creator_id,
        "app_id": "a008d456-b827-4dc3-9c9f-6fcaf6d2e87e",
        "mode": "STANDALONE",
        "input_validation_status": "NONE",
        "output_validation_status": "NONE",
    }
    if job_status in ["NONE", "ASSEMBLY"]:
        with pytest.raises(JobValidationPreconditionError, match="Input validation requires at least READY status"):
            await job_validator.validate_inputs(job, ead)
    else:
        await job_validator.validate_inputs(job, ead)


@pytest.mark.parametrize(
    "job_status",
    [("NONE"), ("ASSEMBLY"), ("READY"), ("SCHEDULED"), ("RUNNING"), ("COMPLETED"), ("ERROR")],
)
@pytest.mark.asyncio
async def test_validate_outputs_requires_completed_status(job_validator, job_id, scoped_job_creator_id, job_status):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "io": {},
        "modes": {"standalone": {"inputs": [], "outputs": []}},
    }
    job = {
        "id": job_id,
        "inputs": {},
        "outputs": {},
        "status": job_status,
        "created_at": "1623349180",
        "creator_type": "SCOPE",
        "creator_id": scoped_job_creator_id,
        "app_id": "a008d456-b827-4dc3-9c9f-6fcaf6d2e87e",
        "mode": "STANDALONE",
        "input_validation_status": "NONE",
        "output_validation_status": "NONE",
    }
    if job_status in ["NONE", "ASSEMBLY", "READY", "SCHEDULED", "RUNNING"]:
        with pytest.raises(JobValidationPreconditionError, match="Output validation requires a terminal status"):
            await job_validator.validate_outputs(job, ead)
    elif job_status == "ERROR":
        with pytest.raises(JobValidationError, match="no validation performed due to job error state"):
            await job_validator.validate_outputs(job, ead)
    else:  # COMPLETED
        await job_validator.validate_outputs(job, ead)
