from typing import List
from uuid import uuid4

import requests

from empaia_app_test_suite.custom_models import WsiInput
from empaia_app_test_suite.utils.utils_commons import ValidationError


def is_single_wsi_input(input_data):
    if "type" in input_data:
        if input_data["type"] == "wsi":
            return True
    return False


def strip_wsi_collection(file_path, data):
    if "type" in data:
        if data["type"] == "wsi":
            if "id" not in data:
                raise Exception("NO ID IN WSI COLLECTION")
            del data["creator_type"]
            del data["creator_id"]
            del data["path"]
    if "items" in data:
        for item in data["items"]:
            strip_wsi_collection(file_path, item)


def is_wsi_collection(input_data: dict):
    if "item_type" in input_data:
        if input_data["item_type"] == "wsi":
            return True
        elif input_data["item_type"] == "collection":
            for item in input_data["items"]:
                return is_wsi_collection(item)
    return False


def append_wsis_in_input_dict_to_list(input_dict: dict, wsi_infos: List[WsiInput]):
    if input_dict["type"] == "wsi":
        wsi = WsiInput.parse_obj(input_dict)
        wsi.id = wsi.id if wsi.id is not None else str(uuid4)
        wsi_infos.append(wsi)
    elif input_dict["type"] == "collection":
        for item in input_dict["items"]:
            append_wsis_in_input_dict_to_list(item, wsi_infos)
    else:
        raise ValidationError("No WSI input.")


def validate_wsis_with_existing_wsis(wsis_to_register: List[WsiInput], mds_url: str):
    new_wsis = []
    existing_wsis = []
    for wsi_info in wsis_to_register:
        # check values equal in CDS
        r = requests.get(f"{mds_url}/v3/slides/{wsi_info.id}")
        wsi = wsi_info.dict()
        if r.status_code != 400:  # Not "Not found" (= already exists)
            existing_slide_cds = r.json()
            if existing_slide_cds["deleted"]:
                error_msg = f"Slide with id [{wsi_info.id}] already exists but was deleted. Please change id of Slide!"
                raise Exception(error_msg)
            for p in ["tissue", "stain", "block"]:
                if existing_slide_cds[p] != wsi[p]:
                    error_msg = (
                        f"Slide with id [{wsi_info.id}] already exists but with a different value for {p}: [{wsi[p]}]."
                    )
                    raise Exception(error_msg)
            existing_wsis.append(wsi_info)
        else:
            new_wsis.append(wsi_info)
        # check values equal in SMS
        r = requests.get(f"{mds_url}/private/v3/slides/{wsi_info.id}/storage")
        if r.status_code != 404:  # Not "Not found" (= already exists)
            existing_slide_sms = r.json()
            for address in existing_slide_sms["storage_addresses"]:
                if address["main_address"]:
                    if address["address"] != wsi_info.path:
                        error_msg = (
                            f"Slide with id [{wsi_info.id}] already exists "
                            f"but with a different path: {address['address']}"
                        )
                        raise Exception(error_msg)
    return new_wsis, existing_wsis


def validate_wsis_current_job_inputs(wsis_to_register: List[WsiInput]):
    no_duplicate_wsis = []
    duplicate_wsis = []
    wsis = {}
    for wsi_info in wsis_to_register:
        wsi_1 = wsi_info.dict()
        if "id" in wsi_1:
            if wsi_1["id"] in wsis:
                wsi_2 = wsis[wsi_1["id"]]
                for key in wsi_1:
                    if key in wsi_2:
                        if wsi_1[key] != wsi_2[key]:
                            error_msg = (
                                f"Slide with id [{wsi_1['id']}] already in input wsis "
                                f"but with a different value for {key}: [{wsi_1[key]}]."
                            )
                            raise Exception(error_msg)
                duplicate_wsis.append(wsi_info)
            else:
                no_duplicate_wsis.append(wsi_info)
        wsis[wsi_1["id"]] = wsi_1
    return no_duplicate_wsis, duplicate_wsis
