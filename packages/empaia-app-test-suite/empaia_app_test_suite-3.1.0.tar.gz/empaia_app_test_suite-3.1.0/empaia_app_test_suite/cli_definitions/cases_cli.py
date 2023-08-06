import docker
import typer

import empaia_app_test_suite.constants as const
from empaia_app_test_suite.commands.cases_commands import cases_list, cases_register
from empaia_app_test_suite.commands.services_commands import services_health
from empaia_app_test_suite.utils.utils_print import convert_cases_list_to_pretty_table, print_table, print_table_column


def init_cases_cli(cases_app):
    @cases_app.command("register")
    def _(description: str = typer.Option(None, "--description", help=const.CASE_DESC_HELPER)):
        client = docker.from_env()
        services_health(client=client, silent=True)

        case = cases_register(client, description)
        print(f"$CASE_ID={case['id']}")

    @cases_app.command("list")
    def _(
        q: bool = typer.Option(None, "-q", help=const.CASE_LIST_OPTION),
        border: bool = typer.Option(None, "--border", help=const.LIST_BORDER_OPTION),
        table_format: str = typer.Option(None, "--format", help=const.LIST_FORMAT),
    ):
        client = docker.from_env()
        services_health(client=client, silent=True)

        cases = cases_list(client)
        table = convert_cases_list_to_pretty_table(cases)
        if q:
            print_table_column(table, "CASE ID")
        else:
            print_table(table, table_format, border)
