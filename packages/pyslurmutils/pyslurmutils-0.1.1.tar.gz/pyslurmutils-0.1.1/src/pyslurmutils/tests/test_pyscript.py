import pytest


@pytest.mark.parametrize("pre_script", [None, "echo 'run pre script'"])
@pytest.mark.parametrize("post_script", [None, "echo 'run post script'"])
def test_python_script(pre_script, post_script, slurm_python_client):
    future = slurm_python_client.spawn(
        sum, args=([1, 1],), pre_script=pre_script, post_script=post_script
    )
    try:
        assert future.result() == 2
        assert slurm_python_client.get_status(future.job_id) == "COMPLETED"
    finally:
        slurm_python_client.print_stdout_stderr(future.job_id)
        slurm_python_client.clean_job_artifacts(future.job_id)


def test_failing_python_script(slurm_python_client):
    future = slurm_python_client.spawn(sum, args=([1, "abc"],))
    try:
        with pytest.raises(TypeError):
            future.result()
        assert slurm_python_client.get_status(future.job_id) == "COMPLETED"
    finally:
        slurm_python_client.print_stdout_stderr(future.job_id)
        slurm_python_client.clean_job_artifacts(future.job_id)
