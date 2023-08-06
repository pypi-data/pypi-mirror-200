from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class RestrictedBaseModel(BaseModel):
    """Abstract Super-class not allowing unknown fields in the **kwargs."""

    class Config:
        extra = "forbid"


class ServiceStatusEnum(str, Enum):
    OK = "ok"
    FAILURE = "failure"


class ServiceStatus(RestrictedBaseModel):
    status: ServiceStatusEnum = Field(example=ServiceStatusEnum.OK.value, description="Status of service")
    version: str = Field(example="0.3.7", description="Version of service")
    message: Optional[str] = Field(
        example="Database offline", description="Message describing the status further if needed"
    )
