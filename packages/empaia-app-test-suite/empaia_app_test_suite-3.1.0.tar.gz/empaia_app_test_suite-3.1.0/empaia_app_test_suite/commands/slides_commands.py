import json

import requests

from empaia_app_test_suite.commands.helper.data_helper import extend_id_inplace, extend_type_inplace
from empaia_app_test_suite.commands.helper.wsi_helper import (
    append_wsis_in_input_dict_to_list,
    is_single_wsi_input,
    is_wsi_collection,
    validate_wsis_current_job_inputs,
    validate_wsis_with_existing_wsis,
)
from empaia_app_test_suite.utils.utils_commons import get_service_url
from empaia_app_test_suite.utils.utils_mds import get_or_create_static_case, register_wsis
from empaia_app_test_suite.utils.utils_print import PrintStep


def slides_register(client, slide_file, quiet=False):
    mds_url = get_service_url(client=client, service_name="medical-data-service")
    with PrintStep("Create case if none exists", quiet=quiet):
        get_or_create_static_case(mds_url)
    with PrintStep("Validate slide file", quiet=quiet):
        wsis_to_register = []
        with open(slide_file, "rb") as data_file:
            data = json.loads(data_file.read())
            extend_type_inplace(data)
            extend_id_inplace(data)
            if is_single_wsi_input(data):
                append_wsis_in_input_dict_to_list(data, wsis_to_register)
            elif is_wsi_collection(data):
                append_wsis_in_input_dict_to_list(data, wsis_to_register)
            else:
                error_msg = (
                    f"The file [{slide_file}] does not match the correct syntax "
                    "for a single slide or for a collection of slides."
                )
                raise Exception(error_msg)
            no_duplicate_new_wsis, _duplicate_wsis = validate_wsis_current_job_inputs(wsis_to_register)
            new_wsis, existing_wsis = validate_wsis_with_existing_wsis(no_duplicate_new_wsis, mds_url)
    with PrintStep("Add new slide(s) to case", quiet=quiet):
        _wsi_ids = register_wsis(new_wsis, mds_url)
    return new_wsis, existing_wsis


def get_slides_list(client):
    mds_url = get_service_url(client=client, service_name="medical-data-service")
    r = requests.get(f"{mds_url}/v3/slides")
    r.raise_for_status()
    slides = r.json()
    for slide in slides["items"]:
        slide_id = slide["id"]
        if slide["deleted"]:
            slide["path"] = ""
        else:
            r = requests.get(f"{mds_url}/private/v3/slides/{slide_id}/storage")
            r.raise_for_status()
            storage = r.json()
            slide["path"] = storage["storage_addresses"][0]["address"]
    return slides


def delete_slide(client, slide_id):
    mds_url = get_service_url(client=client, service_name="medical-data-service")

    # delete storage
    storage_url = f"{mds_url}/private/v3/slides/{slide_id}/storage"
    r = requests.delete(url=storage_url)
    r.raise_for_status()

    # set slide deleted
    data = {"deleted": True}
    update_url = f"{mds_url}/private/v3/slides/{slide_id}"
    r = requests.put(url=update_url, json=data)
    r.raise_for_status()
