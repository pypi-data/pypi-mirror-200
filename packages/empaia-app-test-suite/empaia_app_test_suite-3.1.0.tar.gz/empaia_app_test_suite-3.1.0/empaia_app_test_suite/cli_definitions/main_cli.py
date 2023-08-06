import json
from pathlib import Path
from typing import Optional

import docker
import typer

import empaia_app_test_suite.constants as const
from empaia_app_test_suite import __version__
from empaia_app_test_suite.commands.apps_commands import apps_register
from empaia_app_test_suite.commands.jobs_commands import jobs_export, jobs_register, jobs_run, jobs_wait
from empaia_app_test_suite.commands.services_commands import services_down, services_up, services_wait


def init_main_cli(app):
    def version_callback(value: bool):
        if value:
            typer.echo(__version__)
            raise typer.Exit()

    @app.callback()
    def _(
        version: bool = typer.Option(
            None, "--version", callback=version_callback, is_eager=True, help=const.VERSION_HELP
        ),
    ):
        return

    @app.command("exec")
    def _(
        wsi_mount_points_file: Path = typer.Argument(..., help=const.WSI_MOUNT_POINTS_FILE_HELP),
        ead_file: Path = typer.Argument(..., help=const.EAD_FILE_HELP),
        docker_image: str = typer.Argument(..., help=const.DOCKER_IMAGE_HELP),
        input_dir: Path = typer.Argument(..., help=const.INPUT_DIR_HELP),
        output_dir: Path = typer.Argument(..., help=const.OUTPUT_DIR_HELP),
        job_mode: Optional[str] = typer.Argument("standalone", help=const.JOB_MODE),
        build: bool = typer.Option(False, "--build", help=const.BUILD_HELP),
        pull: bool = typer.Option(False, "--pull", help=const.PULL_HELP),
        docker_config: Path = typer.Option(None, "--docker-config", help=const.DOCKER_CONFIG_FILE_HELP),
        global_config_file: Path = typer.Option(None, "--global-config-file", help=const.GLOBAL_CONFIG_FILE_HELP),
        customer_config_file: Path = typer.Option(None, "--customer-config-file", help=const.CUSTOMER_CONFIG_FILE_HELP),
        nginx_port: int = typer.Option(8888, "--nginx-port", help=const.NGINX_PORT_HELP),
        wbs_url: str = typer.Option(None, "--wbs-url", help=const.WBS_URL_HELP),
        isyntax_sdk: str = typer.Option(None, "--isyntax-sdk", help=const.ISYNTAX_SDK_HELP),
        volume_prefix: str = typer.Option(None, "--volume-prefix", help=const.VOLUME_PREFIX_HELP),
        gpu_driver: str = typer.Option(None, "--gpu-driver", help=const.GPU_DRIVER_HELP),
        frontend_token_exp: int = typer.Option(60, "--frontend-token-exp", help=const.FRONTEND_TOKEN_EXP),
        scope_token_exp: int = typer.Option(300, "--scope-token-exp", help=const.SCOPE_TOKEN_EXP),
        app_ui_frame_ancestors: str = typer.Option(None, "--app-ui-frame-ancestors", help=const.FRAME_ANCENSTORS_HELP),
        app_ui_connect_src: str = typer.Option(None, "--app-ui-connect-src", help=const.CONNECT_SOURCE_HELP),
        app_ui_disable_csp: bool = typer.Option(False, "--app-ui-disable-csp", help=const.DISABLE_CSP_HELP),
    ):
        with open(wsi_mount_points_file, encoding="utf-8") as f:
            wsi_mount_points = json.load(f)

        with open(ead_file, "r", encoding="utf-8") as f:
            ead = json.load(f)

        client = docker.from_env()

        services_down(client=client, volume_prefix=volume_prefix)
        services_up(
            client=client,
            wsi_mount_points=wsi_mount_points,
            docker_config=docker_config,
            build=build,
            pull=pull,
            nginx_port=nginx_port,
            wbs_url=wbs_url,
            isyntax_sdk=isyntax_sdk,
            volume_prefix=volume_prefix,
            gpu_driver=gpu_driver,
            frontend_token_exp=frontend_token_exp,
            scope_token_exp=scope_token_exp,
            app_ui_frame_ancestors=app_ui_frame_ancestors,
            app_ui_connect_src=app_ui_connect_src,
            app_ui_disable_csp=app_ui_disable_csp,
        )
        services_wait(client=client)

        sss_app = apps_register(client, ead, docker_image, global_config_file, customer_config_file)
        app_id = sss_app["id"]

        job_id, token, app_api = jobs_register(
            client=client, app_id=app_id, input_dir=input_dir, job_mode=job_mode, pp_job_id=None
        )
        jobs_run(client=client, job_id=job_id, token=token, app_api=app_api)

        jobs_wait(client=client, job_id=job_id)
        jobs_export(client=client, job_id=job_id, output_dir=output_dir)

        container = client.containers.get(job_id)
        container.remove(force=True)

        services_down(client=client, volume_prefix=volume_prefix)
