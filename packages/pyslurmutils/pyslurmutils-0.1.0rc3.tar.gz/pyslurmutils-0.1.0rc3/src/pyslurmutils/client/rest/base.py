"""Low-level SLURM API to submit, cancel and monitor jobs"""

import os
import logging
import json
import requests
from pprint import pformat
from dataclasses import dataclass
from typing import Iterator, List, Optional, Tuple, Union
from ..errors import SlurmHttpError, raise_chained_errors
from .. import defaults
from .. import os_utils

logger = logging.getLogger(__name__)


@dataclass
class StdInfo:
    """Information about a SLURM job stdout/stderr log file"""

    name: str
    filename: str
    content: Optional[List[str]]

    def lines(self) -> List[str]:
        title = f"{self.name}: {self.filename}\n"
        line = "-" * len(title) + "\n"
        if self.content is None:
            return [title, line, " <not found>"]
        elif not self.content:
            return [title, line, " <empty>"]
        else:
            return [title, line] + self.content


class SlurmBaseRestClient:
    """Low-level SLURM API to submit, cancel and monitor jobs.
    This class does not contain any job-related state."""

    VERSION = "0.0.37"

    def __init__(
        self,
        url: str = "",
        user_name: str = "",
        token: str = "",
        parameters: Optional[dict] = None,
        log_directory: Optional[str] = None,
        request_options: Optional[dict] = None,
    ):
        if not url:
            raise ValueError("Requires the SLURM REST url")
        if not token:
            raise ValueError("Requires a SLURM user token")
        if not user_name:
            raise ValueError("Requires a SLURM user name")
        self._url = url
        self.user_name = user_name.rstrip()
        self._token = token.replace("SLURM_JWT=", "").rstrip()
        self.parameters = parameters
        if log_directory:
            log_directory = log_directory.format(user_name=user_name)
        self.log_directory = log_directory
        self.request_options = request_options

    def cleanup(self, wait: bool = True) -> None:
        pass

    def __enter__(self) -> "SlurmBaseRestClient":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self.cleanup(wait=True)
        return False

    def get_headers(self) -> dict:
        return {"X-SLURM-USER-NAME": self.user_name, "X-SLURM-USER-TOKEN": self._token}

    def _parse_request_options(self, request_options: Optional[dict]) -> dict:
        if self.request_options:
            merged = dict(self.request_options)
        else:
            merged = dict()
        if request_options:
            merged.update(request_options)
        if merged.get("headers") is None:
            merged["headers"] = self.get_headers()
        return merged

    def get(
        self,
        path: str,
        request_options: Optional[dict] = None,
        error_msg: Optional[str] = None,
        raise_on_error: bool = True,
    ) -> dict:
        request_options = self._parse_request_options(request_options)
        response = requests.get(self._url + path, **request_options)
        return self._handle_response(
            response, raise_on_error=raise_on_error, error_msg=error_msg
        )

    def delete(
        self,
        path: str,
        request_options: Optional[dict] = None,
        error_msg: Optional[str] = None,
        raise_on_error: bool = True,
    ) -> dict:
        request_options = self._parse_request_options(request_options)
        response = requests.delete(self._url + path, **request_options)
        return self._handle_response(
            response, raise_on_error=raise_on_error, error_msg=error_msg
        )

    def post(
        self,
        path: str,
        json: Optional[dict] = None,
        request_options: Optional[dict] = None,
        raise_on_error: bool = True,
        error_msg: Optional[str] = None,
    ) -> dict:
        request_options = self._parse_request_options(request_options)
        if json:
            request_options["json"] = json
            logger.debug("POST %s\n%s", path, pformat(json))
        else:
            logger.debug("POST %s", path)
        response = requests.post(self._url + path, **request_options)
        return self._handle_response(
            response, raise_on_error=raise_on_error, error_msg=error_msg
        )

    def _handle_response(
        self, response, raise_on_error: bool = True, error_msg: Optional[str] = None
    ):
        try:
            response.raise_for_status()
        except Exception as e:
            if response.status_code in (400, 500):
                if not raise_on_error:
                    return dict()
                if not error_msg:
                    error_msg = str(e)
                if response.status_code == 500:
                    error_msg = f"{error_msg} (SLURM token expired?)"
                raise SlurmHttpError(error_msg)
            raise
        data = response.json()
        if raise_on_error:
            self._raise_on_error(data.get("errors"), error_msg=error_msg)
        return data

    def server_has_api(self, request_options: Optional[dict] = None) -> bool:
        response = self.get("/openapi", request_options=request_options)
        return self.VERSION == response["info"]["version"]

    def submit_job(
        self,
        script: str,
        parameters: Optional[dict] = None,
        metadata: Optional[Union[str, dict]] = None,
        request_options: Optional[dict] = None,
    ) -> int:
        """Returns the SLURM job ID"""
        # https://slurm.schedmd.com/rest_api.html#slurmV0038SubmitJob
        job = self._create_job_properties(parameters=parameters, metadata=metadata)
        job_recipe = {"script": script, "job": job}
        job_name = job["name"]

        response = self.post(
            f"/slurm/v{self.VERSION}/job/submit",
            json=job_recipe,
            request_options=request_options,
            error_msg=f"failed to submit SLURM job '{job_name}'",
        )

        job_id = response["job_id"]
        user_msg = response.get("job_submit_user_msg", "")
        if user_msg:
            logger.info(
                "SLURM job '%s' submitted (Job ID: %s): %s", job_name, job_id, user_msg
            )
        else:
            logger.info("SLURM job '%s' submitted (Job ID: %s)", job_name, job_id)
        return job_id

    def cancel_job(self, job_id: int, request_options: Optional[dict] = None) -> None:
        # https://slurm.schedmd.com/rest_api.html#slurmV0038CancelJob
        self.delete(
            f"/slurm/v{self.VERSION}/job/{job_id}", request_options=request_options
        )

    def clean_job_artifacts(
        self, job_id: int, raise_on_error=False, properties: Optional[dict] = None, **kw
    ):
        if properties is None:
            properties = self.get_job_properties(
                job_id, raise_on_error=raise_on_error, **kw
            )
        if properties is None:
            return
        self._cleanup_job_io_artifact(job_id, properties.get("standard_output"))
        self._cleanup_job_io_artifact(job_id, properties.get("standard_error"))

    def get_job_properties(
        self, job_id: int, raise_on_error=True, request_options: Optional[dict] = None
    ) -> Optional[dict]:
        # https://slurm.schedmd.com/rest_api.html#slurmdbV0038GetJob
        response = self.get(
            f"/slurm/v{self.VERSION}/job/{job_id}",
            request_options=request_options,
            raise_on_error=raise_on_error,
            error_msg=f"Failed to get properties of SLURM Job ID {job_id}",
        )
        jobs = response.get("jobs", list())
        if len(jobs) != 1:
            return None
        return jobs[0]

    def get_all_job_properties(
        self,
        raise_on_error=True,
        request_options: Optional[dict] = None,
        filter=None,
        update_time=None,
    ) -> List[dict]:
        # https://slurm.schedmd.com/rest_api.html#slurmdbV0038GetJob
        path = f"/slurm/v{self.VERSION}/jobs"
        if update_time:
            path = f"{path}?update_time={update_time.timestamp()}"
        response = self.get(
            path,
            request_options=request_options,
            raise_on_error=raise_on_error,
            error_msg="failed to get SLURM job properties",
        )
        jobs = response.get("jobs", list())
        return list(self._filter_job_properties(jobs, filter))

    def _filter_job_properties(
        self, jobs: List[dict], filter: Optional[dict]
    ) -> Iterator[dict]:
        if filter is None:
            filter = dict()
        filter.setdefault("user_name", self.user_name)
        filter = {k: v for k, v in filter.items() if v is not None}
        for properties in jobs:
            if self._match_filter(properties, None, filter):
                yield properties

    def _match_filter(
        self, properties: dict, name: str, value: Optional[Union[str, dict]]
    ) -> bool:
        if name is None:
            return all(
                self._match_filter(properties, name, value)
                for name, value in value.items()
            )
        elif isinstance(value, str):
            return properties.get(name) == value
        else:
            properties = properties.get(name, dict())
            return all(self._match_filter(properties, k, v) for k, v in value.items())

    def get_stdout_stderr(self, job_id: int, **kw) -> Tuple[StdInfo, StdInfo]:
        properties = self.get_job_properties(job_id, **kw)
        if properties is None:
            properties = dict()
        filename = properties.get("standard_output")
        filename, content = self._read_log(job_id, filename)
        stdout = StdInfo(name="STDOUT", filename=filename, content=content)
        filename = properties.get("standard_error")
        filename, content = self._read_log(job_id, filename)
        stderr = StdInfo(name="STDERR", filename=filename, content=content)
        return stdout, stderr

    def _read_log(
        self, job_id: int, filename: Optional[str]
    ) -> Tuple[str, Optional[List[str]]]:
        filename = self._parse_filename(job_id, filename)
        if filename is None:
            return filename, None
        try:
            with open(filename) as f:
                return filename, list(f)
        except FileNotFoundError:
            return None, None

    def _cleanup_job_io_artifact(self, job_id: int, filename: Optional[str]) -> None:
        filename = self._parse_filename(job_id, filename)
        if filename is None or filename == "/dev/null":
            return None
        try:
            os.remove(filename)
        except FileNotFoundError:
            return None

    def _parse_filename(self, job_id: int, filename: Optional[str]) -> Optional[str]:
        if not filename:
            return None
        return filename.replace("%j", str(job_id))

    def _raise_on_error(
        self, errors: Optional[List[dict]], error_msg: Optional[str] = None
    ):
        if not errors:
            return
        errors = [self._parse_error(error) for error in errors]
        if error_msg:
            errors.append(error_msg + " (token expired?)")
        raise_chained_errors(errors)

    def _parse_error(self, error: dict) -> str:
        description = error.get("error", "<no error description>")
        description = error.get("description", description)
        error_code = error.get("error_code", "<no error code>")
        error_code = error.get("error_number", description)
        return f"{description} (error code: {error_code})"

    def _create_job_properties(
        self,
        parameters: Optional[dict] = None,
        metadata: Optional[Union[str, dict]] = None,
    ) -> dict:
        # https://slurm.schedmd.com/rest_api.html#v0.0.38_job_properties

        if self.parameters:
            job_parameters = dict(self.parameters)
        else:
            job_parameters = dict()
        if parameters:
            job_parameters.update(parameters)

        job_environment = job_parameters.get("environment")
        if job_environment is None:
            job_environment = dict()
            job_parameters["environment"] = job_environment
        if not job_environment:
            # Cannot be empty
            job_environment["DUMMY_VAR"] = "dummy_value"

        job_name = self._ensure_job_name(job_parameters)

        job_parameters["standard_input"] = "/dev/null"
        if self.log_directory:
            os_utils.makedirs(self.log_directory)
            filetemplate = f"{self.log_directory}/{job_name}.%j"
            job_parameters["standard_output"] = filetemplate + ".out"
            job_parameters["standard_error"] = filetemplate + ".err"
        else:
            job_parameters["standard_output"] = "/dev/null"
            job_parameters["standard_error"] = "/dev/null"

        if metadata:
            if not isinstance(metadata, str):
                metadata = json.dumps(metadata)
            job_parameters["comment"] = metadata

        return job_parameters

    def _ensure_job_name(self, job_parameters: dict) -> str:
        job_name = job_parameters.get("name")
        if not job_name:
            job_name = defaults.JOB_NAME
            job_parameters["name"] = job_name
        return job_name
