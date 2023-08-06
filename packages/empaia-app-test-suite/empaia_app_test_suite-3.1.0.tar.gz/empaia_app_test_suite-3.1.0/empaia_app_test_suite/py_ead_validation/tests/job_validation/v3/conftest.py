import asyncio
import random
import uuid

import fastapi
import pytest
import pytest_asyncio

from py_ead_validation.job_validator import JobValidator

from ..empaia_sender_auth import AioHttpClient

MDS_URL = "http://127.0.0.1:5000"


@pytest.fixture
def http_client():
    client = AioHttpClient()
    asyncio.run(client.update_token_routine())
    return client


@pytest.fixture
def job_validator(http_client):
    return JobValidator(MDS_URL, http_client)


@pytest.fixture
def job_id():
    return "a10648a7-340d-43fc-a2d9-4d91cc86f33f"


@pytest.fixture
def scoped_job_creator_id():
    return "cbca27a7-51f4-4257-be73-ea4cc829d697"


@pytest_asyncio.fixture
async def case(http_client):
    payload = {"creator_id": str(uuid.uuid4()), "creator_type": "USER"}
    return await http_client.post(f"{MDS_URL}/private/v1/cases", json=payload)


@pytest_asyncio.fixture
async def slide(http_client, case):
    payload = {"case_id": case["id"]}
    return await http_client.post(f"{MDS_URL}/private/v1/slides", json=payload)


@pytest_asyncio.fixture
async def other_slide(http_client, case):
    payload = {"case_id": case["id"]}
    return await http_client.post(f"{MDS_URL}/private/v1/slides", json=payload)


@pytest_asyncio.fixture
async def slide_collection(http_client, job_id, slide, other_slide):
    payload = {
        "name": "my_wsis",
        "type": "collection",
        "creator_id": job_id,
        "creator_type": "job",
        "item_type": "wsi",
        "items": [
            {
                "id": slide["id"],
                "type": "wsi",
            },
            {
                "id": other_slide["id"],
                "type": "wsi",
            },
        ],
    }
    collection = await http_client.post(f"{MDS_URL}/v3/collections", json=payload)
    return collection


@pytest_asyncio.fixture
async def nested_point_collection_referencing_slides(http_client, job_id, slide, other_slide):
    payload = {
        "name": "my_points",
        "type": "collection",
        "creator_id": job_id,
        "creator_type": "job",
        "item_type": "collection",
        "items": [
            {
                "name": "my_points_0",
                "type": "collection",
                "creator_id": job_id,
                "creator_type": "job",
                "reference_type": "wsi",
                "reference_id": slide["id"],
                "item_type": "point",
                "items": [
                    {
                        "name": "my_point_0_0",
                        "type": "point",
                        "creator_id": job_id,
                        "creator_type": "job",
                        "coordinates": [100, 200],
                        "reference_type": "wsi",
                        "reference_id": slide["id"],
                        "npp_created": 499,
                    },
                    {
                        "name": "my_point_0_1",
                        "type": "point",
                        "creator_id": job_id,
                        "creator_type": "job",
                        "coordinates": [100, 200],
                        "reference_type": "wsi",
                        "reference_id": slide["id"],
                        "npp_created": 499,
                    },
                ],
            },
            {
                "name": "my_points_1",
                "type": "collection",
                "creator_id": job_id,
                "creator_type": "job",
                "reference_type": "wsi",
                "reference_id": other_slide["id"],
                "item_type": "point",
                "items": [
                    {
                        "name": "my_point_1_0",
                        "type": "point",
                        "creator_id": job_id,
                        "creator_type": "job",
                        "coordinates": [100, 200],
                        "reference_type": "wsi",
                        "reference_id": other_slide["id"],
                        "npp_created": 499,
                    },
                    {
                        "name": "my_point_1_1",
                        "type": "point",
                        "creator_id": job_id,
                        "creator_type": "job",
                        "coordinates": [100, 200],
                        "reference_type": "wsi",
                        "reference_id": other_slide["id"],
                        "npp_created": 499,
                    },
                ],
            },
        ],
    }
    collection = await http_client.post(f"{MDS_URL}/v3/collections", json=payload)
    return collection


@pytest_asyncio.fixture
async def point(http_client, job_id, slide):
    payload = {
        "name": "my_point",
        "type": "point",
        "creator_id": job_id,
        "creator_type": "job",
        "coordinates": [100, 200],
        "reference_type": "wsi",
        "reference_id": slide["id"],
        "npp_created": 499,
    }
    return await http_client.post(f"{MDS_URL}/v3/annotations", json=payload)


@pytest_asyncio.fixture
async def point_other_slide(http_client, job_id, other_slide):
    payload = {
        "name": "my_point",
        "type": "point",
        "creator_id": job_id,
        "creator_type": "job",
        "coordinates": [100, 200],
        "reference_type": "wsi",
        "reference_id": other_slide["id"],
        "npp_created": 499,
    }
    return await http_client.post(f"{MDS_URL}/v3/annotations", json=payload)


@pytest_asyncio.fixture
async def string(http_client, job_id, slide):
    payload = {
        "name": "my_string",
        "type": "string",
        "creator_id": job_id,
        "creator_type": "job",
        "value": "my_value",
        "reference_type": "wsi",
        "reference_id": slide["id"],
    }
    return await http_client.post(f"{MDS_URL}/v3/primitives", json=payload)


@pytest_asyncio.fixture
async def string_other_slide(http_client, job_id, other_slide):
    payload = {
        "name": "my_string",
        "type": "string",
        "creator_id": job_id,
        "creator_type": "job",
        "value": "my_value",
        "reference_type": "wsi",
        "reference_id": other_slide["id"],
    }
    return await http_client.post(f"{MDS_URL}/v3/primitives", json=payload)


@pytest_asyncio.fixture
async def string_with_point_reference(http_client, job_id, point):
    payload = {
        "name": "my_string",
        "type": "string",
        "creator_id": job_id,
        "creator_type": "job",
        "value": "my_value",
        "reference_type": "annotation",
        "reference_id": point["id"],
    }
    return await http_client.post(f"{MDS_URL}/v3/primitives", json=payload)


@pytest_asyncio.fixture
async def rectangle(http_client, job_id, slide):
    payload = {
        "name": "my_rectangle",
        "type": "rectangle",
        "creator_id": job_id,
        "creator_type": "job",
        "upper_left": [100, 200],
        "width": 256,
        "height": 128,
        "reference_type": "wsi",
        "reference_id": slide["id"],
        "npp_created": 499,
    }
    return await http_client.post(f"{MDS_URL}/v3/annotations", json=payload)


@pytest_asyncio.fixture
async def other_rectangle(http_client, job_id, slide):
    payload = {
        "name": "my_rectangle",
        "type": "rectangle",
        "creator_id": job_id,
        "creator_type": "job",
        "upper_left": [100, 200],
        "width": 256,
        "height": 128,
        "reference_type": "wsi",
        "reference_id": slide["id"],
        "npp_created": 499,
    }
    return await http_client.post(f"{MDS_URL}/v3/annotations", json=payload)


@pytest_asyncio.fixture
async def scoped_rectangle_wrong_creator_id(http_client, slide):
    payload = {
        "name": "my_rectangle",
        "type": "rectangle",
        "creator_id": str(uuid.uuid4()),
        "creator_type": "scope",
        "upper_left": [100, 200],
        "width": 256,
        "height": 128,
        "reference_type": "wsi",
        "reference_id": slide["id"],
        "npp_created": 499,
    }
    return await http_client.post(f"{MDS_URL}/v3/annotations", json=payload)


@pytest_asyncio.fixture
async def scoped_rectangle_wrong_creator_type(http_client, scoped_job_creator_id, slide):
    payload = {
        "name": "my_rectangle",
        "type": "rectangle",
        "creator_id": scoped_job_creator_id,
        "creator_type": "job",
        "upper_left": [100, 200],
        "width": 256,
        "height": 128,
        "reference_type": "wsi",
        "reference_id": slide["id"],
        "npp_created": 499,
    }
    return await http_client.post(f"{MDS_URL}/v3/annotations", json=payload)


@pytest_asyncio.fixture
async def roi_rectangle(http_client, job_id, slide):
    payload = {
        "name": "my_rectangle",
        "type": "rectangle",
        "creator_id": job_id,
        "creator_type": "job",
        "upper_left": [100, 200],
        "width": 256,
        "height": 128,
        "reference_type": "wsi",
        "reference_id": slide["id"],
        "npp_created": 499,
    }
    rectangle = await http_client.post(f"{MDS_URL}/v3/annotations", json=payload)
    payload = {
        "value": "org.empaia.global.v1.classes.roi",
        "reference_id": rectangle["id"],
        "reference_type": "annotation",
        "creator_id": str(uuid.uuid4()),
        "creator_type": "scope",
        "type": "class",
    }
    await http_client.post(f"{MDS_URL}/v3/classes", json=payload)
    return rectangle


@pytest_asyncio.fixture
async def other_rectangle_roi_klass(http_client, job_id, other_rectangle):
    payload = {
        "value": "org.empaia.global.v1.classes.roi",
        "reference_id": other_rectangle["id"],
        "reference_type": "annotation",
        "creator_id": job_id,
        "creator_type": "job",
        "type": "class",
    }
    return await http_client.post(f"{MDS_URL}/v3/classes", json=payload)


@pytest_asyncio.fixture
async def foo_bar_invalid_class(http_client, job_id, rectangle):
    payload = {
        "value": "org.empaia.vendor_name.ta.v3.0.classes.foo.bar.invalid",
        "reference_id": rectangle["id"],
        "reference_type": "annotation",
        "creator_id": job_id,
        "creator_type": "job",
        "type": "class",
    }
    return await http_client.post(f"{MDS_URL}/v3/classes", json=payload)


@pytest_asyncio.fixture
async def foo_bar_baz_class(http_client, job_id, rectangle):
    payload = {
        "value": "org.empaia.vendor_name.ta.v3.0.classes.foo.bar.baz",
        "reference_id": rectangle["id"],
        "reference_type": "annotation",
        "creator_id": job_id,
        "creator_type": "job",
        "type": "class",
    }
    return await http_client.post(f"{MDS_URL}/v3/classes", json=payload)


@pytest_asyncio.fixture
async def foo_bar_baz_rectangle(http_client, job_id, slide):
    payload = {
        "name": "my_rectangle",
        "type": "rectangle",
        "creator_id": job_id,
        "creator_type": "job",
        "upper_left": [100, 200],
        "width": 256,
        "height": 128,
        "reference_type": "wsi",
        "reference_id": slide["id"],
        "npp_created": 499,
    }
    rectangle = await http_client.post(f"{MDS_URL}/v3/annotations", json=payload)
    payload = {
        "value": "org.empaia.vendor_name.ta.v3.0.classes.foo.bar.baz",
        "reference_id": rectangle["id"],
        "reference_type": "annotation",
        "creator_id": str(uuid.uuid4()),
        "creator_type": "scope",
        "type": "class",
    }
    await http_client.post(f"{MDS_URL}/v3/classes", json=payload)
    return rectangle


@pytest_asyncio.fixture
async def unknown_bar_baz_rectangle(http_client, job_id, slide):
    payload = {
        "name": "my_rectangle",
        "type": "rectangle",
        "creator_id": job_id,
        "creator_type": "job",
        "upper_left": [100, 200],
        "width": 256,
        "height": 128,
        "reference_type": "wsi",
        "reference_id": slide["id"],
        "npp_created": 499,
    }
    rectangle = await http_client.post(f"{MDS_URL}/v3/annotations", json=payload)
    payload = {
        "value": "org.empaia.vendor_name.ta.v3.0.classes.unknown.bar.baz",
        "reference_id": rectangle["id"],
        "reference_type": "annotation",
        "creator_id": str(uuid.uuid4()),
        "creator_type": "scope",
        "type": "class",
    }
    await http_client.post(f"{MDS_URL}/v3/classes", json=payload)
    return rectangle


@pytest_asyncio.fixture
async def foo_bar_unknown_rectangle(http_client, job_id, slide):
    payload = {
        "name": "my_rectangle",
        "type": "rectangle",
        "creator_id": job_id,
        "creator_type": "job",
        "upper_left": [100, 200],
        "width": 256,
        "height": 128,
        "reference_type": "wsi",
        "reference_id": slide["id"],
        "npp_created": 499,
    }
    rectangle = await http_client.post(f"{MDS_URL}/v3/annotations", json=payload)
    payload = {
        "value": "org.empaia.vendor_name.ta.v3.0.classes.foo.bar.unknown",
        "reference_id": rectangle["id"],
        "reference_type": "annotation",
        "creator_id": str(uuid.uuid4()),
        "creator_type": "scope",
        "type": "class",
    }
    await http_client.post(f"{MDS_URL}/v3/classes", json=payload)
    return rectangle


@pytest_asyncio.fixture
async def collection(http_client, job_id, slide):
    payload = {
        "name": "my_collection",
        "type": "collection",
        "creator_id": job_id,
        "creator_type": "job",
        "reference_type": "wsi",
        "reference_id": slide["id"],
        "item_type": "point",
        "items": [
            {
                "name": "my_point_0",
                "type": "point",
                "creator_id": job_id,
                "creator_type": "job",
                "coordinates": [100, 200],
                "reference_type": "wsi",
                "reference_id": slide["id"],
                "npp_created": 499,
            },
            {
                "name": "my_point_1",
                "type": "point",
                "creator_id": job_id,
                "creator_type": "job",
                "coordinates": [100, 200],
                "reference_type": "wsi",
                "reference_id": slide["id"],
                "npp_created": 499,
            },
        ],
    }
    collection = await http_client.post(f"{MDS_URL}/v3/collections", json=payload)
    return collection


@pytest_asyncio.fixture
async def collection_other_slide(http_client, job_id, other_slide):
    payload = {
        "name": "my_collection",
        "type": "collection",
        "creator_id": job_id,
        "creator_type": "job",
        "reference_type": "wsi",
        "reference_id": other_slide["id"],
        "item_type": "point",
        "items": [
            {
                "name": "my_point_0",
                "type": "point",
                "creator_id": job_id,
                "creator_type": "job",
                "coordinates": [100, 200],
                "reference_type": "wsi",
                "reference_id": other_slide["id"],
                "npp_created": 499,
            },
            {
                "name": "my_point_1",
                "type": "point",
                "creator_id": job_id,
                "creator_type": "job",
                "coordinates": [100, 200],
                "reference_type": "wsi",
                "reference_id": other_slide["id"],
                "npp_created": 499,
            },
        ],
    }
    collection = await http_client.post(f"{MDS_URL}/v3/collections", json=payload)
    return collection


@pytest_asyncio.fixture
async def collection_single_item_other_slide(http_client, job_id, slide, other_slide):
    payload = {
        "name": "my_collection",
        "type": "collection",
        "creator_id": job_id,
        "creator_type": "job",
        "reference_type": "wsi",
        "reference_id": slide["id"],
        "item_type": "point",
        "items": [
            {
                "name": "my_point_0",
                "type": "point",
                "creator_id": job_id,
                "creator_type": "job",
                "coordinates": [100, 200],
                "reference_type": "wsi",
                "reference_id": slide["id"],
                "npp_created": 499,
            },
            {
                "name": "my_point_1",
                "type": "point",
                "creator_id": job_id,
                "creator_type": "job",
                "coordinates": [100, 200],
                "reference_type": "wsi",
                "reference_id": other_slide["id"],
                "npp_created": 499,
            },
        ],
    }
    collection = await http_client.post(f"{MDS_URL}/v3/collections", json=payload)
    return collection


@pytest_asyncio.fixture
async def nested_collection(http_client, job_id, slide):
    payload = {
        "name": "my_collection",
        "type": "collection",
        "creator_id": job_id,
        "creator_type": "job",
        "reference_type": "wsi",
        "reference_id": slide["id"],
        "item_type": "collection",
        "items": [
            {
                "name": "my_collection_0",
                "type": "collection",
                "creator_id": job_id,
                "creator_type": "job",
                "reference_type": "wsi",
                "reference_id": slide["id"],
                "item_type": "point",
                "items": [
                    {
                        "name": "my_point_0",
                        "type": "point",
                        "creator_id": job_id,
                        "creator_type": "job",
                        "coordinates": [100, 200],
                        "reference_type": "wsi",
                        "reference_id": slide["id"],
                        "npp_created": 499,
                    },
                    {
                        "name": "my_point_1",
                        "type": "point",
                        "creator_id": job_id,
                        "creator_type": "job",
                        "coordinates": [100, 200],
                        "reference_type": "wsi",
                        "reference_id": slide["id"],
                        "npp_created": 499,
                    },
                ],
            },
            {
                "name": "my_collection_1",
                "type": "collection",
                "creator_id": job_id,
                "creator_type": "job",
                "reference_type": "wsi",
                "reference_id": slide["id"],
                "item_type": "point",
                "items": [
                    {
                        "name": "my_point_2",
                        "type": "point",
                        "creator_id": job_id,
                        "creator_type": "job",
                        "coordinates": [100, 200],
                        "reference_type": "wsi",
                        "reference_id": slide["id"],
                        "npp_created": 499,
                    },
                ],
            },
            {
                "name": "my_collection_2",
                "type": "collection",
                "creator_id": job_id,
                "creator_type": "job",
                "reference_type": "wsi",
                "reference_id": slide["id"],
                "item_type": "point",
                "items": [],
            },
        ],
    }
    collection = await http_client.post(f"{MDS_URL}/v3/collections", json=payload)
    return collection


@pytest_asyncio.fixture
async def nested_collection_large(http_client, job_id, slide):
    number_of_sub_collections = 100
    number_of_points_per_collection = 100

    point = {
        "name": "my_point",
        "type": "point",
        "creator_id": job_id,
        "creator_type": "job",
        "coordinates": [100, 200],
        "reference_type": "wsi",
        "reference_id": slide["id"],
        "npp_created": 499,
    }

    subcollection = {
        "name": "my_collection",
        "type": "collection",
        "creator_id": job_id,
        "creator_type": "job",
        "reference_type": "wsi",
        "reference_id": slide["id"],
        "item_type": "point",
        "items": [point for _ in range(number_of_points_per_collection)],
    }

    payload = {
        "name": "my_collection",
        "type": "collection",
        "creator_id": job_id,
        "creator_type": "job",
        "reference_type": "wsi",
        "reference_id": slide["id"],
        "item_type": "collection",
        "items": [subcollection for _ in range(number_of_sub_collections)],
    }
    collection = await http_client.post(f"{MDS_URL}/v3/collections", json=payload)
    return collection


@pytest_asyncio.fixture
async def rois(http_client, job_id, slide):
    payload = {
        "name": "my_rectangles",
        "type": "collection",
        "creator_id": job_id,
        "creator_type": "job",
        "reference_type": "wsi",
        "reference_id": slide["id"],
        "item_type": "rectangle",
        "items": [
            {
                "name": "my_rectangle_0",
                "type": "rectangle",
                "creator_id": job_id,
                "creator_type": "job",
                "upper_left": [100, 200],
                "width": 256,
                "height": 128,
                "reference_type": "wsi",
                "reference_id": slide["id"],
                "npp_created": 499,
            },
            {
                "name": "my_rectangle_1",
                "type": "rectangle",
                "creator_id": job_id,
                "creator_type": "job",
                "upper_left": [100, 200],
                "width": 256,
                "height": 128,
                "reference_type": "wsi",
                "reference_id": slide["id"],
                "npp_created": 499,
            },
        ],
    }
    collection = await http_client.post(f"{MDS_URL}/v3/collections", json=payload)
    return collection


@pytest_asyncio.fixture
async def many_polygons(http_client, job_id, slide):
    payload = {
        "name": "my_polygons",
        "type": "collection",
        "creator_id": job_id,
        "creator_type": "job",
        "reference_type": "wsi",
        "reference_id": slide["id"],
        "item_type": "polygon",
        "items": [],
    }
    for i in range(2100):
        payload["items"].append(
            {
                "name": f"my_polygon_{i}",
                "type": "polygon",
                "creator_id": job_id,
                "creator_type": "job",
                "coordinates": [[0, 0], [0, 1], [1, 1]],
                "reference_type": "wsi",
                "reference_id": slide["id"],
                "npp_created": 499,
            }
        )
    collection = await http_client.post(f"{MDS_URL}/v3/collections", json=payload)
    return collection


@pytest_asyncio.fixture
async def classes_referencing_many_polygons(http_client, job_id, many_polygons):
    payload = {
        "name": "my_classes",
        "type": "collection",
        "creator_id": job_id,
        "creator_type": "job",
        "item_type": "class",
        "items": [],
    }
    for item in many_polygons["items"]:
        payload["items"].append(
            {
                "value": "org.empaia.vendor_name.ta.v3.0.classes.tumor",
                "type": "class",
                "creator_id": job_id,
                "creator_type": "job",
                "reference_type": "annotation",
                "reference_id": item["id"],
            }
        )
    collection = await http_client.post(f"{MDS_URL}/v3/collections", json=payload)
    return collection


@pytest_asyncio.fixture
async def ints_referencing_rois(http_client, job_id, rois):
    payload = {
        "name": "my_ints",
        "type": "collection",
        "creator_id": job_id,
        "creator_type": "job",
        "item_type": "integer",
        "items": [
            {
                "name": "my_int_0",
                "type": "integer",
                "creator_id": job_id,
                "creator_type": "job",
                "value": 0,
                "reference_type": "annotation",
                "reference_id": rois["items"][0]["id"],
            },
            {
                "name": "my_int_1",
                "type": "integer",
                "creator_id": job_id,
                "creator_type": "job",
                "value": 1,
                "reference_type": "annotation",
                "reference_id": rois["items"][1]["id"],
            },
        ],
    }
    collection = await http_client.post(f"{MDS_URL}/v3/collections", json=payload)
    return collection


@pytest_asyncio.fixture
async def ints_in_nested_collection_referencing_rois(http_client, job_id, slide, rois):
    payload = {
        "name": "my_ints",
        "type": "collection",
        "creator_id": job_id,
        "creator_type": "job",
        "reference_type": "wsi",
        "reference_id": slide["id"],
        "item_type": "collection",
        "items": [
            {
                "name": "my_ints_sub_collection_0",
                "type": "collection",
                "creator_id": job_id,
                "creator_type": "job",
                "item_type": "integer",
                "items": [
                    {
                        "name": "my_int_0",
                        "type": "integer",
                        "creator_id": job_id,
                        "creator_type": "job",
                        "value": 0,
                        "reference_type": "annotation",
                        "reference_id": rois["items"][0]["id"],
                    },
                    {
                        "name": "my_int_1",
                        "type": "integer",
                        "creator_id": job_id,
                        "creator_type": "job",
                        "value": 1,
                        "reference_type": "annotation",
                        "reference_id": rois["items"][1]["id"],
                    },
                ],
            },
            {
                "name": "my_ints_sub_collection_1",
                "type": "collection",
                "creator_id": job_id,
                "creator_type": "job",
                "item_type": "integer",
                "items": [],
            },
        ],
    }
    collection = await http_client.post(f"{MDS_URL}/v3/collections", json=payload)
    return collection


@pytest_asyncio.fixture
async def floats_in_nested_collection_referencing_nested_points(http_client, job_id, slide, nested_collection):
    payload = {
        "name": "my_floats",
        "type": "collection",
        "creator_id": job_id,
        "creator_type": "job",
        "reference_type": "wsi",
        "reference_id": slide["id"],
        "item_type": "collection",
        "items": [
            {
                "name": "my_floats_sub_collection_0",
                "type": "collection",
                "creator_id": job_id,
                "creator_type": "job",
                "item_type": "float",
                "items": [
                    {
                        "name": "my_float_0",
                        "type": "float",
                        "creator_id": job_id,
                        "creator_type": "job",
                        "value": 0.0,
                        "reference_type": "annotation",
                        "reference_id": nested_collection["items"][0]["items"][0]["id"],
                    },
                    {
                        "name": "my_float_1",
                        "type": "float",
                        "creator_id": job_id,
                        "creator_type": "job",
                        "value": 1.0,
                        "reference_type": "annotation",
                        "reference_id": nested_collection["items"][0]["items"][1]["id"],
                    },
                ],
            },
            {
                "name": "my_floats_sub_collection_1",
                "type": "collection",
                "creator_id": job_id,
                "creator_type": "job",
                "item_type": "float",
                "items": [
                    {
                        "name": "my_float_2",
                        "type": "float",
                        "creator_id": job_id,
                        "creator_type": "job",
                        "value": 0.0,
                        "reference_type": "annotation",
                        "reference_id": nested_collection["items"][1]["items"][0]["id"],
                    },
                    {
                        "name": "my_float_3",
                        "type": "float",
                        "creator_id": job_id,
                        "creator_type": "job",
                        "value": 1.0,
                        "reference_type": "annotation",
                        "reference_id": nested_collection["items"][0]["items"][1]["id"],
                    },
                ],
            },
        ],
    }
    collection = await http_client.post(f"{MDS_URL}/v3/collections", json=payload)
    return collection


@pytest_asyncio.fixture
async def floats_in_nested_collection_referencing_nested_points_wrong_reference_id(
    http_client, job_id, slide, nested_collection, point
):
    payload = {
        "name": "my_floats",
        "type": "collection",
        "creator_id": job_id,
        "creator_type": "job",
        "reference_type": "wsi",
        "reference_id": slide["id"],
        "item_type": "collection",
        "items": [
            {
                "name": "my_floats_sub_collection_0",
                "type": "collection",
                "creator_id": job_id,
                "creator_type": "job",
                "item_type": "float",
                "items": [
                    {
                        "name": "my_float_0",
                        "type": "float",
                        "creator_id": job_id,
                        "creator_type": "job",
                        "value": 0.0,
                        "reference_type": "annotation",
                        "reference_id": nested_collection["items"][0]["items"][0]["id"],
                    },
                    {
                        "name": "my_float_1",
                        "type": "float",
                        "creator_id": job_id,
                        "creator_type": "job",
                        "value": 1.0,
                        "reference_type": "annotation",
                        "reference_id": nested_collection["items"][0]["items"][1]["id"],
                    },
                ],
            },
            {
                "name": "my_floats_sub_collection_1",
                "type": "collection",
                "creator_id": job_id,
                "creator_type": "job",
                "item_type": "float",
                "items": [
                    {
                        "name": "my_float_2",
                        "type": "float",
                        "creator_id": job_id,
                        "creator_type": "job",
                        "value": 0.0,
                        "reference_type": "annotation",
                        "reference_id": nested_collection["items"][1]["items"][0]["id"],
                    },
                    {
                        "name": "my_float_3",
                        "type": "float",
                        "creator_id": job_id,
                        "creator_type": "job",
                        "value": 1.0,
                        "reference_type": "annotation",
                        "reference_id": point["id"],  # referencing wrong annotation
                    },
                ],
            },
        ],
    }
    collection = await http_client.post(f"{MDS_URL}/v3/collections", json=payload)
    return collection


@pytest_asyncio.fixture
async def floats_in_nested_collection_referencing_nested_points_large(
    http_client, job_id, slide, nested_collection_large
):
    def get_valid_float():
        random_subcollection_index = random.randint(0, len(nested_collection_large["items"]) - 1)
        random_annotation_index = random.randint(
            0, len(nested_collection_large["items"][random_subcollection_index]["items"]) - 1
        )
        return {
            "name": "my_float",
            "type": "float",
            "creator_id": job_id,
            "creator_type": "job",
            "value": 0.0,
            "reference_type": "annotation",
            "reference_id": nested_collection_large["items"][random_subcollection_index]["items"][
                random_annotation_index
            ]["id"],
        }

    def get_valid_sub_collection(number_of_floats_per_collection):
        return {
            "name": "my_floats_sub_collection",
            "type": "collection",
            "creator_id": job_id,
            "creator_type": "job",
            "item_type": "float",
            "items": [get_valid_float() for _ in range(number_of_floats_per_collection)],
        }

    number_of_sub_collections = 100
    number_of_floats_per_collection = 100

    payload = {
        "name": "my_floats",
        "type": "collection",
        "creator_id": job_id,
        "creator_type": "job",
        "reference_type": "wsi",
        "reference_id": slide["id"],
        "item_type": "collection",
        "items": [get_valid_sub_collection(number_of_floats_per_collection) for _ in range(number_of_sub_collections)],
    }
    collection = await http_client.post(f"{MDS_URL}/v3/collections", json=payload)
    return collection


@pytest_asyncio.fixture
async def floats_in_nested_collection_referencing_nested_points_wrong_reference_type(
    http_client, job_id, slide, nested_collection, point
):
    payload = {
        "name": "my_floats",
        "type": "collection",
        "creator_id": job_id,
        "creator_type": "job",
        "reference_type": "wsi",
        "reference_id": slide["id"],
        "item_type": "collection",
        "items": [
            {
                "name": "my_floats_sub_collection_0",
                "type": "collection",
                "creator_id": job_id,
                "creator_type": "job",
                "item_type": "float",
                "items": [
                    {
                        "name": "my_float_0",
                        "type": "float",
                        "creator_id": job_id,
                        "creator_type": "job",
                        "value": 0.0,
                        "reference_type": "annotation",
                        "reference_id": nested_collection["items"][0]["items"][0]["id"],
                    },
                    {
                        "name": "my_float_1",
                        "type": "float",
                        "creator_id": job_id,
                        "creator_type": "job",
                        "value": 1.0,
                        "reference_type": "annotation",
                        "reference_id": nested_collection["items"][0]["items"][1]["id"],
                    },
                ],
            },
            {
                "name": "my_floats_sub_collection_1",
                "type": "collection",
                "creator_id": job_id,
                "creator_type": "job",
                "item_type": "float",
                "items": [
                    {
                        "name": "my_float_2",
                        "type": "float",
                        "creator_id": job_id,
                        "creator_type": "job",
                        "value": 0.0,
                        "reference_type": "annotation",
                        "reference_id": nested_collection["items"][1]["items"][0]["id"],
                    },
                    {
                        "name": "my_float_3",
                        "type": "float",
                        "creator_id": job_id,
                        "creator_type": "job",
                        "value": 1.0,
                        "reference_type": "wsi",  # wrong reference type
                        "reference_id": nested_collection["items"][0]["items"][1]["id"],
                    },
                ],
            },
        ],
    }
    collection = await http_client.post(f"{MDS_URL}/v3/collections", json=payload)
    return collection


@pytest_asyncio.fixture
async def ints_in_nested_collection_referencing_rois_wrong_reference_id(http_client, job_id, slide, rois, rectangle):
    payload = {
        "name": "my_ints",
        "type": "collection",
        "creator_id": job_id,
        "creator_type": "job",
        "reference_type": "wsi",
        "reference_id": slide["id"],
        "item_type": "collection",
        "items": [
            {
                "name": "my_ints_sub_collection_0",
                "type": "collection",
                "creator_id": job_id,
                "creator_type": "job",
                "item_type": "integer",
                "items": [
                    {
                        "name": "my_int_0",
                        "type": "integer",
                        "creator_id": job_id,
                        "creator_type": "job",
                        "value": 0,
                        "reference_type": "annotation",
                        "reference_id": rois["items"][0]["id"],
                    },
                    {
                        "name": "my_int_1",
                        "type": "integer",
                        "creator_id": job_id,
                        "creator_type": "job",
                        "value": 1,
                        "reference_type": "annotation",
                        "reference_id": rectangle["id"],  # wrong reference id
                    },
                ],
            },
            {
                "name": "my_ints_sub_collection_1",
                "type": "collection",
                "creator_id": job_id,
                "creator_type": "job",
                "item_type": "integer",
                "items": [],
            },
        ],
    }
    collection = await http_client.post(f"{MDS_URL}/v3/collections", json=payload)
    return collection


@pytest_asyncio.fixture
async def ints_in_nested_collection_referencing_rois_wrong_reference_type(http_client, job_id, slide, rois):
    payload = {
        "name": "my_ints",
        "type": "collection",
        "creator_id": job_id,
        "creator_type": "job",
        "reference_type": "wsi",
        "reference_id": slide["id"],
        "item_type": "collection",
        "items": [
            {
                "name": "my_ints_sub_collection_0",
                "type": "collection",
                "creator_id": job_id,
                "creator_type": "job",
                "item_type": "integer",
                "items": [
                    {
                        "name": "my_int_0",
                        "type": "integer",
                        "creator_id": job_id,
                        "creator_type": "job",
                        "value": 0,
                        "reference_type": "annotation",
                        "reference_id": rois["items"][0]["id"],
                    },
                    {
                        "name": "my_int_1",
                        "type": "integer",
                        "creator_id": job_id,
                        "creator_type": "job",
                        "value": 1,
                        "reference_type": "wsi",  # wrong reference type
                        "reference_id": rois["items"][1]["id"],
                    },
                ],
            },
            {
                "name": "my_ints_sub_collection_1",
                "type": "collection",
                "creator_id": job_id,
                "creator_type": "job",
                "item_type": "integer",
                "items": [],
            },
        ],
    }
    collection = await http_client.post(f"{MDS_URL}/v3/collections", json=payload)
    return collection


@pytest_asyncio.fixture
async def ints_referencing_rois_wrong_reference_type(http_client, job_id, rois):
    payload = {
        "name": "my_ints",
        "type": "collection",
        "creator_id": job_id,
        "creator_type": "job",
        "item_type": "integer",
        "items": [
            {
                "name": "my_int_0",
                "type": "integer",
                "creator_id": job_id,
                "creator_type": "job",
                "value": 0,
                "reference_type": "annotation",
                "reference_id": rois["items"][0]["id"],
            },
            {
                "name": "my_int_1",
                "type": "integer",
                "creator_id": job_id,
                "creator_type": "job",
                "value": 1,
                "reference_type": "wsi",  # wrong reference type
                "reference_id": rois["items"][1]["id"],
            },
        ],
    }
    collection = await http_client.post(f"{MDS_URL}/v3/collections", json=payload)
    return collection


@pytest_asyncio.fixture
async def ints_referencing_rois_wrong_reference_id(http_client, job_id, rois, rectangle):
    payload = {
        "name": "my_ints",
        "type": "collection",
        "creator_id": job_id,
        "creator_type": "job",
        "item_type": "integer",
        "items": [
            {
                "name": "my_int_0",
                "type": "integer",
                "creator_id": job_id,
                "creator_type": "job",
                "value": 0,
                "reference_type": "annotation",
                "reference_id": rois["items"][0]["id"],
            },
            {
                "name": "my_int_1",
                "type": "integer",
                "creator_id": job_id,
                "creator_type": "job",
                "value": 1,
                "reference_type": "annotation",
                "reference_id": rectangle["id"],  # referencing wrong annotation
            },
        ],
    }
    collection = await http_client.post(f"{MDS_URL}/v3/collections", json=payload)
    return collection


@pytest_asyncio.fixture
async def rectangle_wrong_creator_id(http_client, slide):
    payload = {
        "name": "my_rectangle",
        "type": "rectangle",
        "creator_id": str(uuid.uuid4()),
        "creator_type": "job",
        "upper_left": [100, 200],
        "width": 256,
        "height": 128,
        "reference_type": "wsi",
        "reference_id": slide["id"],
        "npp_created": 499,
    }
    return await http_client.post(f"{MDS_URL}/v3/annotations", json=payload)


@pytest_asyncio.fixture
async def rectangle_wrong_creator_type(http_client, job_id, slide):
    payload = {
        "name": "my_rectangle",
        "type": "rectangle",
        "creator_id": job_id,
        "creator_type": "scope",
        "upper_left": [100, 200],
        "width": 256,
        "height": 128,
        "reference_type": "wsi",
        "reference_id": slide["id"],
        "npp_created": 499,
    }
    return await http_client.post(f"{MDS_URL}/v3/annotations", json=payload)


@pytest_asyncio.fixture
async def unknown_local_class(http_client, job_id, rectangle):
    payload = {
        "value": "org.empaia.vendor_name.ta.v3.0.classes.foo",
        "reference_id": rectangle["id"],
        "reference_type": "annotation",
        "creator_id": job_id,
        "creator_type": "job",
        "type": "class",
    }
    return await http_client.post(f"{MDS_URL}/v3/classes", json=payload)
