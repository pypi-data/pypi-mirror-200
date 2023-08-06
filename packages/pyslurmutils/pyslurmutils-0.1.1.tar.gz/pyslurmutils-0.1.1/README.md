# pyslurmutils

SLURM utilities for Python.

## Demo

Get an access token on rnice

```bash
export SLURM_TOKEN=$(scontrol token lifespan=3600)
export SLURM_URL=...
export SLURM_USER=...
```

Run any of the example scripts

```bash
python3 scripts/examples.py
```

Run the tests (CI or locally)

```bash
python3 -m pytest .
```

When `SLURM_TOKEN`, `SLURM_URL` or `SLURM_USER` is missing it will mock
the SLURM clients.

## Execute a python function on SLURM

Execute a function on SLURM with an API similar to python's `concurrent.futures`

```python
from pyslurmutils.concurrent.futures import SlurmRestExecutor

with SlurmRestExecutor(
    url,
    user_name,
    token,
    log_directory="/path/to/log",  # for log files
    data_directory="/path/to/data",  # TCP when not provided
    pre_script="module load ewoks",  # load environment
    python_cmd="python",
) as pool:

    future = pool.submit(sum, [1, 1])
    assert future.result() == 2
```
