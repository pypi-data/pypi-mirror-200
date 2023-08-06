import pytest

from py_ead_validation.exceptions import JobValidationError


@pytest.mark.asyncio
async def test_missing_inputs(job_validator, job_id, scoped_job_creator_id):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "io": {"my_wsi": {"type": "wsi"}},
        "modes": {"standalone": {"inputs": ["my_wsi"], "outputs": []}},
    }
    job = {
        "id": job_id,
        "inputs": {},
        "outputs": {},
        "status": "READY",
        "created_at": "1623349180",
        "creator_type": "SCOPE",
        "creator_id": scoped_job_creator_id,
        "app_id": "a008d456-b827-4dc3-9c9f-6fcaf6d2e87e",
        "mode": "STANDALONE",
        "input_validation_status": "NONE",
        "output_validation_status": "NONE",
    }
    with pytest.raises(JobValidationError, match="Missing input my_wsi in job"):
        await job_validator.validate_inputs(job, ead)


@pytest.mark.asyncio
async def test_additional_inputs(job_validator, job_id, scoped_job_creator_id):
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
        "inputs": {"my_wsi": "some-proprietary-id"},
        "outputs": {},
        "status": "READY",
        "created_at": "1623349180",
        "creator_type": "SCOPE",
        "creator_id": scoped_job_creator_id,
        "app_id": "a008d456-b827-4dc3-9c9f-6fcaf6d2e87e",
        "mode": "STANDALONE",
        "input_validation_status": "NONE",
        "output_validation_status": "NONE",
    }
    with pytest.raises(JobValidationError, match="my_wsi not defined as input in EAD in standalone mode"):
        await job_validator.validate_inputs(job, ead)
