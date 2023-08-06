import functools
import sys

import requests
import typer

from empaia_app_test_suite import __version__, settings
from empaia_app_test_suite.cli_definitions.apps_cli import init_apps_cli
from empaia_app_test_suite.cli_definitions.jobs_cli import init_jobs_cli
from empaia_app_test_suite.cli_definitions.main_cli import init_main_cli
from empaia_app_test_suite.cli_definitions.services_cli import init_services_cli
from empaia_app_test_suite.cli_definitions.slides_cli import init_slides_cli
from empaia_app_test_suite.utils.utils_print import print_failed


class ExceptionHandlingTyper(typer.Typer):
    eats_settings = settings.EatsSettings()

    def command(self, *cmd_args, **cmd_kwargs):
        def decorator(function):
            @functools.wraps(function)
            def wrapper(*args, **kwargs):
                try:
                    return function(*args, **kwargs)
                except requests.exceptions.HTTPError as exc:
                    if self.eats_settings.debug:
                        raise exc
                    print_failed(f"{type(exc).__name__}: {exc}")
                    response_dict = exc.response.json()
                    if "detail" in response_dict:
                        if isinstance(response_dict["detail"], str):
                            print_failed(response_dict["detail"])
                        if isinstance(response_dict["detail"], dict):
                            for detail_name, detail in response_dict["detail"].items():
                                print_failed(f"{detail_name.upper()}: {detail}")
                    sys.exit(1)
                except Exception as exc:
                    if self.eats_settings.debug:
                        raise exc
                    print_failed(f"{type(exc).__name__}: {exc}")
                    sys.exit(1)

            return typer.Typer.command(self, *cmd_args, **cmd_kwargs)(wrapper)

        return decorator


app = ExceptionHandlingTyper(name="eats")
services_app = ExceptionHandlingTyper()
jobs_app = ExceptionHandlingTyper()
apps_app = ExceptionHandlingTyper()
slides_app = ExceptionHandlingTyper()
# currently disabled
# cases_app = ExceptionHandlingTyper()

init_main_cli(app)
init_services_cli(services_app)
init_slides_cli(slides_app)
init_apps_cli(apps_app)
init_jobs_cli(jobs_app)
# currently disabled
# init_cases_cli(cases_app)

app.add_typer(services_app, name="services")
app.add_typer(jobs_app, name="jobs")
app.add_typer(apps_app, name="apps")
app.add_typer(slides_app, name="slides")
# currently disabled
# app.add_typer(cases_app, name="cases")


if __name__ == "__main__":
    app()
