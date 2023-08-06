from fastapi.exceptions import HTTPException

from ...exceptions import JobValidationError, JobValidationPreconditionError

_ANNOTATION_TYPES = ["point", "rectangle", "circle", "polygon", "arrow", "line"]
_PRIMITIVE_TYPES = ["integer", "float", "bool", "string"]


async def validate_inputs(job, ead, mds_url, http_client):
    validator = _Validator(job, ead, mds_url, http_client)
    validator.assert_suitable_status_for_input_validation()
    validator.assert_all_inputs_present()
    validator.assert_no_additional_inputs_present()
    await validator.assert_all_inputs_compliant()


async def validate_outputs(job, ead, mds_url, http_client):
    validator = _Validator(job, ead, mds_url, http_client)
    validator.assert_suitable_status_for_output_validation()
    validator.assert_all_outputs_present()
    validator.assert_no_additional_outputs_present()
    await validator.assert_all_outputs_compliant()


class _Validator:
    def __init__(self, job, ead, mds_url, http_client):
        self._job = job
        self._ead = ead
        self._mds_url = mds_url
        self._http_client = http_client
        self._cache = {}

    def assert_suitable_status_for_input_validation(self):
        if self._job["status"] not in ["READY", "SCHEDULED", "RUNNING", "COMPLETED", "ERROR"]:
            raise JobValidationPreconditionError("Input validation requires at least READY status")

    def assert_suitable_status_for_output_validation(self):
        if self._job["status"] not in ["COMPLETED", "ERROR"]:
            raise JobValidationPreconditionError("Output validation requires a terminal status")
        if self._job["status"] != "COMPLETED":
            raise JobValidationError("no validation performed due to job error state")

    def assert_all_inputs_present(self):
        self._assert_all_items_present("input")

    def assert_all_outputs_present(self):
        self._assert_all_items_present("output")

    def assert_no_additional_inputs_present(self):
        self._assert_no_additional_items_present("input")

    def assert_no_additional_outputs_present(self):
        self._assert_no_additional_items_present("output")

    async def assert_all_inputs_compliant(self):
        await self._assert_all_items_compliant("input")

    async def assert_all_outputs_compliant(self):
        await self._assert_all_items_compliant("output")

    def _assert_all_items_present(self, i_or_o):
        ead_items = self._ead["modes"][self._job["mode"].lower()][f"{i_or_o}s"]
        for item_name in ead_items:
            if item_name not in self._job[f"{i_or_o}s"]:
                raise JobValidationError(f"Missing {i_or_o} {item_name} in job")

    def _assert_no_additional_items_present(self, i_or_o):
        mode_lower = self._job["mode"].lower()
        ead_items = self._ead["modes"][mode_lower][f"{i_or_o}s"]
        for item_name in self._job[f"{i_or_o}s"]:
            if item_name not in ead_items:
                raise JobValidationError(f"{item_name} not defined as {i_or_o} in EAD in {mode_lower} mode")

    async def _assert_all_items_compliant(self, i_or_o):
        for item_name in self._job[f"{i_or_o}s"]:
            item_id = self._job[f"{i_or_o}s"][item_name]
            item_spec = self._ead["io"][item_name]
            await self._assert_item_compliant(item_name, item_id, item_spec, i_or_o)

    async def _assert_item_compliant(self, item_name, item_id, item_spec, i_or_o):
        if item_spec["type"] == "wsi":
            item_data = await self._get_slide(item_id, item_name)
        elif item_spec["type"] in _ANNOTATION_TYPES:
            item_data = await self._get_annotation(item_id, item_name)
        elif item_spec["type"] in _PRIMITIVE_TYPES:
            item_data = await self._get_primitive(item_id, item_name)
        elif item_spec["type"] == "class":
            item_data = await self._get_class(item_id, item_name)
        elif item_spec["type"] == "collection":
            item_data = await self._get_shallow_collection(item_id, item_name)
        await self._assert_item_data_compliant(item_name, item_data, item_spec, i_or_o)

    async def _assert_item_data_compliant(self, item_name, item_data, item_spec, i_or_o):
        reference = self._get_reference(item_spec)
        if item_spec["type"] == "wsi":
            pass  # nothing to check for now
        if item_spec["type"] in _ANNOTATION_TYPES:
            await self._assert_annotation_compliant(item_data, item_name, item_spec, reference, i_or_o)
        elif item_spec["type"] in _PRIMITIVE_TYPES:
            await self._assert_primitive_compliant(item_data, item_name, item_spec, reference, i_or_o)
        elif item_spec["type"] == "class":
            await self._assert_class_compliant(item_data, item_name, item_spec, reference, i_or_o)
        elif item_spec["type"] == "collection":
            await self._assert_collection_compliant(item_data, item_name, item_spec, reference, i_or_o)

    async def _assert_annotation_compliant(self, annotation, item_name, item_spec, reference, i_or_o):
        self._assert_type_matches(annotation, item_name, item_spec)
        if i_or_o == "input":
            await self._assert_class_constraints_met(annotation, item_name, item_spec)
        else:
            self._assert_creator_suitable(annotation, item_name)
        if reference:
            await self._assert_reference_matches_spec(item_name, reference, annotation)

    async def _assert_primitive_compliant(self, primitive, item_name, item_spec, reference, i_or_o):
        self._assert_type_matches(primitive, item_name, item_spec)
        if i_or_o == "output":
            self._assert_creator_suitable(primitive, item_name)
        if reference:
            await self._assert_reference_matches_spec(item_name, reference, primitive)

    async def _assert_class_compliant(self, klass, item_name, item_spec, reference, i_or_o):
        class_value = klass["value"]
        if class_value != "org.empaia.global.v1.classes.roi":
            class_value_split = class_value.split(".classes.")
            if len(class_value_split) != 2:
                raise JobValidationError(f"{item_name} class value is malformed")
            namespace, hierarchy = class_value_split
            hierarchy = hierarchy.split(".")
            if self._ead["namespace"] != namespace:
                raise JobValidationError(f"{item_name} has illegal class namespace")
            class_node = self._ead.get("classes", {})
            for item in hierarchy:
                class_node = class_node.get(item, {})
            if not class_node:
                raise JobValidationError(f"{item_name} class value is not known in global or local namespaces")
        await self._assert_reference_matches_spec(item_name, reference, klass)
        if i_or_o == "output":
            self._assert_creator_suitable(klass, item_name)

    async def _assert_collection_compliant(self, collection, item_name, item_spec, reference, i_or_o):
        if collection["item_type"] != item_spec["items"]["type"]:
            required_type = item_spec["items"]["type"]
            raise JobValidationError(
                f"Collection {item_name} requires item type {required_type} but is {collection['item_type']}"
            )
        async for item_data in self._get_collection_items(collection["id"]):
            await self._assert_item_data_compliant(f"{item_name}", item_data, item_spec["items"], i_or_o)
        if reference:
            await self._assert_reference_matches_spec(item_name, reference, collection)
        if i_or_o == "output":
            self._assert_creator_suitable(collection, item_name)

    async def _assert_class_constraints_met(self, annotation, item_name, item_spec):
        if "classes" in item_spec:
            if "classes" not in annotation:
                # in case the annotation data was part of a collection item we need to refetch it with classes
                annotation = await self._get_annotation(annotation["id"], item_name)
            if len(annotation["classes"]) == 0:
                raise JobValidationError(
                    f"{item_name} has unmatched class constraints: {' or '.join(item_spec['classes'])}"
                )
            for klass in annotation["classes"]:
                constraints = [
                    constraint for constraint in item_spec["classes"] if klass["value"].startswith(constraint)
                ]
                if len(constraints) == 0:
                    raise JobValidationError(
                        f"{item_name} has unmatched class constraints: {' or '.join(item_spec['classes'])}"
                    )
                for constraint in constraints:
                    self._check_leaf_constraint(item_name, constraint, klass["value"])

    def _check_leaf_constraint(self, item_name, constraint, class_value):
        if class_value != "org.empaia.global.v1.classes.roi":
            leafs_spec = self._ead["classes"]
            if ".classes." in constraint:
                root = constraint.split(".classes.")[1].split(".")
                for key in root:
                    leafs_spec = leafs_spec[key]
            leafs = class_value.replace(constraint, "").split(".")[1:]
            for leaf in leafs:
                if leaf not in leafs_spec:
                    raise JobValidationError(f"{item_name} has unmatched class constraint: {constraint}")
                leafs_spec = leafs_spec[leaf]

    def _assert_type_matches(self, data, item_name, item_spec):
        if data["type"] != item_spec["type"]:
            raise JobValidationError(f"{item_name} requires type {item_spec['type']} but is {data['type']}")

    def _get_reference(self, spec):
        reference = {}
        if "reference" in spec:
            if spec["reference"].endswith(".items"):
                reference["name"] = spec["reference"][3:].split(".items")[0]
                reference["items_depth"] = spec["reference"].count(".items")
                referenced_collection = self._ead["io"][reference["name"]]
                for _ in range(reference["items_depth"]):
                    referenced_collection = referenced_collection["items"]
                reference["type"] = referenced_collection["type"]
            else:
                reference["name"] = spec["reference"][3:]
                reference["type"] = self._ead["io"][reference["name"]]["type"]
            if reference["name"] in self._job["inputs"]:
                reference["id"] = self._job["inputs"][reference["name"]]
            else:
                reference["id"] = self._job["outputs"][reference["name"]]
        return reference

    async def _assert_reference_matches_spec(self, item_name, reference, data):
        reference_name = reference["name"]
        if reference["type"] in _ANNOTATION_TYPES:
            if data["reference_type"] != "annotation":
                raise JobValidationError(f"{item_name} uses wrong reference type for {reference_name}")
        elif reference["type"] != data["reference_type"]:
            raise JobValidationError(f"{item_name} uses wrong reference type for {reference_name}")
        if "items_depth" in reference:
            cache_key = reference["id"] + str(reference["items_depth"])
            if cache_key not in self._cache:
                collected_item_ids = await self._get_nested_collection_item_ids_at_items_depth(
                    reference["id"], reference["items_depth"], reference["type"]
                )
                self._cache[cache_key] = set(collected_item_ids)
            if data["reference_id"] not in self._cache[cache_key]:
                items_depth_text = ".items" * reference["items_depth"]
                raise JobValidationError(
                    f"At least one item in {item_name} does not reference"
                    + f" any item in {reference_name}{items_depth_text}"
                )
        else:
            if reference["id"] != data["reference_id"]:
                raise JobValidationError(f"{item_name} does not reference {reference_name}")

    def _assert_creator_suitable(self, data, item_name):
        if self._job.get("containerized", True):
            if data["creator_id"] != self._job["id"]:
                raise JobValidationError(f"Creator id of {item_name} must match job id for containerized jobs")
            if data["creator_type"] != "job":
                raise JobValidationError(f"Creator type of {item_name} must be job for containerized jobs")
        else:
            if data["creator_id"] != self._job["creator_id"]:
                raise JobValidationError(
                    f"Creator id of {item_name} must match job creator id for uncontainerized jobs"
                )
            if data["creator_type"] != "scope":
                raise JobValidationError(f"Creator type of {item_name} must be scope for uncontainerized jobs")

    async def _get_slide(self, slide_id, item_name):
        try:
            return await self._http_client.get(f"{self._mds_url}/v3/slides/{slide_id}")
        except HTTPException as e:
            if e.status_code == 400:
                raise JobValidationError(f"{item_name} of type wsi not available on MDS") from e
            raise

    async def _get_annotation(self, annotation_id, item_name):
        try:
            return await self._http_client.get(
                f"{self._mds_url}/v3/annotations/{annotation_id}", params={"with_classes": True}
            )
        except HTTPException as e:
            if e.status_code == 404:
                raise JobValidationError(f"{item_name} of type annotation not available on MDS") from e
            raise

    async def _get_primitive(self, primitive_id, item_name):
        try:
            return await self._http_client.get(f"{self._mds_url}/v3/primitives/{primitive_id}")
        except HTTPException as e:
            if e.status_code == 404:
                raise JobValidationError(f"{item_name} of type primitive not available on MDS") from e
            raise

    async def _get_class(self, class_id, item_name):
        try:
            return await self._http_client.get(f"{self._mds_url}/v3/classes/{class_id}")
        except HTTPException as e:
            if e.status_code == 404:
                raise JobValidationError(f"{item_name} of type class not available on MDS") from e
            raise

    async def _get_shallow_collection(self, collection_id, item_name):
        try:
            return await self._http_client.get(
                f"{self._mds_url}/v3/collections/{collection_id}", params={"shallow": True}
            )
        except HTTPException as e:
            if e.status_code == 404:
                raise JobValidationError(f"{item_name} of type collection not available on MDS") from e
            raise

    async def _get_collection_items(self, collection_id, use_query=True):
        try:
            if use_query:
                params = {"skip": 0, "limit": 1000}
                item_list = await self._http_client.put(
                    f"{self._mds_url}/v3/collections/{collection_id}/items/query", json={}, params=params
                )
                while item_list["item_count"] > 0:
                    for item in item_list["items"]:
                        yield item
                    params["skip"] = params["skip"] + item_list["item_count"]
                    item_list = await self._http_client.put(
                        f"{self._mds_url}/v3/collections/{collection_id}/items/query", json={}, params=params
                    )
            else:
                item_list = await self._http_client.get(f"{self._mds_url}/v3/collections/{collection_id}")
                for item in item_list["items"]:
                    yield item
        except HTTPException as e:
            if e.status_code == 404:
                raise JobValidationError(f"Collection with id {collection_id} not available on MDS") from e
            raise

    async def _get_nested_collection_item_ids_at_items_depth(self, id, items_depth, items_type):
        if id not in self._cache:
            self._cache[id] = [
                item_data async for item_data in self._get_collection_items(id, use_query=(items_type != "wsi"))
            ]
        return self._collect_item_ids_recursive_at_items_depth(self._cache[id], items_depth)

    def _collect_item_ids_recursive_at_items_depth(self, items, items_depth, depth=1):
        if depth == items_depth:
            return [item["id"] for item in items]
        collected_item_ids = []
        for item in items:
            collected_item_ids += self._collect_item_ids_recursive_at_items_depth(item["items"], items_depth, depth + 1)
        return collected_item_ids
