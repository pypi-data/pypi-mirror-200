import json
from typing import List
from uuid import uuid4

from empaia_app_test_suite.constants import ALLOWED_ANNOTATION_TYPES, ALLOWED_PRIMITIVE_TYPES
from empaia_app_test_suite.custom_models import TYPE_MODEL_MAP, ApiDataType
from empaia_app_test_suite.utils.utils_commons import ValidationError


def extend_creator_inplace(data, scope_id):
    creator_id = scope_id
    creator_type = "scope"
    # if "creator_id" not in data:
    data["creator_id"] = creator_id
    # if "creator_type" not in data:
    data["creator_type"] = creator_type
    if "items" in data:
        for item in data["items"]:
            extend_creator_inplace(item, scope_id)


def extend_id_inplace(data):
    if "id" not in data:
        data["id"] = str(uuid4())
    if "items" in data:
        for item in data["items"]:
            extend_id_inplace(item)


def extend_type_inplace(data: dict):
    if "type" not in data:
        if "items" in data:
            data["type"] = "collection"
            for item in data["items"]:
                extend_type_inplace(item)
        elif "value" in data:
            data["type"] = "class"
        elif "path" in data:
            data["type"] = "wsi"


def get_type(data: dict):
    if "type" in data:
        if data["type"] in ALLOWED_ANNOTATION_TYPES:
            return ApiDataType.ANNOTATIONS
        elif data["type"] in ALLOWED_PRIMITIVE_TYPES:
            return ApiDataType.PRIMITIVES
        elif data["type"] == "wsi":
            return ApiDataType.SLIDES
        elif data["type"] == "collection":
            return ApiDataType.COLLECTIONS
        elif data["type"] == "class":
            return ApiDataType.CLASSES
    elif "items" in data:
        return ApiDataType.COLLECTIONS
    elif "value" in data:
        return ApiDataType.CLASSES
    return None


def parse_input_item(_type: str, _file: str):
    with open(_file, encoding="utf-8") as f:
        data = json.load(f)
    if "output_key" in data:
        return
    else:
        extend_type_inplace(data)
        type_model = TYPE_MODEL_MAP[_type]
        return type_model.parse_obj(data)


def is_class_or_class_collection(data):
    if data["type"] == "class":
        return True
    if data["type"] == "collection":
        if "items" in data:
            for item in data["items"]:
                has_classes = is_class_or_class_collection(item)
                if has_classes:
                    return True


def get_ids(data: dict) -> List[str]:
    ids = []
    if "id" in data:
        ids.append(data["id"])
    if "items" in data:
        for item in data["items"]:
            ids += get_ids(item)
    return ids


def check_reference_id(file_path, data):
    # classes
    if "type" not in data and "items" not in data and "value" in data:
        if "reference_id" not in data:
            error_msg = f"Please check the file {file_path}. " "At least one class is missing [reference_id]."
            raise ValidationError(error_msg)
    # annotations
    if "type" in data:
        if data["type"] in ALLOWED_ANNOTATION_TYPES:
            if "reference_id" not in data:
                error_msg = f"Please check the file {file_path}. " "At least one annotation is missing [reference_id]."
                raise ValidationError(error_msg)
    if "items" in data:
        for item in data["items"]:
            item = check_reference_id(file_path, item)
    return data


def get_reference_ids(data: dict) -> List[str]:
    reference_ids = []
    if "reference_id" in data:
        reference_ids.append(data["reference_id"])
    if "items" in data:
        for item in data["items"]:
            reference_ids += get_reference_ids(item)
    return reference_ids


def check_collections_and_items_id(file_path, data):
    has_id = "id" in data
    if "item_type" in data:
        for item in data["items"]:
            item_has_id = "id" in item
            leafs_have_id = check_collections_and_items_id(file_path, item)
            if item_has_id != has_id or leafs_have_id != has_id:
                error_msg = (
                    f"Check file [{file_path}]. If assigning [id]s to input collections or its items, "
                    "then all items and the collection itself must have an [id] assigned."
                )
                raise ValidationError(error_msg)
    return has_id
