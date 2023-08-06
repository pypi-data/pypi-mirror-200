import os
import getpass
import logging


_LOG_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}


def add_parameters(parser):
    parser.add_argument(
        "-l",
        "--log",
        dest="log_level",
        type=str.lower,
        choices=list(_LOG_LEVELS),
        default="warning",
        help="Log level (default: %(default)s)",
    )
    parser.add_argument(
        "-u",
        "--user",
        dest="user_name",
        type=str,
        default=os.environ.get("SLURM_USER", getpass.getuser()),
        help="User name (default: %(default)s)",
    )
    parser.add_argument(
        "-t",
        "--token",
        type=str,
        default=os.environ.get("SLURM_TOKEN"),
        help="Slurm access token (default: %(default)s)",
    )
    parser.add_argument(
        "--url",
        type=str,
        default=os.environ.get("SLURM_URL"),
        help="Slurm Rest Server (default: %(default)s)",
    )
    parser.add_argument(
        "--log-dir",
        dest="log_directory",
        type=str,
        default=os.path.join(os.path.sep, "tmp_14_days", "{user_name}", "slurm_logs"),
        help="Directory of Slurm job logs (default: %(default)s)",
    )


def apply_parameters(args):
    logging.basicConfig(level=_LOG_LEVELS[args.log_level])
