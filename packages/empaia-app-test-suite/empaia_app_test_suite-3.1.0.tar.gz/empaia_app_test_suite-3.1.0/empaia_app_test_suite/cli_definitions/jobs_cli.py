import json
from pathlib import Path
from typing import Optional

import docker
import typer

import empaia_app_test_suite.constants as const
from empaia_app_test_suite.commands.helper.job_helper import read_job_env
from empaia_app_test_suite.commands.jobs_commands import (
    get_jobs_list,
    jobs_abort,
    jobs_export,
    jobs_inspect,
    jobs_register,
    jobs_run,
    jobs_set_running,
    jobs_status,
    jobs_wait,
)
from empaia_app_test_suite.commands.services_commands import services_health
from empaia_app_test_suite.utils.utils_commons import ValidationError
from empaia_app_test_suite.utils.utils_print import convert_jobs_list_to_pretty_table, print_table, print_table_column


def init_jobs_cli(jobs_app):
    @jobs_app.command("exec")
    def _(
        app_id: str = typer.Argument(..., help=const.APP_ID_HELP),
        input_dir: Path = typer.Argument(..., help=const.INPUT_DIR_HELP),
        output_dir: Path = typer.Argument(..., help=const.OUTPUT_DIR_HELP),
        job_mode: Optional[str] = typer.Option("standalone", "--job-mode", help=const.JOB_MODE),
        preprocessing_job_id: str = typer.Option(None, "--preprocessing-job-id", help=const.PREPROCESSING_JOB_ID),
    ):
        client = docker.from_env()
        services_health(client=client, silent=True)

        job_id, token, app_api = jobs_register(
            client=client, app_id=app_id, input_dir=input_dir, job_mode=job_mode, pp_job_id=preprocessing_job_id
        )

        print(f"EMPAIA_JOB_ID={job_id}")
        print(f"EMPAIA_TOKEN={token}")
        print(f"EMPAIA_APP_API={app_api}")

        jobs_run(client=client, job_id=job_id, token=token, app_api=app_api)

        jobs_wait(client=client, job_id=job_id)

        jobs_export(client=client, job_id=job_id, output_dir=output_dir)

        container = client.containers.get(job_id)
        container.remove(force=True)

    @jobs_app.command("list")
    def _(
        q: bool = typer.Option(None, "-q", help=const.JOB_LIST_OPTION),
        border: bool = typer.Option(None, "--border", help=const.LIST_BORDER_OPTION),
        table_format: str = typer.Option(None, "--format", help=const.LIST_FORMAT),
    ):
        client = docker.from_env()
        services_health(client=client, silent=True)

        jobs = get_jobs_list(client)
        table = convert_jobs_list_to_pretty_table(jobs)
        if q:
            print_table_column(table, "JOB ID")
        else:
            print_table(table, table_format, border)

    @jobs_app.command("register")
    def _(
        app_id: str = typer.Argument(..., help=const.APP_ID_HELP),
        input_dir: Path = typer.Argument(..., help=const.INPUT_DIR_HELP),
        job_mode: Optional[str] = typer.Option("standalone", "--job-mode", help=const.JOB_MODE),
        preprocessing_job_id: str = typer.Option(None, "--preprocessing-job-id", help=const.PREPROCESSING_JOB_ID),
    ):
        client = docker.from_env()
        services_health(client=client, silent=True)

        if job_mode != "postprocessing" and preprocessing_job_id:
            raise ValidationError("The option '--preprocessing-job-id' is only supported for job mode 'postprocessing'")

        job_id, token, app_api = jobs_register(
            client=client, app_id=app_id, input_dir=input_dir, job_mode=job_mode, pp_job_id=preprocessing_job_id
        )

        print(f"EMPAIA_JOB_ID={job_id}")
        print(f"EMPAIA_TOKEN={token}")
        print(f"EMPAIA_APP_API={app_api}")

    @jobs_app.command("run")
    def _(
        job_env_file: Path = typer.Argument(
            ..., help="Path to job env file containing EMPAIA_JOB_ID, EMPAIA_TOKEN and EMPAIA_APP_API env vars."
        )
    ):
        client = docker.from_env()
        services_health(client=client, silent=True)

        job_env = read_job_env(job_env_file)

        job_id = job_env.settings.empaia_job_id
        token = job_env.settings.empaia_token
        app_api = job_env.settings.empaia_app_api

        jobs_run(client=client, job_id=job_id, token=token, app_api=app_api)

    @jobs_app.command("status")
    def _(job_id: str = typer.Argument(..., help="Job ID.")):
        client = docker.from_env()
        services_health(client=client, silent=True)

        status = jobs_status(client=client, job_id=job_id)

        print(status)

    @jobs_app.command("inspect")
    def _(job_id: str = typer.Argument(..., help="Job ID.")):
        client = docker.from_env()
        services_health(client=client, silent=True)

        inspect = jobs_inspect(client=client, job_id=job_id, quiet=True)
        print(json.dumps(inspect, indent=4))

    @jobs_app.command("wait")
    def _(job_id: str = typer.Argument(..., help="Job ID.")):
        client = docker.from_env()
        services_health(client=client, silent=True)
        jobs_wait(client=client, job_id=job_id)

    @jobs_app.command("export")
    def _(
        job_id: str = typer.Argument(..., help="Job ID."),
        output_dir: Path = typer.Argument(..., help=const.OUTPUT_DIR_HELP),
    ):
        client = docker.from_env()
        services_health(client=client, silent=True)

        jobs_export(client=client, job_id=job_id, output_dir=output_dir)

    @jobs_app.command("abort")
    def _(job_id: str = typer.Argument(..., help="Job ID.")):
        client = docker.from_env()
        services_health(client=client, silent=True)

        jobs_abort(client=client, job_id=job_id)

    @jobs_app.command("set-running")
    def _(job_id: str = typer.Argument(..., help="Job ID.")):
        client = docker.from_env()
        services_health(client=client, silent=True)

        jobs_set_running(client=client, job_id=job_id)
