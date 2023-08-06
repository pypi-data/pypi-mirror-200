import requests

from empaia_app_test_suite.constants import STATIC_ORGANIZATION_ID


def aaa_post_organization(aaa_url, data):
    url = f"{aaa_url}/api/v2/custom-mock/organization"
    r = requests.post(url, json=data)
    return r


def generate_organization_json(name: str):
    data = {
        "organization_id": STATIC_ORGANIZATION_ID,
        "organization_name": name,
        "logo_url": "https://upload.wikimedia.org/wikipedia/commons/c/ca/Microscope_icon_%28black_OCL%29.svg",
    }
    return data
