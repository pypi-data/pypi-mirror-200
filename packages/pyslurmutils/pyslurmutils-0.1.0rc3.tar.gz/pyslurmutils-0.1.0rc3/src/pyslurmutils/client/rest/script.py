"""SLURM API to submit, cancel and monitor scripts"""

from numbers import Number
import time
import logging
from pprint import pformat
from typing import Optional
from .base import SlurmBaseRestClient
from .. import defaults

_logger = logging.getLogger(__name__)

_DEFAULT_SUCCESS_SCRIPT = """
echo 'Job started'
sleep 1
echo 'Job finished'
"""

_DEFAULT_FAIL_SCRIPT = """
echo 'Job started'
exit 3
"""


_DEFAULT_SCRIPTS = {None: _DEFAULT_SUCCESS_SCRIPT, "fail": _DEFAULT_FAIL_SCRIPT}


class SlurmScriptRestClient(SlurmBaseRestClient):
    """SLURM API to submit, cancel and monitor scripts.
    This class does not contain any job-related state."""

    def submit_script(self, script: Optional[str] = None, **kw) -> int:
        """Submit a script. Assume it is a bash script in the absence of a shebang."""
        script = _DEFAULT_SCRIPTS.get(script, script)
        if not script.startswith("#!"):
            script = f"{defaults.SHEBANG}\n" + script
        return self.submit_job(script, **kw)

    def get_status(self, job_id: int, request_options=None) -> str:
        # https://curc.readthedocs.io/en/latest/running-jobs/squeue-status-codes.html
        properties = self.get_job_properties(job_id, request_options=request_options)
        return properties.get("job_state", "UNKNOWN")

    def get_full_status(self, job_id: int, request_options=None) -> dict:
        properties = self.get_job_properties(job_id, request_options=request_options)
        return {
            "status": properties.get("job_state", "UNKNOWN"),
            "description": properties.get("state_description", ""),
            "reason": properties.get("state_reason", ""),
            "exit_code": self._parse_exit_code(properties.get("exit_code", "")),
        }

    def _parse_exit_code(self, exit_code: Optional[int]) -> Optional[int]:
        if not exit_code:
            return
        return exit_code // 256

    def wait_done(
        self,
        job_id: int,
        progress: bool = False,
        timeout: Optional[Number] = None,
        period: float = 0.5,
    ) -> str:
        job_state = None
        t0 = time.time()
        while job_state not in ("FAILED", "COMPLETED", "CANCELLED"):
            job_state = self.get_status(job_id)
            time.sleep(period)
            if progress:
                print(".", end="", flush=True)
            if timeout is not None and (time.time() - t0) > timeout:
                raise TimeoutError
        status = self.get_full_status(job_id)
        _logger.info("Job '%s' finished: {%s}", job_id, pformat(status))
        return job_state

    def print_stdout_stderr(self, job_id: int):
        stdout, stderr = self.get_stdout_stderr(job_id, raise_on_error=False)
        print()
        print("".join(stdout.lines()))
        print("".join(stderr.lines()))

    def log_stdout_stderr(
        self, job_id: int, logger=None, level=logging.INFO, **kw
    ) -> None:
        if logger is None:
            logger = _logger
        stdout, stderr = self.get_stdout_stderr(job_id, raise_on_error=False)
        stdout = "".join(stdout.lines())
        stderr = "".join(stderr.lines())
        logger.log(level, "\n%s\n%s", stdout, stderr, **kw)
