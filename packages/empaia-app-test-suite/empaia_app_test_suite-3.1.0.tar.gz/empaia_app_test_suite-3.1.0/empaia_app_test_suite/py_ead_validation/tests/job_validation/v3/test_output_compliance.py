import time

import pytest

from py_ead_validation.exceptions import JobValidationError


@pytest.mark.asyncio
async def test_failed_job_raises_validation_error(job_validator, job_id, scoped_job_creator_id):
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
        "status": "ERROR",
        "created_at": "1623349180",
        "creator_type": "SCOPE",
        "creator_id": scoped_job_creator_id,
        "app_id": "a008d456-b827-4dc3-9c9f-6fcaf6d2e87e",
        "mode": "STANDALONE",
        "input_validation_status": "NONE",
        "output_validation_status": "NONE",
    }
    with pytest.raises(JobValidationError, match=f"no validation performed due to job error state"):
        await job_validator.validate_outputs(job, ead)


@pytest.mark.parametrize(
    "io_type, io_subtype",
    [
        ("annotation", "point"),
        ("annotation", "line"),
        ("annotation", "arrow"),
        ("annotation", "circle"),
        ("annotation", "rectangle"),
        ("annotation", "polygon"),
        ("primitive", "integer"),
        ("primitive", "float"),
        ("primitive", "bool"),
        ("primitive", "string"),
        ("collection", "collection"),
    ],
)
@pytest.mark.asyncio
async def test_output_not_available(job_validator, job_id, scoped_job_creator_id, io_type, io_subtype):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "io": {"test": {"type": io_subtype}},
        "modes": {"standalone": {"inputs": [], "outputs": ["test"]}},
    }
    job = {
        "id": job_id,
        "inputs": {},
        "outputs": {"test": "905b863f-2d00-436b-aafa-17de647cd0b0"},
        "status": "COMPLETED",
        "created_at": "1623349180",
        "creator_type": "SCOPE",
        "creator_id": scoped_job_creator_id,
        "app_id": "a008d456-b827-4dc3-9c9f-6fcaf6d2e87e",
        "mode": "STANDALONE",
        "input_validation_status": "NONE",
        "output_validation_status": "NONE",
    }
    with pytest.raises(JobValidationError, match=f"test of type {io_type} not available on MDS"):
        await job_validator.validate_outputs(job, ead)


@pytest.mark.parametrize(
    "io_type",
    [("line"), ("arrow"), ("circle"), ("rectangle"), ("polygon")],
)
@pytest.mark.asyncio
async def test_annotation_output_of_wrong_type(job_validator, job_id, scoped_job_creator_id, slide, point, io_type):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "io": {
            "my_wsi": {"type": "wsi"},
            "test": {"type": io_type, "reference": "io.my_wsi"},
        },
        "modes": {"standalone": {"inputs": ["my_wsi"], "outputs": ["test"]}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"]},
        "outputs": {"test": point["id"]},
        "status": "COMPLETED",
        "created_at": "1623349180",
        "creator_type": "SCOPE",
        "creator_id": scoped_job_creator_id,
        "app_id": "a008d456-b827-4dc3-9c9f-6fcaf6d2e87e",
        "mode": "STANDALONE",
        "input_validation_status": "NONE",
        "output_validation_status": "NONE",
    }
    with pytest.raises(JobValidationError, match=f"test requires type {io_type} but is point"):
        await job_validator.validate_outputs(job, ead)


@pytest.mark.asyncio
async def test_annotation_output_of_wrong_creator_id(
    job_validator, job_id, scoped_job_creator_id, slide, rectangle_wrong_creator_id
):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "io": {
            "my_wsi": {"type": "wsi"},
            "my_rectangle": {"type": "rectangle", "reference": "io.my_wsi"},
        },
        "modes": {"standalone": {"inputs": ["my_wsi"], "outputs": ["my_rectangle"]}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"]},
        "outputs": {"my_rectangle": rectangle_wrong_creator_id["id"]},
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
        JobValidationError, match=f"Creator id of my_rectangle must match job id for containerized jobs"
    ):
        await job_validator.validate_outputs(job, ead)


@pytest.mark.asyncio
async def test_annotation_output_of_wrong_creator_type(
    job_validator, job_id, scoped_job_creator_id, slide, rectangle_wrong_creator_type
):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "io": {
            "my_wsi": {"type": "wsi"},
            "my_rectangle": {"type": "rectangle", "reference": "io.my_wsi"},
        },
        "modes": {"standalone": {"inputs": ["my_wsi"], "outputs": ["my_rectangle"]}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"]},
        "outputs": {"my_rectangle": rectangle_wrong_creator_type["id"]},
        "status": "COMPLETED",
        "created_at": "1623349180",
        "creator_type": "SCOPE",
        "creator_id": scoped_job_creator_id,
        "app_id": "a008d456-b827-4dc3-9c9f-6fcaf6d2e87e",
        "mode": "STANDALONE",
        "input_validation_status": "NONE",
        "output_validation_status": "NONE",
    }
    with pytest.raises(JobValidationError, match=f"Creator type of my_rectangle must be job for containerized jobs"):
        await job_validator.validate_outputs(job, ead)


@pytest.mark.asyncio
async def test_annotation_output_of_wrong_creator_id_uncontainerized(
    job_validator, job_id, scoped_job_creator_id, slide, scoped_rectangle_wrong_creator_id
):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "io": {
            "my_wsi": {"type": "wsi"},
            "my_rectangle": {"type": "rectangle", "reference": "io.my_wsi"},
        },
        "modes": {
            "preprocessing": {"inputs": ["my_wsi"], "outputs": ["my_rectangle"]},
            "postprocessing": {"inputs": ["my_wsi"], "outputs": ["my_rectangle"], "containerized": False},
        },
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"]},
        "outputs": {"my_rectangle": scoped_rectangle_wrong_creator_id["id"]},
        "status": "COMPLETED",
        "created_at": "1623349180",
        "creator_type": "SCOPE",
        "creator_id": scoped_job_creator_id,
        "app_id": "a008d456-b827-4dc3-9c9f-6fcaf6d2e87e",
        "mode": "POSTPROCESSING",
        "containerized": False,
        "input_validation_status": "NONE",
        "output_validation_status": "NONE",
    }
    with pytest.raises(
        JobValidationError, match=f"Creator id of my_rectangle must match job creator id for uncontainerized jobs"
    ):
        await job_validator.validate_outputs(job, ead)


@pytest.mark.asyncio
async def test_annotation_output_of_wrong_creator_type_uncontainerized(
    job_validator, job_id, scoped_job_creator_id, slide, scoped_rectangle_wrong_creator_type
):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "io": {
            "my_wsi": {"type": "wsi"},
            "my_rectangle": {"type": "rectangle", "reference": "io.my_wsi"},
        },
        "modes": {
            "preprocessing": {"inputs": ["my_wsi"], "outputs": ["my_rectangle"]},
            "postprocessing": {"inputs": ["my_wsi"], "outputs": ["my_rectangle"], "containerized": False},
        },
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"]},
        "outputs": {"my_rectangle": scoped_rectangle_wrong_creator_type["id"]},
        "status": "COMPLETED",
        "created_at": "1623349180",
        "creator_type": "SCOPE",
        "creator_id": scoped_job_creator_id,
        "app_id": "a008d456-b827-4dc3-9c9f-6fcaf6d2e87e",
        "mode": "POSTPROCESSING",
        "containerized": False,
        "input_validation_status": "NONE",
        "output_validation_status": "NONE",
    }
    with pytest.raises(
        JobValidationError, match=f"Creator type of my_rectangle must be scope for uncontainerized jobs"
    ):
        await job_validator.validate_outputs(job, ead)


@pytest.mark.parametrize(
    "io_type",
    [("integer"), ("float"), ("bool")],
)
@pytest.mark.asyncio
async def test_primitive_output_of_wrong_type(job_validator, job_id, scoped_job_creator_id, slide, string, io_type):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "io": {
            "my_wsi": {"type": "wsi"},
            "test": {"type": io_type, "reference": "io.my_wsi"},
        },
        "modes": {"standalone": {"inputs": ["my_wsi"], "outputs": ["test"]}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"]},
        "outputs": {"test": string["id"]},
        "status": "COMPLETED",
        "created_at": "1623349180",
        "creator_type": "SCOPE",
        "creator_id": scoped_job_creator_id,
        "app_id": "a008d456-b827-4dc3-9c9f-6fcaf6d2e87e",
        "mode": "STANDALONE",
        "input_validation_status": "NONE",
        "output_validation_status": "NONE",
    }
    with pytest.raises(JobValidationError, match=f"test requires type {io_type} but is string"):
        await job_validator.validate_outputs(job, ead)


@pytest.mark.asyncio
async def test_annotation_output_with_wrong_reference(
    job_validator, job_id, scoped_job_creator_id, slide, point_other_slide
):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "io": {
            "my_wsi": {"type": "wsi"},
            "my_point": {"type": "point", "reference": "io.my_wsi"},
        },
        "modes": {"standalone": {"inputs": ["my_wsi"], "outputs": ["my_point"]}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"]},
        "outputs": {"my_point": point_other_slide["id"]},
        "status": "COMPLETED",
        "created_at": "1623349180",
        "creator_type": "SCOPE",
        "creator_id": scoped_job_creator_id,
        "app_id": "a008d456-b827-4dc3-9c9f-6fcaf6d2e87e",
        "mode": "STANDALONE",
        "input_validation_status": "NONE",
        "output_validation_status": "NONE",
    }
    with pytest.raises(JobValidationError, match="my_point does not reference my_wsi"):
        await job_validator.validate_outputs(job, ead)


@pytest.mark.asyncio
async def test_class_output_with_wrong_reference(
    job_validator, job_id, scoped_job_creator_id, slide, rectangle, other_rectangle_roi_klass
):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "io": {
            "my_wsi": {"type": "wsi"},
            "my_rectangle": {"type": "rectangle", "reference": "io.my_wsi"},
            "my_class": {"type": "class", "reference": "io.my_rectangle"},
        },
        "modes": {"standalone": {"inputs": ["my_wsi"], "outputs": ["my_rectangle", "my_class"]}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"]},
        "outputs": {"my_rectangle": rectangle["id"], "my_class": other_rectangle_roi_klass["id"]},
        "status": "COMPLETED",
        "created_at": "1623349180",
        "creator_type": "SCOPE",
        "creator_id": scoped_job_creator_id,
        "app_id": "a008d456-b827-4dc3-9c9f-6fcaf6d2e87e",
        "mode": "STANDALONE",
        "input_validation_status": "NONE",
        "output_validation_status": "NONE",
    }
    with pytest.raises(JobValidationError, match="my_class does not reference my_rectangle"):
        await job_validator.validate_outputs(job, ead)


@pytest.mark.asyncio
async def test_unknown_local_class_output(
    job_validator, job_id, scoped_job_creator_id, slide, rectangle, unknown_local_class
):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "io": {
            "my_wsi": {"type": "wsi"},
            "my_rectangle": {"type": "rectangle", "reference": "io.my_wsi"},
            "my_class": {"type": "class", "reference": "io.my_rectangle"},
        },
        "modes": {"standalone": {"inputs": ["my_wsi"], "outputs": ["my_rectangle", "my_class"]}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"]},
        "outputs": {"my_rectangle": rectangle["id"], "my_class": unknown_local_class["id"]},
        "status": "COMPLETED",
        "created_at": "1623349180",
        "creator_type": "SCOPE",
        "creator_id": scoped_job_creator_id,
        "app_id": "a008d456-b827-4dc3-9c9f-6fcaf6d2e87e",
        "mode": "STANDALONE",
        "input_validation_status": "NONE",
        "output_validation_status": "NONE",
    }
    with pytest.raises(JobValidationError, match="my_class class value is not known in global or local namespaces"):
        await job_validator.validate_outputs(job, ead)


@pytest.mark.asyncio
async def test_primitive_output_with_wrong_reference(
    job_validator, job_id, scoped_job_creator_id, slide, point, string_other_slide
):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "io": {
            "my_wsi": {"type": "wsi"},
            "my_point": {"type": "point", "reference": "io.my_wsi"},
            "my_primitive": {"type": "string", "reference": "io.my_wsi"},
        },
        "modes": {"standalone": {"inputs": ["my_wsi"], "outputs": ["my_point", "my_primitive"]}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"]},
        "outputs": {"my_point": point["id"], "my_primitive": string_other_slide["id"]},
        "status": "COMPLETED",
        "created_at": "1623349180",
        "creator_type": "SCOPE",
        "creator_id": scoped_job_creator_id,
        "app_id": "a008d456-b827-4dc3-9c9f-6fcaf6d2e87e",
        "mode": "STANDALONE",
        "input_validation_status": "NONE",
        "output_validation_status": "NONE",
    }
    with pytest.raises(JobValidationError, match="my_primitive does not reference my_wsi"):
        await job_validator.validate_outputs(job, ead)


@pytest.mark.asyncio
async def test_primitive_output_with_wrong_reference_type(
    job_validator, job_id, scoped_job_creator_id, slide, point, string_with_point_reference
):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "io": {
            "my_wsi": {"type": "wsi"},
            "my_point": {"type": "point", "reference": "io.my_wsi"},
            "my_primitive": {"type": "string", "reference": "io.my_wsi"},
        },
        "modes": {"standalone": {"inputs": ["my_wsi"], "outputs": ["my_point", "my_primitive"]}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"]},
        "outputs": {"my_point": point["id"], "my_primitive": string_with_point_reference["id"]},
        "status": "COMPLETED",
        "created_at": "1623349180",
        "creator_type": "SCOPE",
        "creator_id": scoped_job_creator_id,
        "app_id": "a008d456-b827-4dc3-9c9f-6fcaf6d2e87e",
        "mode": "STANDALONE",
        "input_validation_status": "NONE",
        "output_validation_status": "NONE",
    }
    with pytest.raises(JobValidationError, match="my_primitive uses wrong reference type for my_wsi"):
        await job_validator.validate_outputs(job, ead)


@pytest.mark.asyncio
async def test_collection_output_with_wrong_reference(
    job_validator, job_id, scoped_job_creator_id, slide, collection_other_slide
):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "io": {
            "my_wsi": {"type": "wsi"},
            "my_points": {"type": "collection", "items": {"type": "point", "reference": "io.my_wsi"}},
        },
        "modes": {"standalone": {"inputs": ["my_wsi"], "outputs": ["my_points"]}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"]},
        "outputs": {"my_points": collection_other_slide["id"]},
        "status": "COMPLETED",
        "created_at": "1623349180",
        "creator_type": "SCOPE",
        "creator_id": scoped_job_creator_id,
        "app_id": "a008d456-b827-4dc3-9c9f-6fcaf6d2e87e",
        "mode": "STANDALONE",
        "input_validation_status": "NONE",
        "output_validation_status": "NONE",
    }
    with pytest.raises(JobValidationError, match="my_points does not reference my_wsi"):
        await job_validator.validate_outputs(job, ead)


@pytest.mark.asyncio
async def test_collection_output_with_wrong_reference_in_item(
    job_validator, job_id, scoped_job_creator_id, slide, collection_single_item_other_slide
):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "io": {
            "my_wsi": {"type": "wsi"},
            "my_points": {"type": "collection", "items": {"type": "point", "reference": "io.my_wsi"}},
        },
        "modes": {"standalone": {"inputs": ["my_wsi"], "outputs": ["my_points"]}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"]},
        "outputs": {"my_points": collection_single_item_other_slide["id"]},
        "status": "COMPLETED",
        "created_at": "1623349180",
        "creator_type": "SCOPE",
        "creator_id": scoped_job_creator_id,
        "app_id": "a008d456-b827-4dc3-9c9f-6fcaf6d2e87e",
        "mode": "STANDALONE",
        "input_validation_status": "NONE",
        "output_validation_status": "NONE",
    }
    with pytest.raises(JobValidationError, match="my_points does not reference my_wsi"):
        await job_validator.validate_outputs(job, ead)


@pytest.mark.asyncio
async def test_collection_output_with_wrong_collection_structure(
    job_validator, job_id, scoped_job_creator_id, slide, nested_collection
):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "io": {
            "my_wsi": {"type": "wsi"},
            "my_points": {"type": "collection", "items": {"type": "point", "reference": "io.my_wsi"}},
        },
        "modes": {"standalone": {"inputs": ["my_wsi"], "outputs": ["my_points"]}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"]},
        "outputs": {"my_points": nested_collection["id"]},
        "status": "COMPLETED",
        "created_at": "1623349180",
        "creator_type": "SCOPE",
        "creator_id": scoped_job_creator_id,
        "app_id": "a008d456-b827-4dc3-9c9f-6fcaf6d2e87e",
        "mode": "STANDALONE",
        "input_validation_status": "NONE",
        "output_validation_status": "NONE",
    }
    with pytest.raises(JobValidationError, match="Collection my_points requires item type point but is collection"):
        await job_validator.validate_outputs(job, ead)


@pytest.mark.asyncio
async def test_collection_references_collection_items_valid(
    job_validator, job_id, scoped_job_creator_id, slide, rois, ints_referencing_rois
):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "io": {
            "my_wsi": {"type": "wsi"},
            "my_rectangles": {"type": "collection", "items": {"type": "rectangle", "reference": "io.my_wsi"}},
            "my_ints": {"type": "collection", "items": {"type": "integer", "reference": "io.my_rectangles.items"}},
        },
        "modes": {"standalone": {"inputs": ["my_wsi", "my_rectangles"], "outputs": ["my_ints"]}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"], "my_rectangles": rois["id"]},
        "outputs": {"my_ints": ints_referencing_rois["id"]},
        "status": "COMPLETED",
        "created_at": "1623349180",
        "creator_type": "SCOPE",
        "creator_id": scoped_job_creator_id,
        "app_id": "a008d456-b827-4dc3-9c9f-6fcaf6d2e87e",
        "mode": "STANDALONE",
        "input_validation_status": "NONE",
        "output_validation_status": "NONE",
    }
    await job_validator.validate_outputs(job, ead)


@pytest.mark.asyncio
async def test_collection_references_collection_items_large_valid(
    job_validator, job_id, scoped_job_creator_id, slide, many_polygons, classes_referencing_many_polygons
):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "classes": {"tumor": {"name": "Tumor"}, "non_tumor": {"name": "Non tumor"}},
        "io": {
            "my_wsi": {"type": "wsi"},
            "my_cells": {"type": "collection", "items": {"type": "polygon", "reference": "io.my_wsi"}},
            "my_cell_classes": {"type": "collection", "items": {"type": "class", "reference": "io.my_cells.items"}},
        },
        "modes": {"preprocessing": {"inputs": ["my_wsi"], "outputs": ["my_cells", "my_cell_classes"]}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"]},
        "outputs": {"my_cells": many_polygons["id"], "my_cell_classes": classes_referencing_many_polygons["id"]},
        "status": "COMPLETED",
        "created_at": "1623349180",
        "creator_type": "SCOPE",
        "creator_id": scoped_job_creator_id,
        "app_id": "a008d456-b827-4dc3-9c9f-6fcaf6d2e87e",
        "mode": "PREPROCESSING",
        "input_validation_status": "NONE",
        "output_validation_status": "NONE",
    }
    await job_validator.validate_outputs(job, ead)


@pytest.mark.asyncio
async def test_collection_references_collection_items_wrong_reference_id(
    job_validator, job_id, scoped_job_creator_id, slide, rois, ints_referencing_rois_wrong_reference_id
):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "io": {
            "my_wsi": {"type": "wsi"},
            "my_rectangles": {"type": "collection", "items": {"type": "rectangle", "reference": "io.my_wsi"}},
            "my_ints": {"type": "collection", "items": {"type": "integer", "reference": "io.my_rectangles.items"}},
        },
        "modes": {"standalone": {"inputs": ["my_wsi", "my_rectangles"], "outputs": ["my_ints"]}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"], "my_rectangles": rois["id"]},
        "outputs": {"my_ints": ints_referencing_rois_wrong_reference_id["id"]},
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
        JobValidationError,
        match="At least one item in my_ints does not reference any item in my_rectangles.items",
    ):
        await job_validator.validate_outputs(job, ead)


@pytest.mark.asyncio
async def test_collection_references_collection_items_wrong_reference_type(
    job_validator, job_id, scoped_job_creator_id, slide, rois, ints_referencing_rois_wrong_reference_type
):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "io": {
            "my_wsi": {"type": "wsi"},
            "my_rectangles": {"type": "collection", "items": {"type": "rectangle", "reference": "io.my_wsi"}},
            "my_ints": {"type": "collection", "items": {"type": "integer", "reference": "io.my_rectangles.items"}},
        },
        "modes": {"standalone": {"inputs": ["my_wsi", "my_rectangles"], "outputs": ["my_ints"]}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"], "my_rectangles": rois["id"]},
        "outputs": {"my_ints": ints_referencing_rois_wrong_reference_type["id"]},
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
        JobValidationError,
        match="my_ints uses wrong reference type for my_rectangles",
    ):
        await job_validator.validate_outputs(job, ead)


@pytest.mark.asyncio
async def test_nested_collection_references_collection_items_valid(
    job_validator, job_id, scoped_job_creator_id, slide, rois, ints_in_nested_collection_referencing_rois
):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "io": {
            "my_wsi": {"type": "wsi"},
            "my_rectangles": {"type": "collection", "items": {"type": "rectangle", "reference": "io.my_wsi"}},
            "my_nested_ints": {
                "type": "collection",
                "items": {"type": "collection", "items": {"type": "integer", "reference": "io.my_rectangles.items"}},
            },
        },
        "modes": {"standalone": {"inputs": ["my_wsi", "my_rectangles"], "outputs": ["my_nested_ints"]}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"], "my_rectangles": rois["id"]},
        "outputs": {"my_nested_ints": ints_in_nested_collection_referencing_rois["id"]},
        "status": "COMPLETED",
        "created_at": "1623349180",
        "creator_type": "SCOPE",
        "creator_id": scoped_job_creator_id,
        "app_id": "a008d456-b827-4dc3-9c9f-6fcaf6d2e87e",
        "mode": "STANDALONE",
        "input_validation_status": "NONE",
        "output_validation_status": "NONE",
    }
    await job_validator.validate_outputs(job, ead)


@pytest.mark.asyncio
async def test_nested_collection_references_nested_collection_items_valid(
    job_validator,
    job_id,
    scoped_job_creator_id,
    slide,
    nested_collection,
    floats_in_nested_collection_referencing_nested_points,
):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "io": {
            "my_wsi": {"type": "wsi"},
            "my_nested_points": {
                "type": "collection",
                "items": {"type": "collection", "items": {"type": "point", "reference": "io.my_wsi"}},
            },
            "my_nested_floats": {
                "type": "collection",
                "items": {
                    "type": "collection",
                    "items": {"type": "float", "reference": "io.my_nested_points.items.items"},
                },
            },
        },
        "modes": {"standalone": {"inputs": ["my_wsi", "my_nested_points"], "outputs": ["my_nested_floats"]}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"], "my_nested_points": nested_collection["id"]},
        "outputs": {"my_nested_floats": floats_in_nested_collection_referencing_nested_points["id"]},
        "status": "COMPLETED",
        "created_at": "1623349180",
        "creator_type": "SCOPE",
        "creator_id": scoped_job_creator_id,
        "app_id": "a008d456-b827-4dc3-9c9f-6fcaf6d2e87e",
        "mode": "STANDALONE",
        "input_validation_status": "NONE",
        "output_validation_status": "NONE",
    }
    await job_validator.validate_outputs(job, ead)


@pytest.mark.asyncio
async def test_nested_collection_references_nested_collection_items_wrong_reference_id(
    job_validator,
    job_id,
    scoped_job_creator_id,
    slide,
    nested_collection,
    floats_in_nested_collection_referencing_nested_points_wrong_reference_id,
):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "io": {
            "my_wsi": {"type": "wsi"},
            "my_nested_points": {
                "type": "collection",
                "items": {"type": "collection", "items": {"type": "point", "reference": "io.my_wsi"}},
            },
            "my_nested_floats": {
                "type": "collection",
                "items": {
                    "type": "collection",
                    "items": {"type": "float", "reference": "io.my_nested_points.items.items"},
                },
            },
        },
        "modes": {"standalone": {"inputs": ["my_wsi", "my_nested_points"], "outputs": ["my_nested_floats"]}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"], "my_nested_points": nested_collection["id"]},
        "outputs": {"my_nested_floats": floats_in_nested_collection_referencing_nested_points_wrong_reference_id["id"]},
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
        JobValidationError,
        match="At least one item in my_nested_floats does not reference any item in my_nested_points.items.items",
    ):
        await job_validator.validate_outputs(job, ead)


@pytest.mark.asyncio
async def test_nested_collection_references_nested_collection_items_wrong_reference_type(
    job_validator,
    job_id,
    scoped_job_creator_id,
    slide,
    nested_collection,
    floats_in_nested_collection_referencing_nested_points_wrong_reference_type,
):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "io": {
            "my_wsi": {"type": "wsi"},
            "my_nested_points": {
                "type": "collection",
                "items": {"type": "collection", "items": {"type": "point", "reference": "io.my_wsi"}},
            },
            "my_nested_floats": {
                "type": "collection",
                "items": {
                    "type": "collection",
                    "items": {"type": "float", "reference": "io.my_nested_points.items.items"},
                },
            },
        },
        "modes": {"standalone": {"inputs": ["my_wsi", "my_nested_points"], "outputs": ["my_nested_floats"]}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"], "my_nested_points": nested_collection["id"]},
        "outputs": {
            "my_nested_floats": floats_in_nested_collection_referencing_nested_points_wrong_reference_type["id"]
        },
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
        JobValidationError,
        match="my_nested_floats uses wrong reference type for my_nested_points",
    ):
        await job_validator.validate_outputs(job, ead)


@pytest.mark.asyncio
async def test_nested_collection_references_collection_items_wrong_reference_id(
    job_validator,
    job_id,
    scoped_job_creator_id,
    slide,
    rois,
    ints_in_nested_collection_referencing_rois_wrong_reference_id,
):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "io": {
            "my_wsi": {"type": "wsi"},
            "my_rectangles": {"type": "collection", "items": {"type": "rectangle", "reference": "io.my_wsi"}},
            "my_nested_ints": {
                "type": "collection",
                "items": {"type": "collection", "items": {"type": "integer", "reference": "io.my_rectangles.items"}},
            },
        },
        "modes": {"standalone": {"inputs": ["my_wsi", "my_rectangles"], "outputs": ["my_nested_ints"]}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"], "my_rectangles": rois["id"]},
        "outputs": {"my_nested_ints": ints_in_nested_collection_referencing_rois_wrong_reference_id["id"]},
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
        JobValidationError,
        match="At least one item in my_nested_ints does not reference any item in my_rectangles.items",
    ):
        await job_validator.validate_outputs(job, ead)


@pytest.mark.asyncio
async def test_nested_collection_references_collection_items_wrong_reference_type(
    job_validator,
    job_id,
    scoped_job_creator_id,
    slide,
    rois,
    ints_in_nested_collection_referencing_rois_wrong_reference_type,
):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "io": {
            "my_wsi": {"type": "wsi"},
            "my_rectangles": {"type": "collection", "items": {"type": "rectangle", "reference": "io.my_wsi"}},
            "my_nested_ints": {
                "type": "collection",
                "items": {"type": "collection", "items": {"type": "integer", "reference": "io.my_rectangles.items"}},
            },
        },
        "modes": {"standalone": {"inputs": ["my_wsi", "my_rectangles"], "outputs": ["my_nested_ints"]}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"], "my_rectangles": rois["id"]},
        "outputs": {"my_nested_ints": ints_in_nested_collection_referencing_rois_wrong_reference_type["id"]},
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
        JobValidationError,
        match="my_nested_ints uses wrong reference type for my_rectangles",
    ):
        await job_validator.validate_outputs(job, ead)


@pytest.mark.asyncio
async def test_nested_collection_references_nested_collection_large(
    job_validator,
    job_id,
    scoped_job_creator_id,
    slide,
    nested_collection_large,
    floats_in_nested_collection_referencing_nested_points_large,
):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "io": {
            "my_wsi": {"type": "wsi"},
            "my_nested_points": {
                "type": "collection",
                "items": {"type": "collection", "items": {"type": "point", "reference": "io.my_wsi"}},
            },
            "my_nested_floats": {
                "type": "collection",
                "items": {
                    "type": "collection",
                    "items": {"type": "float", "reference": "io.my_nested_points.items.items"},
                },
            },
        },
        "modes": {"standalone": {"inputs": ["my_wsi", "my_nested_points"], "outputs": ["my_nested_floats"]}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"], "my_nested_points": nested_collection_large["id"]},
        "outputs": {"my_nested_floats": floats_in_nested_collection_referencing_nested_points_large["id"]},
        "status": "COMPLETED",
        "created_at": "1623349180",
        "creator_type": "SCOPE",
        "creator_id": scoped_job_creator_id,
        "app_id": "a008d456-b827-4dc3-9c9f-6fcaf6d2e87e",
        "mode": "STANDALONE",
        "input_validation_status": "NONE",
        "output_validation_status": "NONE",
    }
    await job_validator.validate_outputs(job, ead)


@pytest.mark.asyncio
async def test_valid_job(job_validator, job_id, scoped_job_creator_id, slide, roi_rectangle, collection):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "io": {
            "my_wsi": {"type": "wsi"},
            "my_rectangle": {
                "type": "rectangle",
                "reference": "io.my_wsi",
            },
            "my_collection": {
                "type": "collection",
                "items": {
                    "type": "point",
                    "reference": "io.my_wsi",
                },
            },
        },
        "modes": {"standalone": {"inputs": ["my_wsi"], "outputs": ["my_rectangle", "my_collection"]}},
    }
    job = {
        "id": job_id,
        "inputs": {
            "my_wsi": slide["id"],
        },
        "outputs": {
            "my_rectangle": roi_rectangle["id"],
            "my_collection": collection["id"],
        },
        "status": "COMPLETED",
        "created_at": "1623349180",
        "creator_type": "SCOPE",
        "creator_id": scoped_job_creator_id,
        "app_id": "a008d456-b827-4dc3-9c9f-6fcaf6d2e87e",
        "mode": "STANDALONE",
        "input_validation_status": "NONE",
        "output_validation_status": "NONE",
    }
    await job_validator.validate_inputs(job, ead)
