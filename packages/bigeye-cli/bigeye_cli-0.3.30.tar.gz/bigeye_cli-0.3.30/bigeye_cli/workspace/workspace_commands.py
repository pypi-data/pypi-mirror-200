import base64
import json
from typing import List

import requests
import typer

from bigeye_cli.functions import cli_client_factory
from bigeye_sdk.authentication.api_authentication import BasicAuthRequestLibConf
from bigeye_sdk.client.enum import Method
from bigeye_sdk.functions.core_py_functs import int_enum_enum_list_joined
from bigeye_sdk.generated.com.bigeye.models.generated import TimeIntervalType, MetricConfiguration, TimeInterval
from bigeye_sdk.log import get_logger

log = get_logger(__file__)

app = typer.Typer(no_args_is_help=True, help='Workspace Commands for Bigeye CLI')

"""Commands that pertain to a Bigeye workspace"""


@app.command()
def unschedule_all_metrics(
        bigeye_conf: str = typer.Option(
            None
            , "--bigeye_conf"
            , "-b"
            , help="Bigeye Basic Auth Configuration")
):
    """Unschedule all metrics in a workspace."""
    client = cli_client_factory(bigeye_conf)

    wids: List[int] = [s.id for s in client.get_sources().sources]

    # Could do bulk change by wid and metric type which are necessary in the api call.
    mcs: List[dict] = [mil.metric_configuration.to_dict()
                       for mil in client.get_metric_info_batch_post(warehouse_ids=wids).metrics]

    mc = MetricConfiguration()
    ti = TimeInterval()
    ti.interval_type = TimeIntervalType.DAYS_TIME_INTERVAL_TYPE
    ti.interval_value = 0
    mc.schedule_frequency = ti

    log.info(mc.to_json())

    # TODO: this is an antipattern.  is there another way to set the value to 0?
    mc_dict = mc.to_dict()
    mc_dict['scheduleFrequency']['intervalValue'] = 0

    log.info(json.dumps(mc_dict))

    url = '/api/v1/metrics/batch'

    response = client._call_datawatch(Method.PUT, url=url, body=json.dumps(mc))


@app.command()
def schedule_all_metrics(
        bigeye_conf: str = typer.Option(
            None
            , "--bigeye_conf"
            , "-b"
            , help="Bigeye Basic Auth Configuration"),
        time_interval_type: int = typer.Option(
            TimeIntervalType.HOURS_TIME_INTERVAL_TYPE.value
            , "--time_interval_type"
            , "-type"
            , help=f"Time interval type.\n {int_enum_enum_list_joined(enum=TimeIntervalType)}"),
        interval_value: int = typer.Option(
            ...
            , "--interval_value"
            , "-value"
            , help="Number of intervals to set on all metric schedules.  If 0 use unschedule all metrics.")
):
    """Schedule all metrics in a workspace."""
    client = cli_client_factory(bigeye_conf)

    tit = TimeIntervalType(time_interval_type)

    wids: List[int] = [s.id for s in client.get_sources().sources]

    # Could do bulk change by wid and metric type which are necessary in the api call.
    mcs: List[dict] = [mil.metric_configuration.to_dict()
                       for mil in client.get_metric_info_batch_post(warehouse_ids=wids).metrics]

    for mc in mcs:
        mc["scheduleFrequency"] = {
            "intervalType": tit.name,
            "intervalValue": interval_value
        }

        url = "/api/v1/metrics"

        response = client._call_datawatch(Method.POST, url=url, body=json.dumps(mc))


@app.command()
def create_named_schedule(
        bigeye_conf: str = typer.Option(
            None
            , "--bigeye_conf"
            , "-b"
            , help="Bigeye Basic Auth Configuration"),
        name: str = typer.Option(
            ...
            , "--name"
            , "-sn"
            , help="The user defined name of the schedule"),
        cron: str = typer.Option(
            ...
            , "--cron"
            , "-c"
            , help="The cron string to define the schedule")
):
    """Create a named, cron based schedule"""
    client = cli_client_factory(bigeye_conf)

    response = client.create_named_schedule(name=name, cron=cron)
    log.info(f"Named schedule created\n\tname: {response.name}\n\tcron:{response.cron}\n\tid:{response.id}")


@app.command()
def delete_named_schedule(
        bigeye_conf: str = typer.Option(
            None
            , "--bigeye_conf"
            , "-b"
            , help="Bigeye Basic Auth Configuration"),
        name: str = typer.Option(
            ...
            , "--name"
            , "-sn"
            , help="The user defined name of the schedule")
):
    """Delete a named schedule."""
    client = cli_client_factory(bigeye_conf)
    response = client.get_named_schedule()
    named_schedules = [s for s in response.named_schedules if s.name == name]

    schedule = named_schedules[0]
    client.delete_named_schedule(schedule_id=schedule.id)


# TODO: These will change based on RBAC. Either add to datawatch client or create UserClient for form submission.
@app.command()
def invite_user(
        bigeye_conf: str = typer.Option(
            ...
            , "--bigeye_conf"
            , "-b"
            , help="Bigeye Basic Auth Configuration. (browser auth not supported)"),
        user_name: str = typer.Option(
            ...
            , "--user_name"
            , "-un"
            , help="User name."),
        email: str = typer.Option(
            ...
            , "--user_email"
            , "-email"
            , help="Email where invite will be sent.")
):
    """Invite a user. Only supports basic auth conf"""
    url = "user/invite/form"
    conf: BasicAuthRequestLibConf = BasicAuthRequestLibConf.load_from_file(bigeye_conf)

    user_url = f"{conf.base_url}/{url}"

    files = {
        'name': (None, user_name),
        'email': (None, email),
    }

    token = base64.b64encode(f"{conf.user}:{conf.password}".encode('utf-8')).decode("ascii")

    response = requests.post(user_url
                             , headers={"Authorization": f"Basic {token}"}
                             , files=files)

    if response.status_code < 200 or response.status_code >= 300:
        errmsg = f'Error Code {response.status_code}: {response.text}'
        log.error(errmsg)
        raise Exception(errmsg)
    else:
        log.info(f"Invite has been sent to {user_name} at {email}")


@app.command()
def edit_user_role(
        bigeye_conf: str = typer.Option(
            ...
            , "--bigeye_conf"
            , "-b"
            , help="Bigeye Basic Auth Configuration. (browser auth not supported)"),
        user_name: str = typer.Option(
            ...
            , "--user_name"
            , "-un"
            , help="User name."),
        user_role: str = typer.Option(
            ...
            , "--user_role"
            , "-role"
            , help="The role to assign the user, i.e. OWNER, ADMIN, USER.")
):
    """Change user role. Only supports basic auth conf"""
    conf: BasicAuthRequestLibConf = BasicAuthRequestLibConf.load_from_file(bigeye_conf)
    base_url = conf.base_url
    token = base64.b64encode(f"{conf.user}:{conf.password}".encode('utf-8')).decode("ascii")
    r = requests.get(url=f"{base_url}/user", headers={"Authorization": f"Basic {token}"})
    user_id = [u['id'] for u in r.json()['users'] if u['name'] == user_name][0]

    files = {
        'user-id': (None, user_id),
        'user-role': (None, user_role.upper()),
    }

    response = requests.post(url=f"{base_url}/user/{user_id}/role"
                             , headers={"Authorization": f"Basic {token}"}
                             , files=files)

    if response.status_code < 200 or response.status_code >= 300:
        errmsg = f'Error Code {response.status_code}: {response.text}'
        log.error(errmsg)
        raise Exception(errmsg)
    else:
        log.info(f"Role for user {user_name} has been changed to {user_role}")


@app.command()
def delete_user(
        bigeye_conf: str = typer.Option(
            ...
            , "--bigeye_conf"
            , "-b"
            , help="Bigeye Basic Auth Configuration. (browser auth not supported)"),
        user_name: str = typer.Option(
            ...
            , "--user_name"
            , "-un"
            , help="User name.")
):
    """Remove user from workspace. Only supports basic auth conf"""
    conf: BasicAuthRequestLibConf = BasicAuthRequestLibConf.load_from_file(bigeye_conf)
    base_url = conf.base_url
    token = base64.b64encode(f"{conf.user}:{conf.password}".encode('utf-8')).decode("ascii")
    r = requests.get(url=f"{base_url}/user", headers={"Authorization": f"Basic {token}"})
    user_id = [u['id'] for u in r.json()['users'] if u['name'] == user_name][0]

    response = requests.delete(url=f"{base_url}/user/{user_id}",
                               headers={"Authorization": f"Basic {token}"})

    if response.status_code < 200 or response.status_code >= 300:
        errmsg = f'Error Code {response.status_code}: {response.text}'
        log.error(errmsg)
        raise Exception(errmsg)
    else:
        log.info(f"User {user_name} has been deleted")
