from typing import List

import requests

from empaia_app_test_suite import settings
from empaia_app_test_suite.commands.helper.data_helper import get_ids
from empaia_app_test_suite.custom_models import ApiDataType, InputParameter
from empaia_app_test_suite.utils.utils_mds import post_collection


def register_input_parameters(
    inputs_to_register: List[InputParameter], input_ids_already_registered: List[str], wsi_ids: List[str], mds_url: str
):
    # needed to check whether all required ids exist for inputs with reference_id
    input_ids_persisted = wsi_ids
    input_ids_persisted += input_ids_already_registered

    input_keys = [p.input_key for p in inputs_to_register]
    input_keys_persisted = []
    new_inputs_persisted_last_run = True
    # loop until no more new items were posted in last loop
    while new_inputs_persisted_last_run:
        new_inputs_persisted_last_run = False
        for input_param in inputs_to_register:
            if (
                # assure references exist at DADS
                set(input_param.reference_ids).issubset(input_ids_persisted)
                # no double post
                and input_param.input_key not in input_keys_persisted
            ):
                try:
                    params = {"external_ids": True}
                    if input_param.api_data_type == ApiDataType.COLLECTIONS:
                        return_data = post_collection(input_param.post_data, mds_url, params)

                    else:
                        r = requests.post(
                            f"{mds_url}/v3/{input_param.api_data_type.value}", json=input_param.post_data, params=params
                        )
                        r.raise_for_status()
                        return_data = r.json()
                    input_ids_persisted += get_ids(return_data)
                    new_inputs_persisted_last_run = True
                    input_keys_persisted.append(input_param.input_key)
                except requests.HTTPError as e:
                    error_msg = f"Could not register input [{input_param.input_key}]. Service Error: {e}"
                    raise Exception(error_msg) from e

    if len(inputs_to_register) > len(input_keys_persisted):
        input_key_not_persisted = list(set(input_keys) - set(input_keys_persisted))
        error_msg = (
            f"Could not register the following inputs: {input_key_not_persisted}. "
            "Check if their [reference_id]s are valid [id]s of other inputs."
        )
        raise Exception(error_msg)


def read_job_env(job_env_file):
    try:
        job_env = settings.JobEnv(env_file=job_env_file)
    except UnicodeDecodeError:
        # windows
        job_env = settings.JobEnv(env_file=job_env_file, encoding="utf-16")

    return job_env
