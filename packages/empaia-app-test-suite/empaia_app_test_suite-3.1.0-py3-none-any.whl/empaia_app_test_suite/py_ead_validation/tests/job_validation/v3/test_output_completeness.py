import pytest

from py_ead_validation.exceptions import JobValidationError


@pytest.mark.asyncio
async def test_missing_outputs(job_validator, job_id, scoped_job_creator_id, slide):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "io": {
            "my_wsi": {"type": "wsi"},
            "my_point": {"type": "point"},
        },
        "modes": {"standalone": {"inputs": ["my_wsi"], "outputs": ["my_point"]}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"]},
        "outputs": {},
        "status": "COMPLETED",
        "created_at": "1623349180",
        "creator_type": "SCOPE",
        "creator_id": scoped_job_creator_id,
        "app_id": "a008d456-b827-4dc3-9c9f-6fcaf6d2e87e",
        "mode": "STANDALONE",
        "input_validation_status": "NONE",
        "output_validation_status": "NONE",
    }
    with pytest.raises(JobValidationError, match="Missing output my_point in job"):
        await job_validator.validate_outputs(job, ead)


@pytest.mark.asyncio
async def test_additional_outputs(job_validator, job_id, scoped_job_creator_id, point):
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
        "outputs": {"something_additional": point["id"]},
        "status": "COMPLETED",
        "created_at": "1623349180",
        "creator_type": "SCOPE",
        "creator_id": scoped_job_creator_id,
        "app_id": "a008d456-b827-4dc3-9c9f-6fcaf6d2e87e",
        "mode": "STANDALONE",
        "input_validation_status": "NONE",
        "output_validation_status": "NONE",
    }
    with pytest.raises(
        JobValidationError, match="something_additional not defined as output in EAD in standalone mode"
    ):
        await job_validator.validate_outputs(job, ead)
