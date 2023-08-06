import json
from importlib import import_module
from pathlib import Path

from .exceptions import JobValidationError


class JobValidator:
    def __init__(self, mds_url, http_client):
        self.mds_url = mds_url
        self.http_client = http_client
        ead_settings = self._load_settings()
        self.name_mappings = ead_settings["mappings"]

    @staticmethod
    def _load_settings():
        definitions_dir_path = Path(__file__).parent.resolve() / "definitions"
        ead_settings_path = definitions_dir_path / "ead-settings.json"
        with open(ead_settings_path, encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def _import_custom_validation_module_by_schema(schema_name):
        schema_stem = Path(schema_name).stem
        package_name = schema_stem.replace("-", "_")
        package_name = package_name.replace(".", "_")
        try:
            # we need to do it that complicated in order to let
            # this code work also in submodule usage of the library
            parent_package_name = ".".join(__name__.split(".")[:-1])
            result = import_module(f".indepth.{package_name}.job", parent_package_name)
            return result
        except ModuleNotFoundError as e:
            raise JobValidationError(f"No custom Job validation module found for {schema_name}") from e

    @staticmethod
    def _get_schema_name(ead):
        return ead["$schema"].split("/")[-1]

    def _import_custom_validation_module(self, ead):
        schema_name = self._get_schema_name(ead)
        if schema_name in self.name_mappings:
            schema_name = self.name_mappings[schema_name]
        return self._import_custom_validation_module_by_schema(schema_name)

    async def validate_inputs(self, job, ead):
        validation_module = self._import_custom_validation_module(ead)
        await validation_module.validate_inputs(job, ead, self.mds_url, self.http_client)

    async def validate_outputs(self, job, ead):
        validation_module = self._import_custom_validation_module(ead)
        await validation_module.validate_outputs(job, ead, self.mds_url, self.http_client)
