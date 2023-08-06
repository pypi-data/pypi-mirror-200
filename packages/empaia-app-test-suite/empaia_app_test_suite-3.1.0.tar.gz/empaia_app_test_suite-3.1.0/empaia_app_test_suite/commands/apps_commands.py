import json

import requests
from requests.exceptions import HTTPError

from empaia_app_test_suite.commands.helper.app_helper import (
    generate_app_json,
    validate_app_ead,
    validate_configuration_parameters,
)
from empaia_app_test_suite.constants import STATIC_ORGANIZATION_ID
from empaia_app_test_suite.utils.utils_aaa import aaa_post_organization, generate_organization_json
from empaia_app_test_suite.utils.utils_commons import ValidationError, get_service_url
from empaia_app_test_suite.utils.utils_mps import (
    mps_post_app,
    register_app_ui_configuration,
    register_app_ui_url,
    register_customer_config,
    register_global_config,
)
from empaia_app_test_suite.utils.utils_print import PrintStep


def apps_register(
    client,
    ead,
    docker_image,
    global_config_file=None,
    customer_config_file=None,
    app_ui_url=None,
    app_ui_config_file=None,
):
    mps_url = get_service_url(client=client, service_name="marketplace-service-mock")
    aaa_url = get_service_url(client=client, service_name="aaa-service-mock")

    with PrintStep("Validate EAD"):
        validate_app_ead(ead)
    with PrintStep("Validate configuration"):
        global_config, customer_config = validate_configuration_parameters(
            ead, global_config_file, customer_config_file
        )
    if len(client.images.list(name=docker_image)) == 0:
        with PrintStep(f"Pull image {docker_image}"):
            client.images.pull(docker_image)
    else:
        with PrintStep("Image found on host system"):
            pass
    with PrintStep("Register app"):
        aaa_orga = generate_organization_json(name="placeholder")
        aaa_post_organization(aaa_url, aaa_orga)
        mps_app = generate_app_json(ead, docker_image, aaa_orga, app_ui_url)
        mps_post_app(mps_url, mps_app)
        app_id = mps_app["active_app_views"]["v3"]["app"]["id"]
    if global_config_file:
        with PrintStep("Register global configuration"):
            try:
                register_global_config(app_id, global_config, mps_url)
            except HTTPError as e:
                error = f"Validation of global configuration failed: {e}"
                raise ValidationError(error) from e
    if customer_config_file:
        with PrintStep("Register customer configuration"):
            try:
                register_customer_config(app_id, STATIC_ORGANIZATION_ID, customer_config, mps_url)
            except HTTPError as e:
                error = f"Validation of global configuration failed: {e}"
                raise ValidationError(error) from e
    if app_ui_config_file:
        with PrintStep("Register app-ui configuration"):
            with open(app_ui_config_file, "r", encoding="utf-8") as f:
                app_ui_config = json.load(f)
            try:
                register_app_ui_configuration(app_id, app_ui_config, mps_url)
            except HTTPError as e:
                error = f"Validation of app ui configuration failed: {e}"
                raise ValidationError(error) from e

    return mps_app


def apps_update(
    client,
    app_id,
    global_config_file=None,
    customer_config_file=None,
    app_ui_url=None,
    app_ui_config_file=None,
):
    mps_url = get_service_url(client=client, service_name="marketplace-service-mock")

    with PrintStep("Checking if App exists"):
        app = requests.get(f"{mps_url}/v1/customer/apps/{app_id}", headers={"organization-id": STATIC_ORGANIZATION_ID})
        if not app:
            raise ValidationError(f"App with id '{app_id}' does not exist!")
        ead = app.json()["ead"]

    with PrintStep("Validate configuration"):
        global_config, customer_config = validate_configuration_parameters(
            ead, global_config_file, customer_config_file
        )
    if global_config_file:
        with PrintStep("Register global configuration"):
            try:
                register_global_config(app_id, global_config, mps_url)
            except HTTPError as e:
                error = f"Validation of global configuration failed: {e}"
                raise ValidationError(error) from e
    if customer_config_file:
        with PrintStep("Register customer configuration"):
            try:
                register_customer_config(app_id, STATIC_ORGANIZATION_ID, customer_config, mps_url)
            except HTTPError as e:
                error = f"Validation of global configuration failed: {e}"
                raise ValidationError(error) from e
    if app_ui_url:
        with PrintStep("Register app-ui url"):
            try:
                register_app_ui_url(app_id, app_ui_url, mps_url)
            except HTTPError as e:
                error = f"Validation of app ui url failed: {e}"
                raise ValidationError(error) from e
    if app_ui_config_file:
        with PrintStep("Register app-ui configuration"):
            with open(app_ui_config_file, "r", encoding="utf-8") as f:
                app_ui_config = json.load(f)
            try:
                register_app_ui_configuration(app_id, app_ui_config, mps_url)
            except HTTPError as e:
                error = f"Validation of app ui configuration failed: {e}"
                raise ValidationError(error) from e
