STATIC_USER_ID = "02792914-0eb0-4c72-a896-a4de43f0371a"
STATIC_CASE_ID = "e5087613-ac4b-4bf9-9d0e-dd37917c3277"
STATIC_ORGANIZATION_ID = "71b77ced-f41e-46e5-a1f2-b9729e60ce54"

ALLOWED_ANNOTATION_TYPES = [
    "point",
    "line",
    "arrow",
    "rectangle",
    "polygon",
    "circle",
]

ALLOWED_PRIMITIVE_TYPES = ["integer", "float", "bool", "string"]

JOB_MODES = {"standalone": "STANDALONE", "preprocessing": "PREPROCESSING", "postprocessing": "POSTPROCESSING"}

SERVICE_API_MAPPING = {
    "workbench-service": "wbs-api",
    "medical-data-service": "mds-api",
    "job-execution-service": "jes-api",
    "app-service": "app-api",
    "marketplace-service-mock": "mps-api",
    "aaa-service-mock": "aaa-api",
    "workbench-client-v3": "wbc-v3",
    "workbench-client-v3-sample-ui": "sample-app-ui",
    "workbench-client-v3-generic-ui": "generic-app-ui",
}


# CLI help texts

# Services
VERSION_HELP = "Shows eats version"
WSI_MOUNT_POINTS_FILE_HELP = (
    "Path to JSON file containing mount point mappings of local WSI storage dirs (keys) "
    "to be mounted in WSI Service container dirs (values)."
)
BUILD_HELP = "Force to build new nginx custom image (needed if nginx port has changed)"
PULL_HELP = "Force to pull service images"
GPU_HELP = "Enable GPU utilization for containerized app."
GPU_DRIVER_HELP = "GPU driver to use for App images, e.g. 'nvidia' (default: no GPU)"
TRIALS_SERVICES_HELP = "Number of times to try connecting to all services"
WBS_PORT_HELP = "Listen port of workbench-service container"
WBS_URL_HELP = "URL used by workbench-client-v3 to access workbench-service (enables custom hosting setups)"
WBC3_PORT_HELP = "Listen port of workbench-client-v3 container"
NGINX_PORT_HELP = "Listen port of nginx container"
ISYNTAX_SDK_HELP = "Full path to philips-pathologysdk-2.0-ubuntu18_04_py36_research.zip for isyntax support"
VOLUME_PREFIX_HELP = "Prefix for the names of the container volumes holding service state"
DOCKER_CONFIG_FILE_HELP = (
    "Docker config file. E.g. to pass proxy configuration to the apps by the job-execution-service."
)
FRONTEND_TOKEN_EXP = "Expiration time in seconds of frontend token (needed to retrieve app ui from workbench service)"
SCOPE_TOKEN_EXP = (
    "Expiration time in seconds of scope token (needed to send or retrieve app data to / from workbench service)"
)
FRAME_ANCENSTORS_HELP = (
    "Content security policy to set allowed frame ancestors for App UI iframes (e.g., http://localhost:8888)"
)
CONNECT_SOURCE_HELP = "Content security policy to set allowed connect sources for App UI iframes (e.g., 'self')"
DISABLE_CSP_HELP = (
    "Disable enforcement of Content Security Policy (CSP) settings for App UI iframes. "
    "Cannot be used in combination with '--app-ui-connect-src' or '--app-ui-frame-ancestors'"
)

# Apps
EAD_FILE_HELP = "Path to EMPAIA App Description (EAD) JSON file."
DOCKER_IMAGE_HELP = (
    "Local docker image name or registry url, e.g. registry.gitlab.com/empaia/integration"
    "/sample-apps/v3/org-empaia-vendor_name-tutorial_app_01:v3.0"
)
GLOBAL_CONFIG_FILE_HELP = (
    "Path to a JSON file containing the global configuration items (e.g., API secrets) if defined in the EAD"
)
CUSTOMER_CONFIG_FILE_HELP = (
    "Path to a JSON file containing the customer configuration items (e.g., user credentials) if defined in the EAD"
)
APP_UI_URL_HELP = "URL and Port of App specific UI to use in WBC 3.0 (e.g., http://host.docker.internal:4300)"
APP_UI_CONFIG_FILE_HELP = "Path to a JSON file containing the app ui configuration"


# Jobs
APP_ID_HELP = "ID of previously registered App."
INPUT_DIR_HELP = "Path to job input dir"
OUTPUT_DIR_HELP = "Path to job output dir"
JOB_MODE = "Mode of job (must be mode declared in EAD 'modes' section)"
PREPROCESSING_JOB_ID = (
    "EMPAIA_JOB_ID of a previously COMPLETED preprocessing job. "
    "Can be used if outputs of a preprocessing job should be used as inputs for a postprocessing job. "
    "Only supported if the job mode is declared as 'postprocessing' and "
    "the preprocessing job was created using the SAME app id as the new postprocessing job."
)

# Cases
CASE_DESC_HELPER = "Description of case shown in Workbench Client"


# Slides
SLIDE_FILE_HELP = (
    "JSON file containing a [path] defined in WSI_MOUNT_POINTS_FILE "
    "and optionally also [id], [tissue], [stain], [block]"
)


# Lists
LIST_BORDER_OPTION = "Add borders to the list ouput"
LIST_FORMAT = "Select another output format (json, markdown, html)"
APP_LIST_OPTION = "Only output APP IDs list without a heading"
JOB_LIST_OPTION = "Only output JOB IDs list without a heading"
SLIDE_LIST_OPTION = "Only output SlIDE IDs list without a heading"
CASE_LIST_OPTION = "Only output CASE IDs list without a heading"
