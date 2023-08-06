import pytest
from ..client.errors import SlurmHttpError


def test_version(slurm_base_client):
    assert slurm_base_client.server_has_api()


def test_wrong_job_wait(slurm_script_client):
    job_id = 0
    with pytest.raises(SlurmHttpError):
        slurm_script_client.wait_done(job_id)


def test_wrong_job_print(slurm_script_client):
    job_id = 0
    slurm_script_client.print_stdout_stderr(job_id)


def test_wrong_job_clean(slurm_base_client):
    job_id = 0
    slurm_base_client.clean_job_artifacts(job_id)
