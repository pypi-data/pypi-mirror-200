# Py EAD Validation

## Code Style

```bash
sudo apt update
sudo apt install python3-venv python3-pip
cd py-ead-validation
python3 -m venv .venv
source .venv/bin/activate
poetry install
```

```bash
isort .
black .
pycodestyle .
pylint .
```

## Usage

### Command Line Interface

```bash
$ python -m py_ead_validation -h
usage: __main__.py [-h] [--config-file CONFIG_FILE] [--enable-legacy-support] ead_file ead_schema_dir namespaces_dir ead_settings_file

EAD Validator

positional arguments:
  ead_file              Path to an EAD file to be validated
  ead_schema_dir        Path to a directory containing EAD schema files
  namespaces_dir        Path to a directory containing namespace files
  ead_settings_file     Path to an ead-settings file

optional arguments:
  -h, --help            show this help message and exit
  --config-file CONFIG_FILE
                        Path to a config file that should additionally be validated against the given EAD
  --enable-legacy-support
                        Include allowed legacy schemas
```

### Python Package

#### EAD v1 (draft-3)

```python
from py_ead_validation.ead_validator import validate_ead, validate_ead_with_config


ead = {
    "$schema": "https://developer.empaia.org/schema/ead-schema.v1-draft3.json",
    "name": "Test App",
    "name_short": "TestApp",
    "namespace": "org.empaia.vendor_name.ta.v1",
    "description": "EAD for testing purposes",
    "configuration": {
        "threshold": {
            "type": "float",
            "storage": "global",
            "optional": True,
        },
        "count": {
            "type": "integer",
            "storage": "global",
            "optional": False,
        }
    },
    "inputs": {
        "my_wsi": {"type": "wsi"},
        "my_rectangle": {
            "type": "rectangle",
            "reference": "inputs.my_wsi",
            "classes": ["org.empaia.global.v1.classes.roi"],
        },
    },
    "outputs": {
        "my_rectangle": {
            "type": "rectangle",
            "reference": "inputs.my_wsi",
        },
        "my_classification": {"type": "class", "reference": "outputs.my_rectangle"},
    },
}

# raises EadValidationError unless compliant
validate_ead(ead)

# raises EadValidationError unless compliant but including legacy EAD versions
validate_ead(ead, enable_legacy_support=True)

# EADs with configuration section can be validated together with a given config
config = {"threshold": 0.75, "count": 3}

# can raise EadValidationError or ConfigValidationError
# ...either without legacy EAD version support
validate_ead_with_config(ead, config)
# ...or with legacy EAD version support
validate_ead_with_config(ead, config, enable_legacy_support=True)

# configs must match exactly the ead's configuration section
validate_ead_with_config(ead, {"threshold": True, "count": 3}) # ConfigValidationError (wrong type)
validate_ead_with_config(ead, {"something": 42, "count": 100}) # ConfigValidationError (unrelated entry)
validate_ead_with_config(ead, {"threshold": 0.75})             # ConfigValidationError (missing entry)
```

#### EAD v3

```python
from py_ead_validation.ead_validator import validate_ead, validate_ead_with_config


ead = {
    "$schema": "https://gitlab.com/empaia/integration/definitions/-/raw/main/ead/ead-schema.v3.json",
    "name": "Test App",
    "name_short": "TestApp",
    "namespace": "org.empaia.vendor_name.ta.v3.0",
    "description": "EAD for testing purposes",
    "configuration": {
        "global": {
            "threshold": {
                "type": "float",
                "optional": True,
            },
        },
        "customer": {
            "count": {
                "type": "integer",
                "optional": False,
            },
        },
    },
    "io": {
        "my_wsi": {"type": "wsi"},
        "my_rectangle": {
            "type": "rectangle",
            "reference": "io.my_wsi",
            "classes": ["org.empaia.global.v1.classes.roi"],
        },
        "my_classification": {"type": "class", "reference": "io.my_rectangle"},
    },
    "modes": {
        "standalone": {
            "inputs": ["my_wsi", "my_rectangle"],
            "outputs": ["my_classification"],
        },
    },
}

# raises EadValidationError unless compliant
validate_ead(ead)

# raises EadValidationError unless compliant but including legacy EAD versions
validate_ead(ead, enable_legacy_support=True)

# EADs with configuration section can be validated together with a given config.
# You can omit sections that you don't want to validate. Empty but given sections
# are treated as empty configurations and are validated.
config = {"global": {"threshold": 0.75}, "customer": {"count": 3}}  # validates both
config = {"global":  {"threshold": 0.68}}                           # only validates global
config = {"customer": {"count": 42}}                                # only validates customer

# can raise EadValidationError or ConfigValidationError
# ...either without legacy EAD version support
validate_ead_with_config(ead, config)
# ...or with legacy EAD version support
validate_ead_with_config(ead, config, enable_legacy_support=True)

# configs must match exactly the ead's configuration section
validate_ead_with_config(ead, {"global": {"threshold": True}, "customer": {"count": 3}})  # ConfigValidationError (wrong type of threshold)
validate_ead_with_config(ead, {"global": {"something": 42}, "customer": {"count": 100}})  # ConfigValidationError (unrelated entry in global)
validate_ead_with_config(ead, {"global": {}, "customer": {}})                              # ConfigValidationError (missing entry in customer - global's threshold is optional)
```

#### Job Validation (only supported for EAD v3 or later)

```python
from py_ead_validation.job_validator import JobValidator

# job is a dictionary conforming to the Job v3 specification
# ead is a dictionary conforming to the EAD v3 specification

async def validate_job_with_ead(job, ead):
    # MDS_URL points to a valid Medical Data Service API host
    # http_client is a valid empaia-sender-auth compatible client
    validator = JobValidator(MDS_URL, http_client)

    await validator.validate_inputs(job, ead)
    await validator.validate_outputs(job, ead)
```
