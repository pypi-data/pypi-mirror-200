import requests

from empaia_app_test_suite.constants import STATIC_USER_ID
from empaia_app_test_suite.utils.utils_commons import get_service_url
from empaia_app_test_suite.utils.utils_print import PrintStep


def cases_register(client, description: str = None):
    mds_url = get_service_url(client=client, service_name="medical-data-service")

    case = {
        "description": description if description else "A very interesting example case",
        "deleted": True,
        "creator_id": STATIC_USER_ID,
        "creator_type": "USER",
    }

    with PrintStep("Create Case"):
        r = requests.post(f"{mds_url}/private/v3/cases", json=case)
        r.raise_for_status()
        case = r.json()

    return case


def cases_list(client):
    mds_url = get_service_url(client=client, service_name="medical-data-service")
    r = requests.get(f"{mds_url}/v3/cases")
    r.raise_for_status()
    return r.json()
