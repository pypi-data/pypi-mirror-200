import json
from pathlib import Path

import docker
import typer

import empaia_app_test_suite.constants as const
from empaia_app_test_suite.commands.apps_commands import apps_register, apps_update
from empaia_app_test_suite.commands.services_commands import services_health
from empaia_app_test_suite.utils.utils_mps import get_mps_apps_list
from empaia_app_test_suite.utils.utils_print import (
    convert_mps_apps_list_to_pretty_table,
    print_table,
    print_table_column,
)


def init_apps_cli(apps_app):
    @apps_app.command("list")
    def _(
        q: bool = typer.Option(None, "-q", help=const.APP_LIST_OPTION),
        border: bool = typer.Option(None, "--border", help=const.LIST_BORDER_OPTION),
        table_format: str = typer.Option(None, "--format", help=const.LIST_FORMAT),
    ):
        client = docker.from_env()
        services_health(client=client, silent=True)

        apps = get_mps_apps_list(client)
        table = convert_mps_apps_list_to_pretty_table(apps)
        if q:
            print_table_column(table, "APP ID")
        else:
            print_table(table, table_format, border)

    @apps_app.command("register")
    def _(
        ead_file: Path = typer.Argument(..., help=const.EAD_FILE_HELP),
        docker_image: str = typer.Argument(..., help=const.DOCKER_IMAGE_HELP),
        global_config_file: Path = typer.Option(None, "--global-config-file", help=const.GLOBAL_CONFIG_FILE_HELP),
        customer_config_file: Path = typer.Option(None, "--customer-config-file", help=const.CUSTOMER_CONFIG_FILE_HELP),
        app_ui_url: str = typer.Option(None, "--app-ui-url", help=const.APP_UI_URL_HELP),
        app_ui_config_file: Path = typer.Option(None, "--app-ui-config-file", help=const.APP_UI_CONFIG_FILE_HELP),
    ):
        client = docker.from_env()
        services_health(client=client, silent=True)

        with open(ead_file, "r", encoding="utf-8") as f:
            ead = json.load(f)
        registered_app = apps_register(
            client, ead, docker_image, global_config_file, customer_config_file, app_ui_url, app_ui_config_file
        )
        print(f"APP_ID={registered_app['active_app_views']['v3']['app']['id']}")

    @apps_app.command("update")
    def _(
        app_id: Path = typer.Argument(..., help=const.APP_ID_HELP),
        global_config_file: Path = typer.Option(None, "--global-config-file", help=const.GLOBAL_CONFIG_FILE_HELP),
        customer_config_file: Path = typer.Option(None, "--customer-config-file", help=const.CUSTOMER_CONFIG_FILE_HELP),
        app_ui_url: str = typer.Option(None, "--app-ui-url", help=const.APP_UI_URL_HELP),
        app_ui_config_file: Path = typer.Option(None, "--app-ui-config-file", help=const.APP_UI_CONFIG_FILE_HELP),
    ):
        client = docker.from_env()
        services_health(client=client, silent=True)

        apps_update(client, app_id, global_config_file, customer_config_file, app_ui_url, app_ui_config_file)
