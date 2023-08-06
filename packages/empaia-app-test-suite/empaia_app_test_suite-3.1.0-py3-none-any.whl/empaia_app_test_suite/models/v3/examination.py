from enum import Enum
from typing import Dict, List, Optional, Union

from pydantic import UUID4, Field, StrictBool, StrictFloat, StrictInt, constr

from .commons import Id, ItemCount, RestrictedBaseModel, Timestamp


class ExaminationState(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


class PutExaminationState(RestrictedBaseModel):
    state: ExaminationState = Field(example=ExaminationState.CLOSED, description="Examination state")


class ExaminationCreatorType(str, Enum):
    USER = "USER"
    SERVICE = "SERVICE"


class PostExamination(RestrictedBaseModel):
    case_id: str = Field(example="b10648a7-340d-43fc-a2d9-4d91cc86f33f", description="Case ID")
    app_id: str = Field(example="b10648a7-340d-43fc-a2d9-4d91cc86f33f", description="App ID")
    creator_id: str = Field(example="b10648a7-340d-43fc-a2d9-4d91cc86f33f", description="Creator ID")
    creator_type: ExaminationCreatorType = Field(example=ExaminationCreatorType.USER, description="Creator Type")


class Examination(PostExamination):
    id: UUID4 = Field(example="b10648a7-340d-43fc-a2d9-4d91cc86f33f", description="Examination ID")
    state: ExaminationState = Field(example=ExaminationState.OPEN, description="Examination state")
    created_at: Timestamp = Field(example=1598611645, description="UNIX timestamp in seconds - set by server")
    updated_at: Timestamp = Field(example=1598611645, description="UNIX timestamp in seconds - set by server")
    jobs: List[Id] = Field(
        example=[
            "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
        ],
        description="Jobs in this examination",
    )


class ExaminationList(RestrictedBaseModel):
    item_count: ItemCount = Field(example=12345, description="Count of items")
    items: List[Examination]


class ExaminationQuery(RestrictedBaseModel):
    cases: Optional[List[Id]] = Field(
        example=[
            "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            "839ba097-f265-4ba0-9412-4b93eea0e6e2",
        ],
        description="Case IDs",
    )
    apps: Optional[List[Id]] = Field(
        example=[
            "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            "839ba097-f265-4ba0-9412-4b93eea0e6e2",
        ],
        description="App IDs",
    )
    creators: Optional[List[Id]] = Field(
        example=[
            "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            "839ba097-f265-4ba0-9412-4b93eea0e6e2",
        ],
        description="Creator IDs",
    )
    scopes: Optional[List[Id]] = Field(
        example=[
            "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            "839ba097-f265-4ba0-9412-4b93eea0e6e2",
        ],
        description="Scope IDs",
    )
    jobs: Optional[List[Id]] = Field(
        example=[
            "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            "839ba097-f265-4ba0-9412-4b93eea0e6e2",
        ],
        description="Job IDs",
    )
    creator_types: Optional[List[ExaminationCreatorType]] = Field(
        example=[ExaminationCreatorType.USER], description="Examination Creator Type"
    )


class PostScope(RestrictedBaseModel):
    examination_id: UUID4 = Field(example="6b30c43c-eb97-448a-9f8e-15fc0da569f0", description="Examination ID")
    user_id: Id = Field(example="02621dcb-e208-449f-9d44-868d092223cf", description="User ID")


class Scope(PostScope):
    id: UUID4 = Field(example="b10648a7-340d-43fc-a2d9-4d91cc86f33f", description="Scope ID")
    app_id: Id = Field(example="77cf6909-6926-45d1-be5d-168ae1eb2dc6", description="App ID")
    created_at: Timestamp = Field(example=1598611645, description="UNIX timestamp in seconds - set by server")


class ScopeToken(RestrictedBaseModel):
    """Wrapper for Scope-ID and Access Token, returned on Scope creation and access."""

    access_token: str = Field(
        example="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI3NTYzMDAxOC03ZjhmLTQ3YjgtODZmNC0wMTliODhjNjZhMTEiLCJle"
        "HAiOjE2MjQzNTkwNTZ9.CnT0NYwVzyNl05Jp0z4W-qDqKjolQHZxmT9i7SYyBYG6D-5K7jLxm3l4lBLp30rnjYOiZm0TtvskK1lYDh"
        "gKNyXnEhB_O7f6DQuTd9tn8yv8XnK19pj6g8nubFfBho9lYhComb6a3XX3vqLK5pnaXuhC9tFdzsnLkQPoIi2DZ8E",
        description="AccessToken based on JSON Web Tokens. It can be created and passed around to validate requests",
    )


class ProprocessingTriggerCreatorType(str, Enum):
    USER = "USER"


class PostPreprocessingTrigger(RestrictedBaseModel):
    creator_id: str = Field(example="b10648a7-340d-43fc-a2d9-4d91cc86f33f", description="Creator ID")
    creator_type: ProprocessingTriggerCreatorType = Field(
        example=ProprocessingTriggerCreatorType.USER, description="Creator Type"
    )
    portal_app_id: Id = Field(example="b10648a7-340d-43fc-a2d9-4d91cc86f33f", description="Portal App ID")
    tissue: str = Field(example="LUNG", description="Tissue Type")
    stain: str = Field(example="HE", description="Stain Type")


class PreprocessingTrigger(PostPreprocessingTrigger):
    id: UUID4 = Field(example="6b30c43c-eb97-448a-9f8e-15fc0da569f0", description="Preprocessing Trigger ID")


class PreprocessingTriggerList(RestrictedBaseModel):
    item_count: ItemCount = Field(example=123, description="Count of items")
    items: List[PreprocessingTrigger]


class PreprocessingRequestCreatorType(str, Enum):
    USER = "USER"


class PostPreprocessingRequest(RestrictedBaseModel):
    creator_id: str = Field(example="b10648a7-340d-43fc-a2d9-4d91cc86f33f", description="Creator ID")
    creator_type: PreprocessingRequestCreatorType = Field(
        example=PreprocessingRequestCreatorType.USER, description="Creator Type"
    )
    slide_id: Id = Field(example="446fda31-2525-48a3-8aff-f845a9589e3c", description="Slide ID")


class PreprocessingRequestState(str, Enum):
    OPEN = "OPEN"
    PROCESSED = "PROCESSED"


class AppJob(RestrictedBaseModel):
    app_id: Id = Field(example="77cf6909-6926-45d1-be5d-168ae1eb2dc6", description="App ID")
    job_id: Id = Field(example="36adca29-b05e-4b87-adf7-78a2b2b78636", description="Job ID")
    trigger_id: Id = Field(example="be61d865-65a1-4138-a206-e2576c14d7ee", description="Trigger ID")


class PreprocessingRequest(PostPreprocessingRequest):
    id: UUID4 = Field(example="f3510b90-d641-44f2-abba-0e614987f821", description="Preprocessing Request ID")
    app_jobs: List[AppJob] = Field(
        example=[
            {
                "app_id": "1a894ba2-e466-44eb-a7bd-bbe1822478c0",
                "job_id": "ccd23315-bce9-409d-a852-66c63dc438fd",
                "trigger_id": "ac0d0b47-cc0b-439a-9e8d-34c1681a325e",
            },
            {
                "app_id": "c711e821-1189-4ee7-9ef0-7582f4a8707a",
                "job_id": "56ae5103-b5d9-4aaf-8fcd-d5d13f0d82c9",
                "trigger_id": "388af081-969d-4ef2-bc7f-84b81aeb4052",
            },
        ],
        description="List of triggered app jobs",
    )
    created_at: Timestamp = Field(example=1598611645, description="UNIX timestamp in seconds - set by server")
    updated_at: Timestamp = Field(example=1598611645, description="UNIX timestamp in seconds - set by server")
    state: PreprocessingRequestState = Field(
        example=PreprocessingRequestState.OPEN, description="Preprocessing request state"
    )


class PreprocessingRequestList(RestrictedBaseModel):
    item_count: ItemCount = Field(example=123, description="Count of items")
    items: List[PreprocessingRequest]


class PreprocessingRequestQuery(RestrictedBaseModel):
    states: Optional[List[PreprocessingRequestState]] = Field(
        example=[PreprocessingRequestState.OPEN], description="List of preprocessing request states"
    )


class PutPreprocessingRequestUpdate(RestrictedBaseModel):
    app_jobs: List[AppJob] = Field(
        example=[
            {
                "app_id": "1a894ba2-e466-44eb-a7bd-bbe1822478c0",
                "job_id": "ccd23315-bce9-409d-a852-66c63dc438fd",
                "trigger_id": "ac0d0b47-cc0b-439a-9e8d-34c1681a325e",
            },
            {
                "app_id": "c711e821-1189-4ee7-9ef0-7582f4a8707a",
                "job_id": "56ae5103-b5d9-4aaf-8fcd-d5d13f0d82c9",
                "trigger_id": "388af081-969d-4ef2-bc7f-84b81aeb4052",
            },
        ],
        description="List of triggered app jobs",
    )


StrAppUiStorage = constr(max_length=10000, strict=True)


AppUiStorageContent = Dict[StrAppUiStorage, Union[StrAppUiStorage, StrictInt, StrictFloat, StrictBool]]


class AppUiStorage(RestrictedBaseModel):
    content: AppUiStorageContent = Field(
        example={"key1": "val1", "key2": 42}, description="Dictionary of key-value-pairs"
    )
