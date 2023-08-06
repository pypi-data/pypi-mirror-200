import json
import os

import requests

from empaia_app_test_suite.constants import ALLOWED_ANNOTATION_TYPES, ALLOWED_PRIMITIVE_TYPES, SERVICE_API_MAPPING
from empaia_app_test_suite.settings import get_services
from empaia_app_test_suite.utils.utils_mds import get_collection


class ValidationError(Exception):
    pass


def get_service_url(client, service_name):
    services = get_services()
    nginx = {}
    for service in services:
        if service["name"] == "nginx":
            nginx = service
    for service in services:
        if service["name"] != service_name:
            continue
        if service["name"] in SERVICE_API_MAPPING:
            container = client.containers.get("nginx")
            internal_port = list(nginx["ports"].keys())[0]
            container_info = client.api.port(container.id, internal_port)
            host_port = container_info[0]["HostPort"]
            return f"http://127.0.0.1:{host_port}/{SERVICE_API_MAPPING[service_name]}"

        return None


def save_output_parameters(job, ead, mds_url, output_dir):
    for output_key, output_id in job["outputs"].items():
        output_type = ead["io"][output_key]["type"]
        return_data = {}
        file_name_ext = ""
        if output_type in ALLOWED_ANNOTATION_TYPES:
            r = requests.get(f"{mds_url}/v3/annotations/{output_id}")
            r.raise_for_status()
            return_data = r.json()
        elif output_type in ALLOWED_PRIMITIVE_TYPES:
            r = requests.get(f"{mds_url}/v3/primitives/{output_id}")
            r.raise_for_status()
            return_data = r.json()
        elif output_type == "collection":
            return_data = get_collection(output_id, mds_url)
        elif output_type == "class":
            r = requests.get(f"{mds_url}/v3/classes/{output_id}")
            r.raise_for_status()
            return_data = r.json()
        else:
            raise Exception("Unknown output type {output_type} for output key {output_key}.")

        with open(os.path.join(output_dir, f"{output_key}{file_name_ext}.json"), "w", encoding="utf-8") as f:
            f.write(json.dumps(clean_dict(return_data), indent=4))


def clean_dict(d):
    if not isinstance(d, (dict, list)):
        return d
    elif isinstance(d, list):
        return [v for v in (clean_dict(v) for v in d) if v is not None]
    else:
        return {k: v for k, v in ((k, clean_dict(v)) for k, v in d.items()) if v is not None}
