import json
from pathlib import Path

import docker
import typer

import empaia_app_test_suite.constants as const
from empaia_app_test_suite.commands.services_commands import (
    services_down,
    services_health,
    services_list,
    services_up,
    services_volumes,
    services_wait,
)


def init_services_cli(services_app):
    @services_app.command("up")
    def _(
        wsi_mount_points_file: Path = typer.Argument(..., help=const.WSI_MOUNT_POINTS_FILE_HELP),
        build: bool = typer.Option(False, "--build", help=const.BUILD_HELP),
        pull: bool = typer.Option(False, "--pull", help=const.PULL_HELP),
        docker_config: Path = typer.Option(None, "--docker-config", help=const.DOCKER_CONFIG_FILE_HELP),
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

    @services_app.command("wait")
    def _(
        trials: int = typer.Option(10, "--trials", help=const.TRIALS_SERVICES_HELP),
    ):
        client = docker.from_env()
        services_wait(client=client, trials=trials)

    @services_app.command("health")
    def _():
        client = docker.from_env()
        services_health(client=client)

    @services_app.command("list")
    def _():
        client = docker.from_env()
        # services_wait(client=client, silent=True)

        services = services_list(client)
        for service in services:
            print(service)

    @services_app.command("down")
    def _(
        del_volumes: bool = typer.Option(None, "-v", help="Delete volumes"),
        volume_prefix: str = typer.Option(None, "--volume-prefix", help=const.VOLUME_PREFIX_HELP),
    ):
        client = docker.from_env()
        services_down(client=client, del_volumes=del_volumes, volume_prefix=volume_prefix)

    @services_app.command("volumes")
    def _(volume_prefix: str = typer.Option(None, "--volume-prefix", help=const.VOLUME_PREFIX_HELP)):
        volumes = services_volumes(volume_prefix)
        for volume in volumes:
            print(volume)
