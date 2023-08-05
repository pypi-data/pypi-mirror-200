import enum
import os
from dataclasses import asdict
from os.path import exists

from typing import List, Dict

import typer
from bigeye_cli import DEFAULT_CRED_FILE
from bigeye_sdk.generated.com.bigeye.models.generated import MetricInfoList, Table, Issue, MetricTemplate
from bigeye_sdk.model.protobuf_extensions import MetricDebugQueries
from rich.prompt import Prompt

from bigeye_sdk.class_ext.enum_ext import StrEnum
from bigeye_sdk.client.datawatch_client import DatawatchClient, datawatch_client_factory

from bigeye_sdk.functions.metric_functions import get_file_name_for_metric
from bigeye_sdk.functions.file_functs import create_subdir_if_not_exists, serialize_listdict_to_json_file, \
    write_to_file, serialize_list_to_json_file

from bigeye_sdk.log import get_logger
from bigeye_sdk.authentication.api_authentication import BasicAuthRequestLibConf, ApiAuthConf
from bigeye_sdk.model.protobuf_message_facade import SimpleTemplateMetric

log = get_logger(__file__)


def print_txt_file(file: str):
    from rich.console import Console

    console = Console()
    with open(file, "r+") as help_file:
        with console.pager():
            console.print(help_file.read())


def print_markdown(file: str):
    from rich.console import Console
    from rich.markdown import Markdown

    console = Console()
    with open(file, "r+") as help_file:
        with console.pager():
            console.print(Markdown(help_file.read()))


def cli_client_factory(api_conf_file: str = None) -> DatawatchClient:
    """
    Args:
        api_conf_file: file containing the api_conf.  If none will look for environment var BIGEYE_API_CRED_FILE
        or the default cred file.

    Returns: a Datawatch client

    """
    if api_conf_file and os.path.isfile(api_conf_file):
        return datawatch_client_factory(ApiAuthConf.load_from_file(api_conf_file))
    elif api_conf_file:
        return datawatch_client_factory(ApiAuthConf.load_from_base64(api_conf_file))
    elif 'BIGEYE_API_CRED_FILE' in os.environ:
        return datawatch_client_factory(ApiAuthConf.load_from_file(os.environ['BIGEYE_API_CRED_FILE']))
    elif exists(DEFAULT_CRED_FILE):
        return datawatch_client_factory(ApiAuthConf.load_from_file(DEFAULT_CRED_FILE))
    else:
        raise Exception('No credential present.  Please either identify a default credential file or pass one'
                        'with the command.')


def write_metric_info(output_path: str, metrics: MetricInfoList,
                      file_name: str = None, only_metric_conf: bool = False):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    for metric in metrics.metrics:
        """Writes individual metrics to files in the output path."""
        mc = metric.metric_configuration
        md = metric.metric_metadata

        if only_metric_conf:
            datum = mc
            log.info('Persisting metric configurations.')
        else:
            datum = metric
            log.info('Persisting metric info.')

        if not file_name:
            subpath = f"{output_path}/metric_info/warehouse_id-{md.warehouse_id}"

            create_subdir_if_not_exists(path=subpath)
            fn = get_file_name_for_metric(metric)
            url = f'{subpath}/{fn}'
        else:
            url = f'{output_path}/metric_info/{file_name}'

        serialize_listdict_to_json_file(url=url,
                                        data=[datum.to_dict()])


def write_debug_queries(output_path: str, queries: List[MetricDebugQueries]):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    for q in queries:
        subpath = f"{output_path}/debug_queries"

        create_subdir_if_not_exists(path=subpath)

        fn = f'{q.metric_id}_metric_query.txt'
        url = f'{subpath}/{fn}'
        write_to_file(url, [q.debug_queries.metric_query])

        if q.debug_queries.debug_query:
            fn = f'{q.metric_id}_debug_query.txt'
            url = f'{subpath}/{fn}'
            write_to_file(url, [q.debug_queries.debug_query])


def write_table_info(output_path: str, tables: List[Table], file_name: str = None):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    for table in tables:
        """Writes individual issues to files in the output path."""
        log.info('Persisting issue.')
        if not file_name:
            subpath = f"{output_path}/table_info/warehouse_id-{table.warehouse_id}"

            create_subdir_if_not_exists(path=subpath)
            fn = f'{table.id}-{table.schema_name}-{table.name}.json'
            url = f'{subpath}/{fn}'
        else:
            url = f'{output_path}/{file_name}'

        serialize_listdict_to_json_file(url=url,
                                        data=[table.to_dict()])


def write_issue_info(output_path: str, issues: List[Issue], file_name: str = None):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    for issue in issues:
        """Writes individual issues to files in the output path."""
        log.info('Persisting issue.')
        if not file_name:
            subpath = f"{output_path}/issue_info/warehouse_id-{issue.metric_configuration.warehouse_id}" \
                      f"/dataset_id-{issue.metric_configuration.dataset_id}" \
                      f"/{issue.metric_configuration.name.replace(' ', '_')}"

            create_subdir_if_not_exists(path=subpath)
            fn = f'{issue.id}-{issue.name}.json'
            url = f'{subpath}/{fn}'
        else:
            url = f'{output_path}/{file_name}'

        serialize_listdict_to_json_file(url=url,
                                        data=[issue.to_dict()])


def write_metric_templates(output_path: str, metric_templates: List[MetricTemplate], file_name: str = None):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if not file_name:
        file_name = "metric_templates.json"

    url = f'{output_path}/{file_name}'

    serialize_list_to_json_file(url=url, data=metric_templates)


def run_enum_menu(enum_clz: enum.EnumMeta, default: StrEnum) -> StrEnum:
    valid_types: Dict[int, StrEnum] = {index: auth_type for index, auth_type in enumerate(list(enum_clz), start=1)}
    valid_type_by_type: Dict[StrEnum, int] = {v: k for k, v in valid_types.items()}

    user_chosen_type_ix = 0

    while user_chosen_type_ix not in valid_type_by_type.values():
        for user_chosen_type_ix, index in valid_type_by_type.items():
            typer.echo(f"{index}) {user_chosen_type_ix.value}")
        try:
            user_chosen_type_ix = int(Prompt.ask(
                f"Would authorization method would you like to use? "
                f"(Default: {valid_type_by_type[default]})", default=valid_type_by_type[default])
            )
        except ValueError as e:
            pass

        if user_chosen_type_ix not in valid_types.keys():
            typer.echo(f"Invalid Choice.")

    return valid_types[user_chosen_type_ix]
