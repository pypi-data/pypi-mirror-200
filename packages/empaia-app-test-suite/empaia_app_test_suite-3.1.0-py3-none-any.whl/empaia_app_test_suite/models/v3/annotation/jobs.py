from pydantic import Field

from ..commons import Id, RestrictedBaseModel


class JobLock(RestrictedBaseModel):
    item_id: Id = Field(
        example="b10648a7-340d-43fc-a2d9-4d91cc86f33f",
        description="ID of the locked element",
    )
    job_id: Id = Field(
        example="b10648a7-340d-43fc-a2d9-4d91cc86f33f",
        description="ID of the job the element was locked for",
    )
