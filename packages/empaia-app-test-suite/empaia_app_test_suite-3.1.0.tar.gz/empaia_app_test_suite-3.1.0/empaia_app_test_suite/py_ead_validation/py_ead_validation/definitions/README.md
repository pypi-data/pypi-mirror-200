# Definitions

## EAD

* EMPAIA App Description (EAD) JSON-Schema files
  * used for validation of EAD files provided by EMPAIA compatible apps

### Schema Validation Process

The schema validation must not be performed against a schema that is hosted online. Instead services that perform schema validation include this repository as a git submodule and use the given resources offline.

App developers can include an online link or file path to a schema file in their EAD to enable automatic schema validation and code completion in their code editor. EMPAIA services will parse the link URL or path to only use the name of the file. Based on the file name an offline validation is performed.

The following rules apply based on the `ead-settings.json` file:

* For **new apps** that are developed using the EMPAIA App Test Suite (EATS) and that are uploaded to the EMPAIA Marketplace only schemas listed as `allowed` will be considered for validation.
* For **legacy apps** that are already included in the EMPAIA Marketplace additional schemas listed as `allowed_legacy` will be considered for validation. Supported legacy apps can still be executed in the platform.
* For schemas that have been renamed a name lookup is done in the `mappings` section.

For a Python code example of the schema validation process see https://gitlab.com/empaia/integration/py-ead-validation

## Namespaces

* JSON files defining the content of EMPAIA global namespaces
  * class definitions that can be used by any app
