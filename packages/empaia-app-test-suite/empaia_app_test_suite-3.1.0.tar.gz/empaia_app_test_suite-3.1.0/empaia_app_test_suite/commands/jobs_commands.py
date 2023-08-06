import os
from time import sleep

import requests
from requests import HTTPError

from empaia_app_test_suite.commands.helper.job_helper import register_input_parameters
from empaia_app_test_suite.commands.helper.job_validation_helper import (
    check_preprocessing_job,
    parse_input_parameters_files,
    remove_already_existing_inputs,
    validate_input_parameters_files,
)
from empaia_app_test_suite.commands.helper.wsi_helper import (
    validate_wsis_current_job_inputs,
    validate_wsis_with_existing_wsis,
)
from empaia_app_test_suite.constants import ALLOWED_ANNOTATION_TYPES, ALLOWED_PRIMITIVE_TYPES, STATIC_ORGANIZATION_ID
from empaia_app_test_suite.utils.utils_commons import ValidationError, get_service_url, save_output_parameters
from empaia_app_test_suite.utils.utils_mds import (
    add_job_to_examination,
    create_job,
    get_annotation,
    get_collection,
    get_or_create_examination,
    get_or_create_scope,
    get_or_create_static_case,
    post_job_inputs,
    register_wsis,
    set_job_statuses,
)
from empaia_app_test_suite.utils.utils_mps import get_app, get_ead
from empaia_app_test_suite.utils.utils_print import PrintStep


def get_jobs_list(client):
    mds_url = get_service_url(client=client, service_name="medical-data-service")
    r = requests.get(f"{mds_url}/v3/jobs")
    r.raise_for_status()
    return r.json()


def jobs_register(client, app_id, input_dir, job_mode, pp_job_id):
    mds_url = get_service_url(client=client, service_name="medical-data-service")

    # get app from mps-mock
    app = get_app(client, app_id)
    ead = app["ead"]

    with PrintStep("Check if job mode declared in EAD"):
        if job_mode not in ead["modes"]:
            raise ValidationError(
                f"Job mode '{job_mode}' not decleared in EAD. Available modes: "
                f"{', '.join([key for key in ead['modes'].keys()])}"
            )
        if job_mode == "postprocessing":
            mode = ead["modes"][job_mode]
            if "containerized" in mode and not mode["containerized"]:
                raise ValidationError(
                    f"Job mode '{job_mode}' is declared as not 'containerized' in EAD. Mode not supported via CLI"
                )

    if pp_job_id:
        with PrintStep("Check provided preprocessing job"):
            inputs_from_preprocessing = check_preprocessing_job(app, pp_job_id, input_dir, mds_url)

    with PrintStep("Create case if none exists"):
        get_or_create_static_case(mds_url)
    with PrintStep("Create Examination if none is OPEN"):
        ex = get_or_create_examination(mds_url, app_id)
        ex_id = ex["id"]
    scope_id = None
    with PrintStep("Create scope if none exists"):
        scope_id = get_or_create_scope(mds_url, ex_id)
    with PrintStep("Validate inputs"):
        mode_inputs = validate_input_parameters_files(ead, input_dir, job_mode)
        inputs_to_register, wsis_to_register, job_inputs = parse_input_parameters_files(
            ead=ead, input_dir=input_dir, job_mode=job_mode, mode_inputs=mode_inputs, scope_id=scope_id
        )
        no_duplicate_new_wsis, _duplicates = validate_wsis_current_job_inputs(wsis_to_register)
        new_wsis, _existing = validate_wsis_with_existing_wsis(no_duplicate_new_wsis, mds_url)
        inputs_to_register, input_ids_already_registered = remove_already_existing_inputs(inputs_to_register, mds_url)
    with PrintStep("Add new slide(s) to case"):
        new_wsi_ids = register_wsis(new_wsis, mds_url)

    with PrintStep("Creating inputs"):
        wsi_ids = new_wsi_ids
        wsi_ids += [wsi_info.id for wsi_info in wsis_to_register]
        wsi_ids = list(set(wsi_ids))
        register_input_parameters(inputs_to_register, input_ids_already_registered, wsi_ids, mds_url)
    with PrintStep("Create job"):
        creator_id = "wbs" if job_mode == "preprocessing" else scope_id
        creator_type = "SERVICE" if job_mode == "preprocessing" else "SCOPE"
        job_id, token = create_job(
            app_id=app_id, mds_url=mds_url, job_mode=job_mode, creator_id=creator_id, creator_type=creator_type
        )

        if pp_job_id:
            job_inputs = {**job_inputs, **inputs_from_preprocessing}

        post_job_inputs(job_id=job_id, job_inputs=job_inputs, mds_url=mds_url)

    with PrintStep("Add job to examination"):
        add_job_to_examination(mds_url, job_id, ex_id)

    app_api = "http://app-service:8000"
    return job_id, token, app_api


def jobs_run(client, job_id, token, app_api):
    jes_url = get_service_url(client=client, service_name="job-execution-service")
    mds_url = get_service_url(client=client, service_name="medical-data-service")
    mps_url = get_service_url(client=client, service_name="marketplace-service-mock")

    with PrintStep("Retrieving app_id for job"):
        r = requests.get(f"{mds_url}/v3/jobs/{job_id}")
        r.raise_for_status()
        job_status = r.json()["status"]
        app_id = r.json()["app_id"]

    with PrintStep("Locking job inputs"):
        lock_inputs_to_job(client, job_id, mds_url, mps_url)

    with PrintStep("Checking job status"):
        if job_status != "ASSEMBLY":
            raise Exception(f"Job has already been started. Current status: {job_status}")

    with PrintStep("Starting app"):
        set_job_statuses(job_id, mds_url, ["READY"])
        exec_request = {
            "app_id": app_id,
            "job_id": job_id,
            "access_token": token,
            "app_service_url": app_api,
            "timeout": -1,
        }
        r = requests.post(
            f"{jes_url}/v1/executions", json=exec_request, headers={"organization-id": STATIC_ORGANIZATION_ID}
        )
        set_job_statuses(job_id, mds_url, ["SCHEDULED"])


def jobs_status(client, job_id, quiet=False):
    mds_url = get_service_url(client=client, service_name="medical-data-service")
    with PrintStep("Retrieve job status", quiet=quiet):
        r = requests.get(f"{mds_url}/v3/jobs/{job_id}")
        r.raise_for_status()
        job = r.json()
        status = job["status"]
    return status


def jobs_inspect(client, job_id, quiet=False):
    mds_url = get_service_url(client=client, service_name="medical-data-service")
    with PrintStep("Retrieve job", quiet=quiet):
        r = requests.get(f"{mds_url}/v3/jobs/{job_id}")
        r.raise_for_status()
        job = r.json()

    return job


def jobs_export(client, job_id, output_dir):
    mds_url = get_service_url(client=client, service_name="medical-data-service")

    with PrintStep("Retrieve job"):
        r = requests.get(f"{mds_url}/v3/jobs/{job_id}")
        r.raise_for_status()
        job = r.json()

    ead = get_ead(client, job["app_id"])

    with PrintStep("Export job outputs"):
        os.makedirs(output_dir, exist_ok=True)
        save_output_parameters(job=job, ead=ead, mds_url=mds_url, output_dir=output_dir)


def jobs_wait(client, job_id):
    job_finished_states = ("COMPLETED", "FAILED", "ERROR", "TIMEOUT")
    validation_finished_states = ("COMPLETED", "ERROR")
    error_msg_hint = "Use 'eats jobs inspect $EMPAIA_JOB_ID' for more information."

    with PrintStep(f"Waiting for job {job_id} to finish"):
        while True:
            job = jobs_inspect(client=client, job_id=job_id, quiet=True)
            status = job["status"]
            input_validation = job["input_validation_status"]
            output_validation = job["output_validation_status"]
            if input_validation == "ERROR":
                raise ValidationError(f"Input validation failed: {error_msg_hint}")
            if status in job_finished_states:
                if status != "COMPLETED":
                    raise ValidationError(f"Error while Job execution: {error_msg_hint}")
                if output_validation in validation_finished_states:
                    if output_validation == "ERROR":
                        raise ValidationError(f"Output validation failed: {error_msg_hint}")
                    if input_validation == "COMPLETED":
                        break
            sleep(1)


def jobs_abort(client, job_id):
    status = jobs_status(client, job_id)
    jes_url = get_service_url(client=client, service_name="job-execution-service")
    with PrintStep(f"Aborting job {job_id}"):
        try:
            r_jes = requests.put(
                f"{jes_url}/v1/executions/{job_id}/stop", headers={"organization-id": STATIC_ORGANIZATION_ID}
            )
            r_jes.raise_for_status()
            if not r_jes.json():
                raise Exception(f"Unable to abort job. Job status: {status}")
        except requests.HTTPError as e:
            if r_jes.status_code == 404:
                raise Exception(f"Unable to abort job. Job not yet started. Job status: {status}") from e
            raise e


def jobs_set_running(client, job_id):
    mds_url = get_service_url(client=client, service_name="medical-data-service")
    try:
        r_mds = requests.put(f"{mds_url}/v3/jobs/{job_id}/status", json={"status": "RUNNING"})
        r_mds.raise_for_status()
    except requests.HTTPError as e_mds:
        if r_mds.status_code == 400:  # job exists neither at JES nor JS
            error_msg = f"No job with with id [{job_id}] found."
        raise Exception(error_msg) from e_mds


def lock_inputs_to_job(client, job_id: str, mds_url: str, mps_url: str):
    url = f"{mds_url}/v3/jobs/{job_id}"
    r = requests.get(url)
    r.raise_for_status()
    job = r.json()
    ead = get_ead(client, job["app_id"])

    try:
        class_ids = validate_classes_of_inputs(job, ead, mds_url)
    except requests.HTTPError as e:
        error_msg = e.response
        raise ValidationError(e) from e

    try:
        for input_key, input_id in job["inputs"].items():
            input_spec = ead["io"][input_key]
            input_type = input_spec["type"]
            if input_type == "wsi":
                lock_type = "slides"
            elif input_type in ALLOWED_ANNOTATION_TYPES:
                lock_type = "annotations"
            elif input_type in ALLOWED_PRIMITIVE_TYPES:
                lock_type = "primitives"
            elif input_type == "class":
                lock_type = "classes"
            elif input_type == "collection":
                lock_type = "collections"
            r = requests.put(f"{mds_url}/v3/jobs/{job_id}/lock/{lock_type}/{input_id}")
            r.raise_for_status()
        if class_ids:
            for class_id in class_ids:
                r = requests.put(f"{mds_url}/v3/jobs/{job_id}/lock/classes/{class_id}")
                r.raise_for_status()
    except requests.HTTPError as e:
        msg = r.text
        error_msg = f"Could not lock input_id [{input_id}] of type [{input_type}] to job. Error: {msg}"
        raise Exception(error_msg) from e


def validate_classes_of_inputs(job, ead, mds_url):
    creator_id = job["creator_id"]
    valid_ead_classes = []
    if "classes" in ead:
        valid_ead_classes = get_ead_classes_recursive(f"{ead['namespace']}", "classes", ead["classes"])
    classes_to_lock = []
    input_keys = ead["modes"][job["mode"].lower()]["inputs"]
    for key, value in ead["io"].items():
        if key not in input_keys:
            continue
        else:
            temp_classes = validate_ead_input_classes(value, job["inputs"][key], creator_id, valid_ead_classes, mds_url)
            if temp_classes:
                classes_to_lock.extend(temp_classes)
    return classes_to_lock


def get_ead_classes_recursive(base_name: str, class_key, class_node):
    base_name = f"{base_name}.{class_key}"
    class_values = []
    if "name" in class_node:
        class_values.append(base_name)
    else:
        for key, value in class_node.items():
            class_values.extend(get_ead_classes_recursive(base_name, key, value))
    return class_values


def validate_ead_input_classes(partial_input_ead, input_id, scope_id, ead_classes, mds_url):
    class_ids = []
    if "classes" in partial_input_ead:
        annotation = get_annotation(input_id, mds_url)
        if len(annotation["classes"]) == 0:
            raise HTTPError("Class constraint for annotation not fullfilled")
        valid_classes = get_valid_class_values_for_constraint(ead_classes, partial_input_ead["classes"])
        for annot_class in annotation["classes"]:
            if annot_class["value"] in valid_classes and annot_class["creator_id"] == scope_id:
                class_ids.append(annot_class["id"])
        if len(class_ids) == 0:
            raise HTTPError("Class constraint for annotation not fullfilled")
    if partial_input_ead["type"] == "collection":
        collection = get_collection(input_id, mds_url)
        for item in collection["items"]:
            ids = validate_ead_input_classes(partial_input_ead["items"], item["id"], scope_id, ead_classes, mds_url)
            class_ids.extend(ids)
    return class_ids


def get_valid_class_values_for_constraint(ead_class_values, class_values_contraints):
    valid_class_values = []
    for value in class_values_contraints:
        resolved_class_values = [cl for cl in ead_class_values if value in cl]
        if resolved_class_values:
            valid_class_values.extend(resolved_class_values)
        else:
            valid_class_values.append(value)
    return valid_class_values
