import json
from enum import Enum
from sqlite3 import Timestamp
from typing import Dict, List, Optional, Union

from pydantic import UUID4, Field, StrictBool, StrictFloat, StrictInt, StrictStr, conint, conlist, constr

from ..commons import RestrictedBaseModel

ItemCount = conint(ge=0)

VersionConstraint = constr(regex=r"^(\d+\.)?(\d+\.)?(\d+\.)(\*|\d+)$")

ConfigurationModel = Dict[StrictStr, Union[StrictStr, StrictInt, StrictFloat, StrictBool]]


config_section_example = {
    "some_token": "secret-token",
    "some_flag": True,
    "some_parameter": 42,
    "some_other_param": 42.5,
}


class AppMediaPurpose(str, Enum):
    PEEK = "peek"
    BANNER = "banner"
    WORKFLOW = "workflow"
    MANUAL = "manual"


class ListingStatus(str, Enum):
    LISTED = "LISTED"
    DELISTED = "DELISTED"
    ADMIN_DELISTED = "ADMIN_DELISTED"
    DRAFT = "DRAFT"


class AppStatus(str, Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    PENDING = "PENDING"
    DRAFT = "DRAFT"


class ApiVersion(str, Enum):
    V1 = "v1"
    V2 = "v2"
    V3 = "v3"


class Language(str, Enum):
    DE = "DE"
    EN = "EN"


class AppConfigurationType(str, Enum):
    GLOBAL = "global"
    CUSTOMER = "customer"


class Browser(str, Enum):
    FIREFOX = "firefox"
    CHROME = "chrome"
    EDGE = "edge"
    SAFARI = "safari"


class OS(str, Enum):
    Win10 = "win10"
    Win11 = "win11"
    Linux = "linux"
    MacOS = "macOS"


class TextTranslation(RestrictedBaseModel):
    lang: Language = Field(example=Language.EN, description="Language abbreviation")
    text: str = Field(example="Some text", description="Translated tag name")


class PostAppTag(RestrictedBaseModel):
    tag_group: str = Field(example="TISSUE", description="Tag group. See definitions for valid tag groups.")
    tag_name: str = Field(example="SKIN", description="Tag name. See definitions for valid tag names.")


class AppTag(RestrictedBaseModel):
    name: str = Field(example="SKIN", description="Tag name. See definitions for valid tag names.")
    tag_translations: List[TextTranslation]


class TagList(RestrictedBaseModel):
    tissues: List[AppTag] = Field(default=[], description="List of tissues")
    stains: List[AppTag] = Field(default=[], description="List of stains")
    indications: List[AppTag] = Field(default=[], description="List of indications")
    analysis: List[AppTag] = Field(default=[], description="List of analysis")
    clearances: List[AppTag] = Field(default=[], description="List of market clearances / certifications")


class MediaMetadata(RestrictedBaseModel):
    caption: Optional[Dict[str, str]] = Field(
        example={"EN": "Description in english", "DE": "Beschreibung auf Deutsch"}, description="Caption"
    )
    alternative_text: Optional[Dict[str, str]] = Field(
        example={"EN": "Description in english", "DE": "Beschreibung auf Deutsch"}, description="Alternative text"
    )

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class ResizedMediaUrlsObject(RestrictedBaseModel):
    w60: Optional[str] = Field(
        default=None,
        example="https://url.to/image_w60",
        description="Presigned url to the media object with max width 60px",
    )
    w400: Optional[str] = Field(
        default=None,
        example="https://url.to/image_w400",
        description="Presigned url to the media object with max width 400px",
    )
    w800: Optional[str] = Field(
        default=None,
        example="https://url.to/image_w800",
        description="Presigned url to the media object with max width 800x",
    )
    w1200: Optional[str] = Field(
        default=None,
        example="https://url.to/image_w1200",
        description="Presigned url to the media object with max width 1200px",
    )


class MediaObjectCore(RestrictedBaseModel):
    index: int = Field(
        example=2, description="Number of the step, required when media purpose is 'PREVIEW', 'BANNER' or 'WORKFLOW"
    )
    caption: Optional[List[TextTranslation]] = Field(description="Media caption")
    alt_text: Optional[List[TextTranslation]] = Field(
        description="Alternative text for media",
    )
    internal_path: str = Field(example="/internal/path/to", description="Internam Minio path")
    content_type: str = Field(example="image/jpeg", description="Content type of the media object")
    presigned_media_url: Optional[str] = Field(
        example="https://url.to/image", description="Presigned url to the media object"
    )
    resized_presigned_media_urls: Optional[ResizedMediaUrlsObject] = Field(
        description="Resized versions of an image media object"
    )


class MediaObject(MediaObjectCore):
    id: UUID4 = Field(example="b10648a7-340d-43fc-a2d9-4d91cc86f33f", description="Media ID")


PostMediaObject = MediaObjectCore


class MediaList(RestrictedBaseModel):
    peek: List[MediaObject] = Field(default=[], description="Peek media")
    banner: List[MediaObject] = Field(default=[], description="Banner media")
    workflow: List[MediaObject] = Field(default=[], description="Workflow media")
    manual: List[MediaObject] = Field(default=[], description="Manual media")


# App UI Config


# CSP - unsafe-inline and unsafe-eval policy settings for supported *-src csp directives
class AppUiConfigSrcPolicies(RestrictedBaseModel):
    unsafe_inline: Optional[bool] = Field(
        example=True, description="Set unsafe-inline for App-UI code if set to 'true'."
    )
    unsafe_eval: Optional[bool] = Field(example=True, description="Set unsafe-eval for App-UI code if set to 'true'.")


class AppUiCspConfiguration(RestrictedBaseModel):
    script_src: Optional[AppUiConfigSrcPolicies] = Field(description="CSP script-src setting for App-UIs.")
    style_src: Optional[AppUiConfigSrcPolicies] = Field(description="CSP style-src setting for App-UIs.")
    font_src: Optional[AppUiConfigSrcPolicies] = Field(description="CSP font-src setting for App-UIs.")


class AppUiIframeConfiguration(RestrictedBaseModel):
    allow_popups: Optional[bool] = Field(
        example=True, description="Set to 'true' if an App UI is allowed to redirect in external popup."
    )


class AppUiTested(RestrictedBaseModel):
    browser: Browser = Field(example=Browser.CHROME, description="App UI tested for browser")
    version: VersionConstraint = Field(example="102.32.552", description="App UI tested for browser version")
    os: OS = Field(example=OS.Win11, description="App UI tested on operating system")


class AppUiConfiguration(RestrictedBaseModel):
    csp: Optional[AppUiCspConfiguration] = Field(description="CSP settings for App-UIs.")
    iframe: Optional[AppUiIframeConfiguration] = Field(description="Iframe settings for App-UIs.")
    tested: Optional[List[AppUiTested]] = Field(description="Tested combination of browser and OS for an App UI.")

    # ORM mode needs to be set to true, to allow posting dictionaries as form data
    class Config:
        orm_mode = True


# App


class AppDetailsCore(RestrictedBaseModel):
    name: str = Field(example="PD-L1 Quantifier", description="Qualified app name displayed in the portal")


class PostAppDetails(AppDetailsCore):
    description: Dict[str, str] = Field(
        example={"EN": "Description in english", "DE": "Beschreibung auf Deutsch"}, description="Description"
    )


class AppDetails(AppDetailsCore):
    marketplace_url: str = Field(example="http://url.to/store", description="Url to app in the marketplace")
    description: List[TextTranslation] = Field(description="Description")


class PostApp(RestrictedBaseModel):
    ead: Optional[dict] = Field(example={}, description="EAD content of the app")
    registry_image_url: Optional[str] = Field(
        example="https://registry.gitlab.com/empaia/integration/ap_xyz",
        description="Url to the container image in the registry",
    )
    app_ui_url: Optional[str] = Field(example="http://app1.emapaia.org", description="Url where the app UI is located")
    app_ui_configuration: Optional[AppUiConfiguration] = Field(example={}, description="App UI configuration")


class PostAdminApp(PostApp):
    id: Optional[UUID4] = Field(
        default=None, example="b10648a7-340d-43fc-a2d9-4d91cc86f33f", description="External ID of the app"
    )


class PostActiveAdminApps(RestrictedBaseModel):
    v1: Optional[PostAdminApp] = Field(description="App for EAD v1-darft3 without App UI (WBC 1.0)")
    v2: Optional[PostAdminApp] = Field(description="App for EAD v1-darft3 with App UI (WBC 2.0)")
    v3: Optional[PostAdminApp] = Field(description="App for EAD v3")


class PublicApp(PostApp):
    id: UUID4 = Field(example="b10648a7-340d-43fc-a2d9-4d91cc86f33f", description="ID of the app")
    version: Optional[str] = Field(example="v1.2", description="Version of the app")
    has_frontend: bool = Field(example=True, description="If true, app is shipped with a frontend")


class ClosedApp(PublicApp):
    status: AppStatus = Field(example=AppStatus.DRAFT, description="Status of the app")
    portal_app_id: UUID4 = Field(example="b10648a7-340d-43fc-a2d9-4d91cc86f33f", description="ID of the portal app")
    creator_id: str = Field(example="b10648a7-340d-43fc-a2d9-4d91cc86f33f", description="Creator ID")
    created_at: Timestamp = Field(example=1598611645, description="UNIX timestamp in seconds - set by server")
    updated_at: Timestamp = Field(example=1598611645, description="UNIX timestamp in seconds - set by server")


# Portal App View


class AppViewCore(RestrictedBaseModel):
    non_functional: Optional[bool] = Field(
        example=False,
        default=False,
        description="If true, portal app can be listed although technical app is not yet available",
    )
    research_only: bool = Field(
        example=False,
        default=False,
        description="If true, app is intended to be used for reasearch only",
    )


class PostAdminAppView(AppViewCore):
    details: Optional[PostAppDetails]
    tags: Optional[List[PostAppTag]]
    app: PostAdminApp


class PublicAppView(AppViewCore):
    version: Optional[str] = Field(example="v1.2", description="Version of the currently active app")
    details: Optional[AppDetails]
    media: Optional[MediaList]
    tags: Optional[TagList]
    created_at: Timestamp = Field(example=1598611645, description="UNIX timestamp in seconds - set by server")
    reviewed_at: Optional[Timestamp] = Field(
        example=1598611645, description="UNIX timestamp in seconds - set by server"
    )


class PublicActiveAppViews(RestrictedBaseModel):
    v1: Optional[PublicAppView] = Field(description="App view for EAD v1-darft3 without App UI (WBC 1.0)")
    v2: Optional[PublicAppView] = Field(description="App view for EAD v1-darft3 with App UI (WBC 2.0)")
    v3: Optional[PublicAppView] = Field(description="App view for EAD v3")


class ClosedAppView(PublicAppView):
    id: UUID4 = Field(example="b10648a7-340d-43fc-a2d9-4d91cc86f33f", description="ID of the app view")
    portal_app_id: UUID4 = Field(example="b10648a7-340d-43fc-a2d9-4d91cc86f33f", description="ID of the portal app")
    organization_id: str = Field(example="b10648a7-340d-43fc-a2d9-4d91cc86f33f", description="Organization ID")
    status: AppStatus = Field(example=AppStatus.DRAFT, descritpion="Status of the app")
    app: Optional[ClosedApp]
    creator_id: str = Field(example="b10648a7-340d-43fc-a2d9-4d91cc86f33f", description="ID of the app view creator")
    review_comment: Optional[str] = Field(
        example="Review comment", description="Review commet, i.e. in case of rejection"
    )
    api_version: ApiVersion = Field(example=ApiVersion.V1, description="Supported API version by this app view")
    reviewer_id: Optional[str] = Field(example="b10648a7-340d-43fc-a2d9-4d91cc86f33f", description="ID of the reviewer")


class ClosedActiveAppViews(RestrictedBaseModel):
    v1: Optional[ClosedAppView] = Field(description="App view for EAD v1-darft3 without App UI (WBC 1.0)")
    v2: Optional[ClosedAppView] = Field(description="App view for EAD v1-darft3 with App UI (WBC 2.0)")
    v3: Optional[ClosedAppView] = Field(description="App view for EAD v3")


# Portal App


class PostAdminPortalApp(RestrictedBaseModel):
    id: Optional[UUID4] = Field(example="b10648a7-340d-43fc-a2d9-4d91cc86f33f", description="Portal App ID")
    organization_id: str = Field(
        example="b10648a7-340d-43fc-a2d9-4d91cc86f33f", description="ID of the organization providing the portal app"
    )
    status: Optional[ListingStatus] = Field(
        example=ListingStatus.LISTED, description="Listing status of the portal app"
    )
    details: Optional[PostAppDetails]
    active_apps: Optional[PostActiveAdminApps] = Field(description="Active apps for portal app")
    tags: Optional[List[PostAppTag]]
    research_only: Optional[bool] = Field(
        example=False,
        default=False,
        description="If true, app is intended to be used for reasearch only",
    )
    non_functional: Optional[bool] = Field(
        example=False,
        default=False,
        description="If true, portal app can be listed although technical app is not yet available",
    )


class PortalAppCore(RestrictedBaseModel):
    id: UUID4 = Field(example="b10648a7-340d-43fc-a2d9-4d91cc86f33f", description="ID of the portal app")
    organization_id: str = Field(
        example="b10648a7-340d-43fc-a2d9-4d91cc86f33f", description="ID of the organization providing the portal app"
    )
    status: ListingStatus = Field(example=ListingStatus.DRAFT, descritpion="Status of the app")
    creator_id: str = Field(example="b10648a7-340d-43fc-a2d9-4d91cc86f33f", description="Creator ID")
    created_at: Timestamp = Field(example=1598611645, description="UNIX timestamp in seconds - set by server")
    updated_at: Timestamp = Field(example=1598611645, description="UNIX timestamp in seconds - set by server")


class PublicPortalApp(PortalAppCore):
    active_app_views: Optional[PublicActiveAppViews] = Field(description="Currently active app views")


class ClosedPortalApp(PortalAppCore):
    id: UUID4 = Field(example="b10648a7-340d-43fc-a2d9-4d91cc86f33f", description="ID of the portal app")
    active_app_views: Optional[ClosedActiveAppViews] = Field(description="Currently active app views")


class PublicPortalAppList(RestrictedBaseModel):
    item_count: ItemCount = Field(example=123, description="Count of all available apps")
    items: List[PublicPortalApp]


class ClosedPortalAppList(RestrictedBaseModel):
    item_count: ItemCount = Field(example=123, description="Count of all available apps")
    items: List[ClosedPortalApp]


# Queries


class BaseQuery(RestrictedBaseModel):
    pass


class PortalAppQuery(BaseQuery):
    active_app_version: Optional[ApiVersion] = Field(
        example=ApiVersion.V3, description="Filter option for active app version"
    )
    tissues: Optional[List[str]] = Field(example=["SKIN", "BREAST"], description="Filter option for tissue types")
    stains: Optional[List[str]] = Field(example=["HE", "PHH3"], description="Filter option for stain types")
    indications: Optional[List[str]] = Field(
        example=["MELANOMA", "PROSTATE_CANCER"], description="Filter option for indication types"
    )
    analysis: Optional[List[str]] = Field(
        example=["GRADING", "QUANTIFICATION"], description="Filter option for analysis types"
    )
    clearances: Optional[List[str]] = Field(
        example=["CE_IVD", "CE_IVDR"], description="Filter option for clearance/certification types"
    )


class CustomerPortalAppQuery(BaseQuery):
    apps: Optional[List[str]] = Field(example=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"], description="List of app IDs")
    tissues: Optional[List[str]] = Field(example=["SKIN", "BREAST"], description="Filter option for tissue types")
    stains: Optional[List[str]] = Field(example=["HE", "PHH3"], description="Filter option for stain types")


class AdminPortalAppQuery(PortalAppQuery, CustomerPortalAppQuery):
    statuses: Optional[List[AppStatus]] = Field(example=[AppStatus.DRAFT], description="Filter option for app status")
    creators: Optional[List[str]] = Field(example=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"])


class CustomerAppViewQuery(BaseQuery):
    apps: conlist(UUID4, min_items=1) = Field(
        example=["b10648a7-340d-43fc-a2d9-4d91cc86f33f"], description="List of app IDs"
    )
    api_versions: Optional[List[ApiVersion]] = Field(
        example=[ApiVersion.V1], description="List of supported API versions"
    )


# App Configuratuin


class PostAppConfiguration(RestrictedBaseModel):
    content: ConfigurationModel = Field(
        example={"secret1": "value", "secret2": 100}, description="Dictionary of key-value-pairs"
    )


class AppConfiguration(RestrictedBaseModel):
    app_id: str = Field(example="b10648a7-340d-43fc-a2d9-4d91cc86f33f", description="App ID")
    global_: ConfigurationModel = Field(
        default={},
        example=config_section_example,
        description="Global app configuration as dictionary of key-value-pairs",
        alias="global",
    )
    customer: ConfigurationModel = Field(
        default={},
        example=config_section_example,
        description="Customer app configuration as dictionary of key-value-pairs",
    )
