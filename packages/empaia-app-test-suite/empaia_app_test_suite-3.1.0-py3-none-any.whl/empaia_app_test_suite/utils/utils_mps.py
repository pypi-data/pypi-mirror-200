import requests

from empaia_app_test_suite.constants import STATIC_ORGANIZATION_ID
from empaia_app_test_suite.utils.utils_commons import get_service_url


def get_mps_apps_list(client):
    headers = {"organization-id": STATIC_ORGANIZATION_ID}
    mps_url = get_service_url(client=client, service_name="marketplace-service-mock")
    r = requests.put(f"{mps_url}/v1/customer/portal-apps/query", json={}, headers=headers)
    r.raise_for_status()
    return r.json()


def mps_post_app(mps_url, data):
    url = f"{mps_url}/v1/custom-mock/portal-apps"
    r = requests.post(url, json=data)
    return r


def register_global_config(app_id: str, global_config: str, mps_url):
    url = f"{mps_url}/v1/custom-mock/apps/{app_id}/config/global"
    r = requests.put(url, json=global_config)
    r.raise_for_status()


def register_customer_config(app_id: str, organization_id: str, customer_config: str, mps_url):
    url = f"{mps_url}/v1/custom-mock/apps/{app_id}/config/customer/{organization_id}"
    r = requests.put(url, json=customer_config)
    r.raise_for_status()


def register_app_ui_url(app_id: str, app_ui_url: str, mps_url):
    url = f"{mps_url}/v1/custom-mock/apps/{app_id}/app-ui-url"
    r = requests.put(url, json={"app_ui_url": app_ui_url})
    r.raise_for_status()


def register_app_ui_configuration(app_id: str, app_ui_config: dict, mps_url):
    url = f"{mps_url}/v1/custom-mock/apps/{app_id}/app-ui-config"
    r = requests.put(url, json=app_ui_config)
    r.raise_for_status()


def get_ead(client, app_id):
    mps_url = get_service_url(client=client, service_name="marketplace-service-mock")
    url = f"{mps_url}/v1/customer/apps/{app_id}"
    headers = {"organization-id": STATIC_ORGANIZATION_ID}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    app = r.json()
    return app["ead"]


def get_app(client, app_id):
    mps_url = get_service_url(client=client, service_name="marketplace-service-mock")
    url = f"{mps_url}/v1/customer/apps/{app_id}"
    headers = {"organization-id": STATIC_ORGANIZATION_ID}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    app = r.json()
    return app
