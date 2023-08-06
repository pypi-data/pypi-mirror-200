# 0.3.25

* remove unused customer portal app model

# 0.3.24

* updated post models for App Service v3 API
* removed Annotation Service Core models from v3 API

# 0.3.23

* refactored v3 annotation service post models

# 0.3.22

* added resized image model to portal app

# 0.3.21

* minor codestyle change due to black update

# 0.3.20

* removed optional from tag model

# 0.3.19

* added cleanrance filter to public portal app query

# 0.3.18

* v3/examinations.py:
  * added app_id to Scope model (only for returned Scope, not PostScope)
  * added scopes and jobs to ExaminationsQuery

# 0.3.17

* remove ead from v3 job model

# 0.3.16

* updated customer query model

# 0.3.15

* add support for validation status in query

# 0.3.14

* fix PostJob validator

# 0.3.13

* added validation status and error message fields

# 0.3.12

* added query and admin post model for app views

# 0.3.11

* updated job mode and validation

# 0.3.10

* app configs are now mandatory fields and default to empty dict
* `research_only`defaults to false

# 0.3.9

* updated app view model and ui configuration

# 0.3.8

* renamed PortalAppPreview to AppView
* removed redundant ExtendedConfiguration and renamed AppConfig property names

# 0.3.7

* new ExtendedConfiguration model

# 0.3.6

* renamed AppUiState model to AppUiStorage

# 0.3.4

* added AppUiState model

# 0.3.3

* updated app config (global and customer)

# 0.3.2

* updated marketplace models

# 0.3.1

* removed deprecated models (needed for result tree in WBC 1.0) from v3

# 0.3.0

* Refactor ServiceStatus
  * Changes model
  * excluded from api versions (lives on top level, is not part of empaia API specifications)
* Added v3 models
  * changes to examination only containing one app

# 0.2.2

* moved accesstokentools into own utils folder

# 0.2.1

* added missing annotation models to `\v2` folder

# 0.2.0

* Refactoring to serve models for multiple API versions
* Models before preprocessing feature gone to `v1` folder
* Models for Preprocessing apps `/v2` folder
* `access_token_tools` extensions from `0.1.26` are in both versions

# 0.1.26

* re-introduced old `access_token_tools.ceate_token(subject: str ...)`
* added another method `access_token_tools.create_token_from_dict()...)`
