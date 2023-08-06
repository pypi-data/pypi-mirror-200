import json
from datetime import datetime
from uuid import uuid4

from empaia_app_test_suite.py_ead_validation.py_ead_validation.ead_validator import (
    validate_ead,
    validate_ead_with_customer_config,
    validate_ead_with_global_config,
)
from empaia_app_test_suite.py_ead_validation.py_ead_validation.exceptions import (
    ConfigValidationError,
    EadSchemaValidationError,
    EadValidationError,
)
from empaia_app_test_suite.utils.utils_commons import ValidationError


def generate_app_json(ead: dict, docker_registry: str, organization: dict, app_ui_url: str):
    now = str(datetime.now())
    _idx = ead["namespace"].rfind(".")
    version = ead["namespace"][_idx - 2 :]

    data = {
        "id": str(uuid4()),
        "organization_id": organization["organization_id"],
        "status": "LISTED",
        "creator_id": str(uuid4()),
        "created_at": now,
        "updated_at": now,
        "active_app_views": {
            "v3": {
                "version": version,
                "api_version": "v3",
                "details": {
                    "name": ead["name"],
                    "marketplace_url": "http://url.to/store",
                    "description": [
                        {"lang": "DE", "text": ead["description"]},
                    ],
                },
                "media": {"peek": [], "banner": [], "workflow": [], "manual": []},
                "tags": {"tissues": [], "stains": [], "indications": [], "analysis": [], "clearances": []},
                "id": str(uuid4()),
                "non_functional": False,
                "research_only": False,
                "portal_app_id": str(uuid4()),
                "organization_id": organization["organization_id"],
                "status": "APPROVED",
                "creator_id": str(uuid4()),
                "created_at": now,
                "review_comment": "Test comment",
                "reviewer_id": str(uuid4()),
                "reviewed_at": now,
                "app": {
                    "ead": ead,
                    "registry_image_url": docker_registry,
                    "app_ui_url": app_ui_url,
                    "id": str(uuid4()),
                    "version": version,
                    "status": "APPROVED",
                    "has_frontend": bool(app_ui_url),
                    "portal_app_id": str(uuid4()),
                    "creator_id": str(uuid4()),
                    "created_at": now,
                    "updated_at": now,
                },
            },
        },
    }

    return data


def validate_app_ead(ead: dict):
    try:
        validate_ead(ead)
    except EadSchemaValidationError as e:
        error = "Validation of EAD failed: EAD does not match schema."
        raise ValidationError(error) from e
    except EadValidationError as e:
        error = f"Validation of EAD failed: {e}"
        raise ValidationError(error) from e


def validate_configuration_parameters(ead: dict, global_config_file: str, customer_config_file: str):
    global_config = None
    customer_config = None

    if global_config_file is not None:
        with open(global_config_file, "r", encoding="utf-8") as f:
            global_config = json.load(f)

        try:
            validate_ead_with_global_config(ead, config=global_config)
        except EadValidationError as e:
            error = f"Validation of EAD failed: {e}"
            raise ValidationError(error) from e
        except ConfigValidationError as e:
            error = f"Validation of global configuration failed: {e}"
            raise ValidationError(error) from e

    if customer_config_file is not None:
        with open(customer_config_file, "r", encoding="utf-8") as f:
            customer_config = json.load(f)

        try:
            validate_ead_with_customer_config(ead, config=customer_config)
        except EadValidationError as e:
            error = f"Validation of EAD failed: {e}"
            raise ValidationError(error) from e
        except ConfigValidationError as e:
            error = f"Validation of customer configuration failed: {e}"
            raise ValidationError(error) from e

    return global_config, customer_config
