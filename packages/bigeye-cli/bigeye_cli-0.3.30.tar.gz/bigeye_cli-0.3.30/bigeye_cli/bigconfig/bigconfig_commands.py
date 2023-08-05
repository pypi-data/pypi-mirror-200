from pathlib import Path
from typing import Optional, List

import typer

from bigeye_cli.functions import cli_client_factory
from bigeye_sdk.controller.metric_suite_controller import MetricSuiteController
from bigeye_sdk.log import get_logger

log = get_logger(__file__)

app = typer.Typer(no_args_is_help=True, help='Bigconfig Commands for Bigeye CLI')

"""
File should contain commands relating to deploying Bigconfig files.
"""


@app.command()
def plan(
        bigeye_conf: str = typer.Option(
            None
            , "--bigeye_conf"
            , "-b"
            , help="Bigeye Auth Configuration"),
        input_path: Optional[List[str]] = typer.Option(
            None
            , "--input_path"
            , "-ip"
            , help="List of paths containing Bigconfig files or pointing to a Bigconfig file. E.g. -ip path1 -ip path2."
                   " If no input path is defined then current working directory will be used."),
        output_path: str = typer.Option(
            None
            , "--output_path"
            , "-op"
            , help="Output path where reports and fixme files will be saved. If no output path is defined "
                   "then current working directory will be used."),
        purge_source_names: Optional[List[str]] = typer.Option(
            None
            , "--purge_source_name"
            , "-psn"
            , help="List of source names to purge  E.g. -psn source_1 -psn source_2."
        ),
        purge_all_sources: bool = typer.Option(
            False
            , "--purge_all_sources"
            , "-purge_all"
            , help="Purge all sources: True or False."
        ),
        recursive: bool = typer.Option(
            False
            , "--recursive"
            , "-r"
            , help="Search all input directories recursively."
        )
):
    """Executes a plan for purging sources or processing bigconfig files in the input path/current
    working directory."""

    client = cli_client_factory(bigeye_conf)
    mc = MetricSuiteController(client=client)
    if not input_path:
        input_path = [Path.cwd()]
    if not output_path:
        output_path = Path.cwd()

    if purge_source_names or purge_all_sources:
        mc.execute_purge(purge_source_names=purge_source_names, purge_all_sources=purge_all_sources,
                         output_path=output_path, apply=False)
    else:
        mc.execute_bigconfig(input_path=input_path, output_path=output_path, apply=False, recursive=recursive)


@app.command()
def apply(
        bigeye_conf: str = typer.Option(
            None
            , "--bigeye_conf"
            , "-b"
            , help="Bigeye Auth Configuration"),
        input_path: Optional[List[str]] = typer.Option(
            None
            , "--input_path"
            , "-ip"
            , help="List of paths containing Bigconfig files or pointing to a Bigconfig file. E.g. -ip path1 -ip path2."
                   " If no input path is defined then current working directory will be used."),
        output_path: str = typer.Option(
            None
            , "--output_path"
            , "-op"
            ,
            help="Output path where reports and fixme files will be saved. If no output path is defined "
                 "then current working directory will be used."),
        purge_source_names: Optional[List[str]] = typer.Option(
            None
            , "--purge_source_name"
            , "-psn"
            , help="List of source names to purge  E.g. -psn source_1 -psn source_2."
        ),
        purge_all_sources: bool = typer.Option(
            False
            , "--purge_all_sources"
            , "-purge_all"
            , help="Purge all sources: True or False."
        ),
        no_queue: bool = typer.Option(
            False
            , "--no_queue"
            , "-nq"
            , help="Don't submit to queue: True or False."
        ),
        recursive: bool = typer.Option(
            False
            , "--recursive"
            , "-r"
            , help="Search all input directories recursively."
        )
):
    """Applies a purge of deployed metrics or applies Bigconfig files from the input path/current working directory to
    the Bigeye workspace."""

    client = cli_client_factory(bigeye_conf)
    mc = MetricSuiteController(client=client)
    if not input_path:
        input_path = [Path.cwd()]
    if not output_path:
        output_path = Path.cwd()

    if purge_source_names or purge_all_sources:
        mc.execute_purge(purge_source_names=purge_source_names, purge_all_sources=purge_all_sources,
                         output_path=output_path, apply=True)
    else:
        mc.execute_bigconfig(input_path=input_path, output_path=output_path, apply=True,
                             no_queue=no_queue, recursive=recursive)

