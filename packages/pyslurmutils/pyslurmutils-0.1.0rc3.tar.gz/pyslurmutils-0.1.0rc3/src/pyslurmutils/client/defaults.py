import socket

JOB_NAME = f"pyslurmutils.{socket.gethostname()}"  # keep filename friendly
PYTHON_CMD = "python3"
SHEBANG = "#!/bin/bash -l"
SPAWN_ARGUMENTS_NAME = "_slurm_spawn_arguments"
