from pathlib import Path

import docker
import typer

import empaia_app_test_suite.constants as const
from empaia_app_test_suite import __version__
from empaia_app_test_suite.commands.services_commands import services_health
from empaia_app_test_suite.commands.slides_commands import delete_slide, get_slides_list, slides_register
from empaia_app_test_suite.utils.utils_print import convert_slides_list_to_pretty_table, print_table, print_table_column


def init_slides_cli(slides_app):
    @slides_app.command("register")
    def _(
        slide_file: Path = typer.Argument(..., help=const.SLIDE_FILE_HELP),
        q: bool = typer.Option(None, "-q", help=const.APP_LIST_OPTION),
        table_format: str = typer.Option(None, "--format", help=const.LIST_FORMAT),
        border: bool = typer.Option(None, "--border", help=const.LIST_BORDER_OPTION),
    ):
        client = docker.from_env()
        services_health(client=client, silent=True)

        new_wsis, existing_wsis = slides_register(client=client, slide_file=slide_file, quiet=True)
        added_ids = [wsi.id for wsi in new_wsis + existing_wsis]
        raw_slides = get_slides_list(client)["items"]
        added_slides = []
        for raw_slide in raw_slides:
            if raw_slide["id"] in added_ids:
                added_slides.append(raw_slide)

        table = convert_slides_list_to_pretty_table({"items": added_slides})
        if q:
            print_table_column(table, "SLIDE ID")
        else:
            print_table(table, table_format, border)

    @slides_app.command("list")
    def _(
        q: bool = typer.Option(None, "-q", help=const.APP_LIST_OPTION),
        border: bool = typer.Option(None, "--border", help=const.LIST_BORDER_OPTION),
        table_format: str = typer.Option(None, "--format", help=const.LIST_FORMAT),
    ):
        client = docker.from_env()
        services_health(client=client, silent=True)

        slides = get_slides_list(client)
        table = convert_slides_list_to_pretty_table(slides)
        if q:
            print_table_column(table, "SLIDE ID")
        else:
            print_table(table, table_format, border)

    @slides_app.command("delete")
    def _(slide_id: str = typer.Argument(..., help="Slide ID.")):
        client = docker.from_env()
        services_health(client=client, silent=True)
        delete_slide(client=client, slide_id=slide_id)
