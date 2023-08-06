"""Monitor SLURM jobs and status"""

import sys
import time
import argparse
import datetime
from typing import List, Any
from tabulate import tabulate

from .cli import common as common_cli
from .cli import status as status_cli
from .cli import cancel as cancel_cli
from .cli import submit as submit_cli
from ..client import SlurmScriptRestClient


def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(
        description="Slurm Job Monitor", prog="pyslurmutils"
    )
    subparsers = parser.add_subparsers(help="Commands", dest="command")

    check = subparsers.add_parser("check", help="Check slurm connection")
    common_cli.add_parameters(check)

    status = subparsers.add_parser("status", help="Job status")
    common_cli.add_parameters(status)
    status_cli.add_parameters(status)

    status = subparsers.add_parser("cancel", help="Cancel Slurm jobs")
    common_cli.add_parameters(status)
    cancel_cli.add_parameters(status)

    status = subparsers.add_parser("submit", help="Submit Slurm jobs")
    common_cli.add_parameters(status)
    submit_cli.add_parameters(status)

    args = parser.parse_args(argv[1:])

    if args.command == "status":
        command_status(args)
    elif args.command == "check":
        command_check(args)
    elif args.command == "cancel":
        command_cancel(args)
    elif args.command == "submit":
        command_submit(args)
    else:
        parser.print_help()
    return 0


def command_status(args):
    common_cli.apply_parameters(args)
    status_cli.apply_parameters(args)

    with SlurmScriptRestClient(
        args.url,
        args.user_name,
        args.token,
        log_directory=args.log_directory,
    ) as client:
        for _ in _monitor_loop(args.interval):
            _print_jobs(client, args.jobid, args.all)
            if args.jobid:
                client.print_stdout_stderr(args.jobid)


def command_check(args):
    common_cli.apply_parameters(args)

    with SlurmScriptRestClient(
        args.url,
        args.user_name,
        args.token,
        log_directory=args.log_directory,
    ) as client:
        assert client.server_has_api(), "Wrong Rest API version"


def command_cancel(args):
    common_cli.apply_parameters(args)
    cancel_cli.apply_parameters(args)
    with SlurmScriptRestClient(
        args.url,
        args.user_name,
        args.token,
        log_directory=args.log_directory,
    ) as client:
        job_ids = args.job_ids
        if not job_ids:
            job_ids = client.get_all_job_properties()
        for job_id in job_ids:
            client.cancel_job(job_id)


def command_submit(args):
    common_cli.apply_parameters(args)
    submit_cli.apply_parameters(args)
    with SlurmScriptRestClient(
        args.url,
        args.user_name,
        args.token,
        parameters=args.parameters,
        log_directory=args.log_directory,
    ) as client:
        job_id = client.submit_script(args.script)
        print(f"Slurm job {job_id} started")
        try:
            client.wait_done(job_id)
            client.print_stdout_stderr(job_id)
        finally:
            client.clean_job_artifacts(job_id)


def _monitor_loop(interval):
    try:
        if not interval:
            yield
            return
        while True:
            yield
            time.sleep(interval)
    except KeyboardInterrupt:
        pass


def _print_jobs(client, jobid, all_users):
    if jobid:
        jobs = [client.get_job_properties(jobid)]
    else:
        if all_users:
            filter = {"user_name": None}
        else:
            filter = None
        jobs = client.get_all_job_properties(filter=filter)

    columns = {
        "ID": (_passthrough, ("job_id",)),
        "Name": (_passthrough, ("name",)),
        "State": (_passthrough, ("job_state",)),
        "User": (_passthrough, ("user_name",)),
        "Limit": (_time_limit, ("time_limit",)),
        "Pending": (_pending_time, ("submit_time", "start_time")),
        "Runtime": (_running_time, ("start_time", "end_time", "job_state")),
        "Resources": (_resources, ("partition", "tres_req_str", "tres_alloc_str")),
    }
    rows = list()
    for info in jobs:
        rows.append(
            [
                parser(*[info[k] if isinstance(k, str) else k for k in parser_args])
                for parser, parser_args in columns.values()
            ]
        )
    if not rows:
        return
    titles = list(columns)
    print(_format_info(titles, rows))


def _passthrough(x: Any) -> str:
    return str(x)


def _time_limit(x: int) -> str:
    return str(datetime.timedelta(minutes=x))


def _resources(partition: str, requested: str, allocated: str) -> str:
    return f"{partition}: {requested or allocated}"


def _pending_time(submit_time: int, start_time: int) -> str:
    return _time_diff(submit_time, start_time)


def _running_time(start_time: int, end_time: int, state: str) -> str:
    if state == "PENDING":
        return "-"
    if state in ("RUNNING", "COMPLETING"):
        end_time = 0
    return _time_diff(start_time, end_time)


def _time_diff(t0: int, t1: int) -> str:
    duration = _get_datetime(t1) - _get_datetime(t0)
    if duration.total_seconds() < 0:
        return "-"
    return str(duration)


def _get_datetime(epoch: int) -> datetime.datetime:
    if epoch == 0:
        now = datetime.datetime.now()
        return now.replace(microsecond=0)
    else:
        return datetime.datetime.fromtimestamp(epoch)


def _format_info(titles: List[str], rows: List[List[str]]) -> str:
    maxcolwidths = [None] * len(titles)
    maxcolwidths[1] = 40
    return tabulate(rows, headers=titles, maxcolwidths=maxcolwidths)


if __name__ == "__main__":
    sys.exit(main())
