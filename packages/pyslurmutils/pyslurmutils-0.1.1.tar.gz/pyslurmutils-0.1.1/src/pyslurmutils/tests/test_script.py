def test_script(slurm_base_client, slurm_script_client, slurm_env):
    nbefore = len(list(slurm_base_client.get_all_job_properties(update_time=None)))
    job_id = slurm_script_client.submit_script()
    try:
        try:
            assert slurm_script_client.wait_done(job_id) == "COMPLETED"
        finally:
            slurm_script_client.print_stdout_stderr(job_id)

        assert slurm_script_client.get_status(job_id) == "COMPLETED"
        nafter = len(list(slurm_base_client.get_all_job_properties(update_time=None)))
        if slurm_env["mock"]:
            # This might fail on a production SLURM queue
            assert (nafter - nbefore) == 1
    finally:
        slurm_base_client.clean_job_artifacts(job_id)


def test_failing_script(slurm_script_client):
    job_id = slurm_script_client.submit_script("fail")
    try:
        assert slurm_script_client.wait_done(job_id) == "FAILED"
        slurm_script_client.print_stdout_stderr(job_id)
    finally:
        slurm_script_client.clean_job_artifacts(job_id)


def test_cancel_script(slurm_base_client, slurm_script_client):
    job_id = slurm_script_client.submit_script()
    try:
        slurm_script_client.cancel_job(job_id)
        assert slurm_script_client.wait_done(job_id) == "CANCELLED"
        slurm_script_client.print_stdout_stderr(job_id)
    finally:
        slurm_base_client.clean_job_artifacts(job_id)
