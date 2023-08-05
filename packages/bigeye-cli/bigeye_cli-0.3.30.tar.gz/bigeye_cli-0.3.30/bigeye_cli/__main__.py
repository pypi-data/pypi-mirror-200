from typing import Optional

import typer

from bigeye_cli import DEFAULT_CRED_FILE, CLI_DOCS_MD
from bigeye_cli.bigconfig import bigconfig_commands
from bigeye_cli.lineage import lineage_commands
from bigeye_sdk.authentication.enums import AuthConfType, BrowserType
from bigeye_sdk.functions.file_functs import create_subdir_if_not_exists

from bigeye_sdk.authentication.api_authentication import BasicAuthRequestLibConf, BrowserAuthConf

import bigeye_cli.__version__ as bigeye_cli_version
import bigeye_sdk.__version__ as bigeye_sdk_version
from bigeye_cli.deltas import deltas_commands
from bigeye_cli.functions import print_markdown, run_enum_menu
from bigeye_cli.workspace import workspace_commands
from bigeye_sdk.log import get_logger

from bigeye_cli.catalog import catalog_commands
from bigeye_cli.sla import sla_commands
from bigeye_cli.metric import metric_commands
from bigeye_cli.issues import issue_commands
from bigeye_cli.collections import collection_commands

# create logger
log = get_logger(__file__)

app = typer.Typer(no_args_is_help=True, help="""Bigeye CLI""")
app.add_typer(sla_commands.app, name='sla', deprecated=True)
app.add_typer(catalog_commands.app, name='catalog')
app.add_typer(metric_commands.app, name='metric')
app.add_typer(deltas_commands.app, name='deltas')
app.add_typer(workspace_commands.app, name='workspace')
app.add_typer(issue_commands.app, name='issues')
app.add_typer(bigconfig_commands.app, name='bigconfig')
app.add_typer(collection_commands.app, name='collections')
app.add_typer(lineage_commands.app, name='lineage')


@app.callback(invoke_without_command=True)
def options_callback(
        version: Optional[bool] = typer.Option(
            None, "--version", help="Bigeye CLI and SDK Versions"),
        readme: Optional[bool] = typer.Option(
            None, "--readme", help="Prints Readme.")
):
    if version:
        typer.echo(f'Bigeye CLI Version: {bigeye_cli_version.version}\n'
                   f'Bigeye SDK Version: {bigeye_sdk_version.version}')
        raise typer.Exit()
    elif readme:
        print_markdown(file=CLI_DOCS_MD)


@app.command()
def credential():
    """Create a default credential for Bigeye CLI."""
    from rich.prompt import Prompt

    auth_type = run_enum_menu(enum_clz=AuthConfType, default=AuthConfType.BROWSER_AUTH)

    if auth_type == AuthConfType.BASIC_AUTH:
        base_url = Prompt.ask("Enter the Bigeye URL", default="https://app.bigeye.com")
        username = Prompt.ask("Enter the username")
        password = Prompt.ask("Enter the password", password=True)
        cred = BasicAuthRequestLibConf(base_url=base_url, user=username,
                                       password=password)
    else:
        browser_type = run_enum_menu(enum_clz=BrowserType, default=BrowserType.CHROME)

        browser_profile_user_name = None

        if browser_type == BrowserType.CHROME:
            # TODO Could condition on path containing Profile_N directories.
            browser_profile_user_name = Prompt.ask("Enter the profile email if logged into Chrome (Default: None)")
        base_url = Prompt.ask("Enter the Bigeye URL", default="https://app.bigeye.com")

        cred = BrowserAuthConf(browser=browser_type, base_url=base_url,
                               browser_profile_user_name=browser_profile_user_name)

    create_subdir_if_not_exists(path=DEFAULT_CRED_FILE, includes_file=True)

    cred.save_to_file(DEFAULT_CRED_FILE)


if __name__ == '__main__':
    app()
