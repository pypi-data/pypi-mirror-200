"""
This modules defines different concepts that are used in the Job Service, in particular
the Job Request, which is used for creating a Job, and the Job itself, which extends
the Job Request with additional attributes on the job's current status.
"""

from enum import Enum
from typing import Dict, List, Optional

from pydantic import UUID4, Field, conlist, validator

from .commons import Id, ItemCount, Progress, RestrictedBaseModel, Timestamp


class JobStatus(str, Enum):
    """Current status of a Job"""

    NONE = "NONE"  # unknown status
    ASSEMBLY = "ASSEMBLY"  # Job being assembled in the WBS'
    READY = "READY"  # Assembly done, can be passed to JES
    SCHEDULED = "SCHEDULED"  # scheduled for execution
    RUNNING = "RUNNING"  # currently running
    COMPLETED = "COMPLETED"  # completed with return code == 0
    FAILED = "FAILED"  # completed with return code != 0
    TIMEOUT = "TIMEOUT"  # process killed after Request timeout
    ERROR = "ERROR"  # indicating error with job executor, i.e. outside of app
    INCOMPLETE = "INCOMPLETE"  # Job finished, but not all non-optional outputs are set


class JobCreatorType(str, Enum):
    """Type of Job Creator"""

    USER = "USER"
    SCOPE = "SCOPE"
    SERVICE = "SERVICE"
    # AUTOMATIC = "AUTOMATIC"
    # SOLUTION = "SOLUTION"  # post-MVP


class JobMode(str, Enum):
    """Mode of Job"""

    STANDALONE = "STANDALONE"
    PREPROCESSING = "PREPROCESSING"
    POSTPROCESSING = "POSTPROCESSING"
    REPORT = "REPORT"


class JobValidationStatus(str, Enum):
    """Status of job validation"""

    NONE = "NONE"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"


# MODELS FOR JOB SERVICE


class PostJob(RestrictedBaseModel):
    """This is sent by the workbench-service to the job-service to request the creation of a new Job.
    The full EAD has to be submitted before the Job is created; Job-Inputs are added after creation.
    """

    app_id: UUID4 = Field(
        ...,
        example="b10648a7-340d-43fc-a2d9-4d91cc86f33f",
        description="The ID of the app to start, including the exact version of the app",
    )

    creator_id: Id = Field(
        ...,
        example="b10648a7-340d-43fc-a2d9-4d91cc86f33f",
        description="ID of the scope or user, that created the job",
    )

    creator_type: JobCreatorType = Field(
        ...,
        example=JobCreatorType.SCOPE,
        description="The type of creator that created the job. This can be a scope or a user (only for WBS v1)",
    )

    mode: JobMode = Field(
        default="STANDALONE",
        example=JobMode.STANDALONE,
        description="The mode of the job corresponding to a mode in the EAD",
    )

    containerized: bool = Field(
        default=True,
        example=True,
        description="Whether this job uses a container or not (postprocessing only)",
    )

    @validator("mode")
    def validate_mode(cls, mode, values):
        mode_validation_rules = {
            JobMode.PREPROCESSING: [{"key": "creator_type", "allowed_values": [JobCreatorType.SERVICE]}],
            JobMode.REPORT: [{"key": "creator_type", "allowed_values": [JobCreatorType.SCOPE]}],
            JobMode.POSTPROCESSING: [
                {
                    "key": "creator_type",
                    "allowed_values": [JobCreatorType.SCOPE],
                }
            ],
            JobMode.STANDALONE: [
                {"key": "creator_type", "allowed_values": [JobCreatorType.USER, JobCreatorType.SCOPE]}
            ],
        }

        if mode in mode_validation_rules:
            validators = mode_validation_rules[mode]
            for v in validators:
                if values[v["key"]] not in v["allowed_values"]:
                    raise ValueError(f"{v['key']} {values[v['key']]} for mode {mode} not allowed")

        return mode

    @validator("containerized")
    def validate_containerized(cls, containerized, values):
        if not containerized:
            assert "mode" not in values or values["mode"] in [JobMode.POSTPROCESSING, JobMode.REPORT]
        return containerized


class Job(PostJob):
    """This describes the actual job and is a superset of the job-request, adding status parameters that are added
    after the job has been created, such as the access-token, but also status-information and references to the created
    output.
    """

    id: UUID4 = Field(
        example="a10648a7-340d-43fc-a2d9-4d91cc86f33f",
        description="The unique ID of the job, set by the database",
    )

    inputs: Dict[str, str] = Field(
        example={
            "first_input": "c10648a7-340d-43fc-a2d9-4d91cc86f33f",
        },
        description="Data references to input parameters, added after job creation",
    )

    outputs: Dict[str, str] = Field(
        example={
            "first_output": "d10648a7-340d-43fc-a2d9-4d91cc86f33f",
        },
        description="Data references to output values, added when the job is being executed",
    )

    status: JobStatus = Field(
        example=JobStatus.RUNNING,
        description="The current status of the job",
    )

    created_at: Timestamp = Field(
        example=1623349180,
        description="Time when the job was created",
    )

    started_at: Optional[Timestamp] = Field(
        example=1623359180,
        description="Time when execution of the job was started",
    )

    progress: Optional[Progress] = Field(example=0.5, description="The progress of the job between 0.0 and 1.0")

    ended_at: Optional[Timestamp] = Field(
        example=1623369180,
        description="Time when the job was completed or when it failed",
    )

    runtime: Optional[int] = Field(
        example=1234,
        description="Time in seconds the job is running (if status RUNNING) or was running (if status COMPLETED)",
    )

    error_message: Optional[str] = Field(
        example="Error 123: Parameters could not be processed",
        description="Optional error message in case the job failed",
    )

    input_validation_status: JobValidationStatus = Field(
        default=JobValidationStatus.NONE,
        example=JobValidationStatus.ERROR,
        description="Validation status for the job inputs",
    )

    input_validation_error_message: Optional[str] = Field(
        example="Input key does not match specification in EAD",
        description="Optional error message in case the input validation failed",
    )

    output_validation_status: JobValidationStatus = Field(
        default=JobValidationStatus.NONE,
        example=JobValidationStatus.RUNNING,
        description="Validation status for the job outputs",
    )

    output_validation_error_message: Optional[str] = Field(
        example="Output key does not match specification in EAD",
        description="Optional error message in case the output validation failed",
    )


class JobList(RestrictedBaseModel):
    """Job query result."""

    item_count: ItemCount = Field(
        example=1,
        description="Number of Jobs as queried without skip and limit applied",
    )

    items: List[Job] = Field(
        example=[
            Job(
                id="a10648a7-340d-43fc-a2d9-4d91cc86f33f",
                app_id="b10648a7-340d-43fc-a2d9-4d91cc86f33f",
                creator_id="c10648a7-340d-43fc-a2d9-4d91cc86f33f",
                creator_type=JobCreatorType.SCOPE,
                inputs={"first_input": "d10648a7-340d-43fc-a2d9-4d91cc86f33f"},
                outputs={},
                status=JobStatus.ASSEMBLY,
                created_at=1623349180,
            )
        ],
        description="List of Job items as queried with skip and limit applied",
    )


class JobQuery(RestrictedBaseModel):
    """Query for one or more Jobs by Status, creator, and others.
    Jobs have to match _any_ of the values in _all_ the provided fields.
    """

    statuses: Optional[conlist(JobStatus, min_items=1)] = Field(
        example=[JobStatus.ASSEMBLY, JobStatus.READY],
        description="List of job status values",
    )

    apps: Optional[conlist(UUID4, min_items=1)] = Field(
        example=[
            "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
        ],
        description="List of app IDs",
    )

    creators: Optional[conlist(Id, min_items=1)] = Field(
        example=[
            "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
        ],
        description="List of job creator IDs",
    )

    creator_types: Optional[conlist(JobCreatorType, min_items=1)] = Field(
        example=[JobCreatorType.SCOPE, JobCreatorType.SERVICE], description="List of job creator type values"
    )

    jobs: Optional[conlist(UUID4, min_items=1)] = Field(
        example=[
            "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
            "b10648a7-340d-43fc-a2d9-4d91cc86f33f",
        ],
        description="List of job IDs",
    )

    modes: Optional[conlist(JobMode, min_items=1)] = Field(
        example=["PREPROCESSING", "POSTPROCESSING"], description="List of job modes"
    )

    input_validation_statuses: Optional[conlist(JobValidationStatus, min_items=1)] = Field(
        example=[JobValidationStatus.NONE, JobValidationStatus.RUNNING],
        description="List of input validation status values",
    )

    output_validation_statuses: Optional[conlist(JobValidationStatus, min_items=1)] = Field(
        example=[JobValidationStatus.NONE, JobValidationStatus.RUNNING],
        description="List of output validation status values",
    )


class JobToken(RestrictedBaseModel):
    """Wrapper for Job-ID and Access Token, returned on Job creation."""

    job_id: UUID4 = Field(
        example="a10648a7-340d-43fc-a2d9-4d91cc86f33f",
        description="The ID of the newly created job corresponding to the token",
    )

    access_token: str = Field(
        example="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI3NTYzMDAxOC03ZjhmLTQ3YjgtODZmNC0wMTliODhjNjZhMTEiLCJle"
        "HAiOjE2MjQzNTkwNTZ9.CnT0NYwVzyNl05Jp0z4W-qDqKjolQHZxmT9i7SYyBYG6D-5K7jLxm3l4lBLp30rnjYOiZm0TtvskK1lYDh"
        "gKNyXnEhB_O7f6DQuTd9tn8yv8XnK19pj6g8nubFfBho9lYhComb6a3XX3vqLK5pnaXuhC9tFdzsnLkQPoIi2DZ8E",
        description="Access-Token used for accessing the actual data; passed to app by JES. and further to App-Service "
        "to validate authenticity of the job; decodes as {'sub': <job-id>, 'exp': <time>}.",
    )


class PutJobStatus(RestrictedBaseModel):
    """Wrapper for a status and an optional error message."""

    status: JobStatus = Field(
        ...,
        example=JobStatus.FAILED,
        description="The new status of the job",
    )

    error_message: Optional[str] = Field(
        example="Error 123: Parameters could not be processed",
        description="Optional error message in case of FAILED status",
    )


class PutJobProgress(RestrictedBaseModel):
    """Wrapper for a progress update"""

    progress: Progress = Field(
        ...,
        example=0.75,
        description="The new value for the job's progress",
    )


class PutJobValidationStatus(RestrictedBaseModel):
    """Wrapper for a validation status and an optional error message."""

    validation_status: JobValidationStatus = Field(
        example=JobValidationStatus.ERROR,
        description="The new validation status",
    )

    error_message: Optional[str] = Field(
        example="Reference does not match correct type",
        description="Optional error message in case of ERROR status",
    )
