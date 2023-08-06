import pytest

from py_ead_validation.exceptions import JobValidationError


@pytest.mark.parametrize(
    "io_type, io_subtype",
    [
        ("wsi", "wsi"),
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
        ("class", "class"),
        ("collection", "collection"),
    ],
)
@pytest.mark.asyncio
async def test_input_not_available(job_validator, job_id, scoped_job_creator_id, io_type, io_subtype):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "io": {"test": {"type": io_subtype}},
        "modes": {"standalone": {"inputs": ["test"], "outputs": []}},
    }
    job = {
        "id": job_id,
        "inputs": {"test": "905b863f-2d00-436b-aafa-17de647cd0b0"},
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
    with pytest.raises(JobValidationError, match=f"test of type {io_type} not available on MDS"):
        await job_validator.validate_inputs(job, ead)


@pytest.mark.parametrize(
    "io_type",
    [("line"), ("arrow"), ("circle"), ("rectangle"), ("polygon")],
)
@pytest.mark.asyncio
async def test_annotation_input_of_wrong_type(job_validator, job_id, scoped_job_creator_id, slide, point, io_type):
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
        "modes": {"standalone": {"inputs": ["my_wsi", "test"], "outputs": []}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"], "test": point["id"]},
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
    with pytest.raises(JobValidationError, match=f"test requires type {io_type} but is point"):
        await job_validator.validate_inputs(job, ead)


@pytest.mark.parametrize(
    "io_type",
    [("integer"), ("float"), ("bool")],
)
@pytest.mark.asyncio
async def test_primitive_input_of_wrong_type(job_validator, job_id, scoped_job_creator_id, slide, string, io_type):
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
        "modes": {"standalone": {"inputs": ["my_wsi", "test"], "outputs": []}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"], "test": string["id"]},
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
    with pytest.raises(JobValidationError, match=f"test requires type {io_type} but is string"):
        await job_validator.validate_inputs(job, ead)


@pytest.mark.asyncio
async def test_annotation_input_with_unmatched_class_constraints(
    job_validator, job_id, scoped_job_creator_id, slide, rectangle
):
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
                "classes": ["org.empaia.global.v1.classes.roi"],
            },
        },
        "modes": {"standalone": {"inputs": ["my_wsi", "my_rectangle"], "outputs": []}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"], "my_rectangle": rectangle["id"]},
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
    with pytest.raises(
        JobValidationError,
        match="my_rectangle has unmatched class constraints: org.empaia.global.v1.classes.roi",
    ):
        await job_validator.validate_inputs(job, ead)


@pytest.mark.asyncio
async def test_annotation_input_with_matched_class_constraint(
    job_validator, job_id, scoped_job_creator_id, slide, roi_rectangle
):
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
                "classes": ["org.empaia.global.v1.classes.roi"],
            },
        },
        "modes": {"standalone": {"inputs": ["my_wsi", "my_rectangle"], "outputs": []}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"], "my_rectangle": roi_rectangle["id"]},
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
    await job_validator.validate_inputs(job, ead)


@pytest.mark.asyncio
async def test_annotation_input_with_matched_local_root_class_constraint(
    job_validator, job_id, scoped_job_creator_id, slide, foo_bar_baz_rectangle
):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "classes": {
            "foo": {
                "bar": {
                    "baz": {"name": "FooBarBaz"},
                },
            },
        },
        "io": {
            "my_wsi": {"type": "wsi"},
            "my_rectangle": {
                "type": "rectangle",
                "reference": "io.my_wsi",
                "classes": ["org.empaia.vendor_name.ta.v3.0.classes"],
            },
        },
        "modes": {"standalone": {"inputs": ["my_wsi", "my_rectangle"], "outputs": []}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"], "my_rectangle": foo_bar_baz_rectangle["id"]},
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
    await job_validator.validate_inputs(job, ead)


@pytest.mark.asyncio
async def test_annotation_input_with_matched_local_non_leaf_class_constraint(
    job_validator, job_id, scoped_job_creator_id, slide, foo_bar_baz_rectangle
):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "classes": {
            "foo": {
                "bar": {
                    "baz": {"name": "FooBarBaz"},
                },
            },
        },
        "io": {
            "my_wsi": {"type": "wsi"},
            "my_rectangle": {
                "type": "rectangle",
                "reference": "io.my_wsi",
                "classes": ["org.empaia.vendor_name.ta.v3.0.classes.foo.bar"],
            },
        },
        "modes": {"standalone": {"inputs": ["my_wsi", "my_rectangle"], "outputs": []}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"], "my_rectangle": foo_bar_baz_rectangle["id"]},
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
    await job_validator.validate_inputs(job, ead)


@pytest.mark.asyncio
async def test_annotation_input_with_matched_local_non_leaf_class_constraint_wrong_class_1(
    job_validator, job_id, scoped_job_creator_id, slide, foo_bar_unknown_rectangle
):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "classes": {
            "foo": {
                "bar": {
                    "baz": {"name": "FooBarBaz"},
                },
            },
        },
        "io": {
            "my_wsi": {"type": "wsi"},
            "my_rectangle": {
                "type": "rectangle",
                "reference": "io.my_wsi",
                "classes": ["org.empaia.vendor_name.ta.v3.0.classes.foo.bar"],
            },
        },
        "modes": {"standalone": {"inputs": ["my_wsi", "my_rectangle"], "outputs": []}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"], "my_rectangle": foo_bar_unknown_rectangle["id"]},
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
    with pytest.raises(
        JobValidationError,
        match="my_rectangle has unmatched class constraint: org.empaia.vendor_name.ta.v3.0.classes.foo.bar",
    ):
        await job_validator.validate_inputs(job, ead)


@pytest.mark.asyncio
async def test_annotation_input_with_matched_local_non_leaf_class_constraint_wrong_class_2(
    job_validator, job_id, scoped_job_creator_id, slide, unknown_bar_baz_rectangle
):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "classes": {
            "foo": {
                "bar": {
                    "baz": {"name": "FooBarBaz"},
                },
            },
        },
        "io": {
            "my_wsi": {"type": "wsi"},
            "my_rectangle": {
                "type": "rectangle",
                "reference": "io.my_wsi",
                "classes": ["org.empaia.vendor_name.ta.v3.0.classes.foo.bar"],
            },
        },
        "modes": {"standalone": {"inputs": ["my_wsi", "my_rectangle"], "outputs": []}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"], "my_rectangle": unknown_bar_baz_rectangle["id"]},
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
    with pytest.raises(
        JobValidationError,
        match="my_rectangle has unmatched class constraints: org.empaia.vendor_name.ta.v3.0.classes.foo.bar",
    ):
        await job_validator.validate_inputs(job, ead)


@pytest.mark.asyncio
async def test_annotation_input_with_matched_local_non_leaf_class_constraint_two_classes(
    job_validator, job_id, scoped_job_creator_id, slide, foo_bar_baz_rectangle
):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "classes": {
            "foo": {
                "bar": {
                    "baz": {"name": "FooBarBaz"},
                },
            },
        },
        "io": {
            "my_wsi": {"type": "wsi"},
            "my_rectangle": {
                "type": "rectangle",
                "reference": "io.my_wsi",
                "classes": ["org.empaia.global.v1.classes.roi", "org.empaia.vendor_name.ta.v3.0.classes.foo.bar"],
            },
        },
        "modes": {"standalone": {"inputs": ["my_wsi", "my_rectangle"], "outputs": []}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"], "my_rectangle": foo_bar_baz_rectangle["id"]},
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
    await job_validator.validate_inputs(job, ead)


@pytest.mark.asyncio
async def test_annotation_input_with_matched_local_non_leaf_class_constraint_two_classes_wrong_class(
    job_validator, job_id, scoped_job_creator_id, slide, foo_bar_baz_rectangle
):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "classes": {
            "sub": {
                "sub": {
                    "sub": {"name": "sub"},
                },
            },
        },
        "io": {
            "my_wsi": {"type": "wsi"},
            "my_rectangle": {
                "type": "rectangle",
                "reference": "io.my_wsi",
                "classes": ["org.empaia.global.v1.classes.roi", "org.empaia.vendor_name.ta.v3.0.classes.sub.sub"],
            },
        },
        "modes": {"standalone": {"inputs": ["my_wsi", "my_rectangle"], "outputs": []}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"], "my_rectangle": foo_bar_baz_rectangle["id"]},
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
    classes = ead["io"]["my_rectangle"]["classes"]
    with pytest.raises(
        JobValidationError,
        match=f"my_rectangle has unmatched class constraints: {classes[0]} or {classes[1]}",
    ):
        await job_validator.validate_inputs(job, ead)


@pytest.mark.asyncio
async def test_annotation_input_with_wrong_reference(
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
        "modes": {"standalone": {"inputs": ["my_wsi", "my_point"], "outputs": []}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"], "my_point": point_other_slide["id"]},
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
    with pytest.raises(JobValidationError, match="my_point does not reference my_wsi"):
        await job_validator.validate_inputs(job, ead)


@pytest.mark.asyncio
async def test_class_input_with_wrong_reference(
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
        "modes": {"standalone": {"inputs": ["my_wsi", "my_rectangle", "my_class"], "outputs": []}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"], "my_rectangle": rectangle["id"], "my_class": other_rectangle_roi_klass["id"]},
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
    with pytest.raises(JobValidationError, match="my_class does not reference my_rectangle"):
        await job_validator.validate_inputs(job, ead)


@pytest.mark.asyncio
async def test_unknown_local_class_input(
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
        "modes": {"standalone": {"inputs": ["my_wsi", "my_rectangle", "my_class"], "outputs": []}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"], "my_rectangle": rectangle["id"], "my_class": unknown_local_class["id"]},
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
    with pytest.raises(JobValidationError, match="my_class class value is not known in global or local namespaces"):
        await job_validator.validate_inputs(job, ead)


@pytest.mark.asyncio
async def test_unknown_nested_local_class_input(
    job_validator, job_id, scoped_job_creator_id, slide, rectangle, foo_bar_invalid_class
):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "classes": {
            "foo": {
                "bar": {
                    "baz": {"name": "FooBarBaz"},
                },
            },
        },
        "io": {
            "my_wsi": {"type": "wsi"},
            "my_rectangle": {"type": "rectangle", "reference": "io.my_wsi"},
            "my_class": {"type": "class", "reference": "io.my_rectangle"},
        },
        "modes": {"standalone": {"inputs": ["my_wsi", "my_rectangle", "my_class"], "outputs": []}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"], "my_rectangle": rectangle["id"], "my_class": foo_bar_invalid_class["id"]},
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
    with pytest.raises(JobValidationError, match="my_class class value is not known in global or local namespaces"):
        await job_validator.validate_inputs(job, ead)


@pytest.mark.asyncio
async def test_known_nested_local_class_input(
    job_validator, job_id, scoped_job_creator_id, slide, rectangle, foo_bar_baz_class
):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "classes": {
            "foo": {
                "bar": {
                    "baz": {"name": "FooBarBaz"},
                },
            },
        },
        "io": {
            "my_wsi": {"type": "wsi"},
            "my_rectangle": {"type": "rectangle", "reference": "io.my_wsi"},
            "my_class": {"type": "class", "reference": "io.my_rectangle"},
        },
        "modes": {"standalone": {"inputs": ["my_wsi", "my_rectangle", "my_class"], "outputs": []}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"], "my_rectangle": rectangle["id"], "my_class": foo_bar_baz_class["id"]},
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
    await job_validator.validate_inputs(job, ead)


@pytest.mark.asyncio
async def test_primitive_input_with_wrong_reference(
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
        "modes": {"standalone": {"inputs": ["my_wsi", "my_point", "my_primitive"], "outputs": []}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"], "my_point": point["id"], "my_primitive": string_other_slide["id"]},
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
    with pytest.raises(JobValidationError, match="my_primitive does not reference my_wsi"):
        await job_validator.validate_inputs(job, ead)


@pytest.mark.asyncio
async def test_primitive_input_with_wrong_reference_type(
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
        "modes": {"standalone": {"inputs": ["my_wsi", "my_point", "my_primitive"], "outputs": []}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"], "my_point": point["id"], "my_primitive": string_with_point_reference["id"]},
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
    with pytest.raises(JobValidationError, match="my_primitive uses wrong reference type for my_wsi"):
        await job_validator.validate_inputs(job, ead)


@pytest.mark.asyncio
async def test_collection_input_with_wrong_reference(
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
        "modes": {"standalone": {"inputs": ["my_wsi", "my_points"], "outputs": []}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"], "my_points": collection_other_slide["id"]},
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
    with pytest.raises(JobValidationError, match="my_points does not reference my_wsi"):
        await job_validator.validate_inputs(job, ead)


@pytest.mark.asyncio
async def test_collection_input_with_wrong_reference_in_item(
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
        "modes": {"standalone": {"inputs": ["my_wsi", "my_points"], "outputs": []}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"], "my_points": collection_single_item_other_slide["id"]},
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
    with pytest.raises(JobValidationError, match="my_points does not reference my_wsi"):
        await job_validator.validate_inputs(job, ead)


@pytest.mark.asyncio
async def test_collection_input_with_wrong_collection_structure(
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
        "modes": {"standalone": {"inputs": ["my_wsi", "my_points"], "outputs": []}},
    }
    job = {
        "id": job_id,
        "inputs": {"my_wsi": slide["id"], "my_points": nested_collection["id"]},
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
    with pytest.raises(JobValidationError, match="Collection my_points requires item type point but is collection"):
        await job_validator.validate_inputs(job, ead)


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
                "classes": ["org.empaia.global.v1.classes.roi"],
            },
            "my_collection": {
                "type": "collection",
                "items": {
                    "type": "point",
                    "reference": "io.my_wsi",
                },
            },
        },
        "modes": {"standalone": {"inputs": ["my_wsi", "my_rectangle", "my_collection"], "outputs": []}},
    }
    job = {
        "id": job_id,
        "inputs": {
            "my_wsi": slide["id"],
            "my_rectangle": roi_rectangle["id"],
            "my_collection": collection["id"],
        },
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
    await job_validator.validate_inputs(job, ead)


@pytest.mark.asyncio
async def test_valid_job_reference_into_slide_collection(
    job_validator, job_id, scoped_job_creator_id, slide_collection, nested_point_collection_referencing_slides
):
    ead = {
        "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
        "name": "Test App",
        "name_short": "TestApp",
        "namespace": "org.empaia.vendor_name.ta.v3.0",
        "description": "EAD for testing purposes",
        "io": {
            "my_wsis": {"type": "collection", "items": {"type": "wsi"}},
            "my_points": {
                "type": "collection",
                "items": {
                    "type": "collection",
                    "reference": "io.my_wsis.items",
                    "items": {"type": "point", "reference": "io.my_wsis.items"},
                },
            },
        },
        "modes": {"standalone": {"inputs": ["my_wsis", "my_points"], "outputs": []}},
    }
    job = {
        "id": job_id,
        "inputs": {
            "my_wsis": slide_collection["id"],
            "my_points": nested_point_collection_referencing_slides["id"],
        },
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
    await job_validator.validate_inputs(job, ead)
