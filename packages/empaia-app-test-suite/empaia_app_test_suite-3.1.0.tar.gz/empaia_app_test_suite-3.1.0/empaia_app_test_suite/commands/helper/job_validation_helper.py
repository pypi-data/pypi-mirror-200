import json
import os
from copy import deepcopy
from pathlib import Path
from typing import List

import requests
from pydantic import ValidationError as PydanticValidationError

from empaia_app_test_suite.commands.helper import data_helper as dh
from empaia_app_test_suite.commands.helper import wsi_helper as wh
from empaia_app_test_suite.custom_models import ApiDataType, InputParameter
from empaia_app_test_suite.utils.utils_commons import ValidationError
from empaia_app_test_suite.utils.utils_mds import get_collection, get_job


def validate_input_parameters_files(ead, input_dir, job_mode):
    # validate file exists for each input
    inputs = ead["modes"][job_mode]["inputs"]
    for input_key in inputs:
        input_data = ead["io"][input_key]
        input_file = os.path.join(input_dir, f"{input_key}.json")
        if not os.path.isfile(input_file):
            raise ValidationError(f"Validating [{input_key}] failed: No input file found")
        try:
            # pydantic model validation
            dh.parse_input_item(input_data["type"], input_file)
        except PydanticValidationError as e:
            raise ValidationError(f"Validating [{input_key}] failed: \n{e.json()}") from e
    return inputs


def is_ead_input_or_class(input_key, mode_inputs, data):
    if input_key in mode_inputs:
        return True
    if "value" in data and "reference_id" in data:
        return True
    if "item_type" in data:
        if data["item_type"] == "class":
            return True
        if data["item_type"] == "collection":
            return is_ead_input_or_class(input_key, mode_inputs, data["items"][0])
    return False


def parse_input_parameters_files(ead, input_dir, job_mode, mode_inputs, scope_id):
    # semantic validation and data extension
    inputs_to_register = []
    wsis_to_register = []
    job_inputs = {}
    for path in Path(input_dir).glob("*.json"):
        input_key = path.stem
        with open(path, "rb") as data_file:
            data = json.loads(data_file.read())
            if "output_key" in data:
                continue
            dh.extend_type_inplace(data)
            is_class_or_classes_collection = dh.is_class_or_class_collection(data)
            if input_key not in mode_inputs and not is_class_or_classes_collection:
                continue
            if is_ead_input_or_class(input_key, mode_inputs, data):
                # single wsi
                if wh.is_single_wsi_input(data):
                    input_type = dh.get_type(data)
                    dh.extend_id_inplace(data)
                    wh.append_wsis_in_input_dict_to_list(data, wsis_to_register)
                # wsi collection
                elif wh.is_wsi_collection(data):
                    input_type = dh.get_type(data)
                    # check if either all collection items (incl. collection) either dont have ID or all do have
                    dh.check_collections_and_items_id(path, data)
                    # recursive add missing ids
                    dh.extend_id_inplace(data)
                    data_copy = deepcopy(data)
                    wh.append_wsis_in_input_dict_to_list(data_copy, wsis_to_register)
                    # recursive add creator_type and creator_id
                    dh.extend_creator_inplace(data, scope_id)
                    # for wsi collections, the leafs only have "id"
                    wh.strip_wsi_collection(input_key, data)
                    reference_ids = []
                    entry = InputParameter(
                        input_key=input_key, post_data=data, api_data_type=input_type, reference_ids=reference_ids
                    )
                    inputs_to_register.append(entry)
                # rest
                else:
                    input_type = dh.get_type(data)
                    # configuration file residing in inputs folder might be None
                    if input_type is not None:
                        # check if either all collection items (incl. collection) either dont have ID or all do have
                        dh.check_collections_and_items_id(path, data)
                        # check if classes and annotations have reference_id
                        dh.check_reference_id(path, data)
                        # recursive add creator_type and creator_id
                        dh.extend_creator_inplace(data, scope_id)
                        # recursive add missing ids
                        dh.extend_id_inplace(data)
                        # recursive get all reference_ids
                        reference_ids = dh.get_reference_ids(data)
                        entry = InputParameter(
                            input_key=input_key, post_data=data, api_data_type=input_type, reference_ids=reference_ids
                        )
                        inputs_to_register.append(entry)

                # for all
                # classes, e.g. rois, are not listed in the ead/job!
                if input_key in mode_inputs:
                    job_inputs[input_key] = data["id"]

    return inputs_to_register, wsis_to_register, job_inputs


def remove_already_existing_inputs(inputs_to_register: List[InputParameter], mds_url: str):
    inputs_to_register_new = []
    input_ids_already_registered = []
    for input_param in inputs_to_register:
        # input id does not exist
        if not check_input_with_id_exist(input_param, mds_url):
            inputs_to_register_new.append(input_param)
        # input id already exists AND data has not changed
        else:
            input_ids_already_registered += dh.get_ids(input_param.post_data)
    return inputs_to_register_new, input_ids_already_registered


def check_input_with_id_exist(input_param: InputParameter, mds_url: str):
    input_id = input_param.post_data["id"]
    r = requests.get(f"{mds_url}/v3/{input_param.api_data_type.value}/{input_id}?shallow=true")
    if r.status_code == 404:
        return False
    else:
        if input_param.api_data_type == ApiDataType.COLLECTIONS:
            return_data = get_collection(input_id, mds_url)
        else:
            r.raise_for_status()
            return_data = r.json()
        check_data_changed(input_param.input_key, input_param.post_data, return_data)
        return True


def check_data_changed(input_key: str, input_data: dict, return_data: dict):
    for key in input_data:
        if key != "items":
            if input_data[key] != return_data[key]:
                error_msg = (
                    f"Value of [{key}] of input parameter [{input_key}] with [id] [{input_data['id']}] changed. "
                    f"If [{input_key}] is a (nested) collection, this might also be an item of this collection. "
                    "Delete volumes of the EMPAIA Test Suite <docker volume rm $(eats services volumes)>. "
                    f"Or if you want to preserve old job data, assign new IDs to the collection [{input_key}] "
                    "and to all of its (nested) items."
                )
                raise Exception(error_msg)
        else:
            if len(input_data["items"]) != return_data["item_count"]:
                error_msg = (
                    f"Number of items in collection [{input_key}] changed. "
                    "Delete volumes of the EMPAIA Test Suite <docker volume rm $(eats services volumes)>. "
                    f"Or if you want to preserve old job data, assign new IDs to the collection [{input_key}] "
                    "and to all of its (nested) items."
                )
                raise Exception(error_msg)
            for item in input_data["items"]:
                item_id = item["id"]
                item_found = False
                for r_item in return_data["items"]:
                    r_item_id = r_item["id"]
                    if item_id == r_item_id:
                        check_data_changed(input_key, item, r_item)
                        item_found = True
                        break
                if not item_found:
                    error_msg = (
                        f"Number of items in collection [{input_key}] changed. "
                        "Delete volumes of the EMPAIA Test Suite <docker volume rm $(eats services volumes)>. "
                        f"Or if you want to preserve old job data, assign new IDs to the collection [{input_key}] "
                        "and to all of its (nested) items."
                    )
                    raise Exception(error_msg)


def check_preprocessing_job(app: dict, pp_job_id: str, input_dir, mds_url: str):
    ead = app["ead"]
    job = get_job(pp_job_id, mds_url)
    job_app_id = job["app_id"]
    job_status = job["status"]
    job_mode = job["mode"]
    job_outputs = job["outputs"]
    valid_input_keys = ead["modes"]["postprocessing"]["inputs"]
    inputs_from_preprocessing = {}

    if job_app_id != app["id"]:
        raise ValidationError("Referenced job is from a different app.")
    if job_status != "COMPLETED":
        raise ValidationError(f"Referenced preprocessing job is not in status 'COMPLETED'. Status: {job_status}")
    if job_mode != "PREPROCESSING":
        raise ValidationError(f"Referenced job is no preprocessing job. Mode: {job_mode}")

    for path in Path(input_dir).glob("*.json"):
        input_key = path.stem
        if input_key not in valid_input_keys:
            continue
        with open(path, "rb") as data_file:
            data = json.loads(data_file.read())
            if "output_key" in data:
                output_key = data["output_key"]
                if output_key not in job_outputs:
                    raise ValidationError(f"Input key '{input_key}' is no output of referenced preprocessing job")
                output_type = ead["io"][output_key]["type"]
                output_id = job_outputs[output_key]

                if output_type == "collection":
                    get_collection(output_id, mds_url, shallow=True)
                    inputs_from_preprocessing[input_key] = output_id
                    continue

                if output_type == "annotation":
                    url = f"{mds_url}/v3/annotations/{output_id}"
                if output_type == "class":
                    url = f"{mds_url}/v3/classes/{output_id}"
                if output_type == "primitive":
                    url = f"{mds_url}/v3/primitives/{output_id}"

                r = requests.get(url)
                r.raise_for_status()
                inputs_from_preprocessing[input_key] = output_id
                continue

    return inputs_from_preprocessing
