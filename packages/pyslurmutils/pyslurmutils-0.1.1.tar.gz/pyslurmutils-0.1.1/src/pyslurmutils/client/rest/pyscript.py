"""SLURM API to submit, cancel and monitor python functions"""

import time
import logging
import json
import weakref
from uuid import uuid4
from typing import Any, Callable, Mapping, Optional, Tuple
from .script import SlurmScriptRestClient
from ..job_io import base_io
from ..job_io import tcp_io
from ..job_io import file_io
from .. import defaults
from .. import os_utils
from .. import utils

logger = logging.getLogger(__name__)


class SlurmPythonJobRestClient(SlurmScriptRestClient):
    """SLURM API to submit, cancel and monitor python functions.
    This class contains job-related state (needed to handle response)."""

    def __init__(
        self,
        *args,
        data_directory=None,
        max_workers: Optional[int] = None,
        pre_script: Optional[str] = None,
        post_script: Optional[str] = None,
        python_cmd: Optional[str] = None,
        **kw,
    ):
        if data_directory:
            data_directory = data_directory.format(**kw)
        self.data_directory = data_directory
        if data_directory:
            os_utils.makedirs(data_directory)
            self._io_handler = file_io.JobFileIoHandler(client=self)
        else:
            self._io_handler = tcp_io.JobTcpIoHandler(
                max_workers=max_workers, client=self
            )
        self.pre_script = pre_script
        self.post_script = post_script
        self.python_cmd = python_cmd
        super().__init__(*args, **kw)

    @property
    def io_handler(self) -> base_io.JobIoHandler:
        return self._io_handler

    def cleanup(self, wait: bool = True, cancel_futures: bool = False) -> None:
        """Cleanup in-memory artifacts but not on-disk artifacts (see `clean_all_job_artifacts`)"""
        self._io_handler.shutdown(wait=wait, cancel_futures=cancel_futures)
        super().cleanup(wait=wait)

    def clean_all_job_artifacts(self) -> None:
        """Cleanup on-disk artifacts"""
        for job_id in self._io_handler.get_job_ids():
            self.clean_job_artifacts(job_id)

    def spawn(
        self,
        func: Callable,
        args: Optional[Tuple] = None,
        kwargs: Optional[Mapping] = None,
        pre_script: Optional[str] = None,
        post_script: Optional[str] = None,
        python_cmd: Optional[str] = None,
        **submit_kw,
    ) -> base_io.Future:
        if kwargs:
            spawn_kw = kwargs.pop(defaults.SPAWN_ARGUMENTS_NAME, None)
        else:
            spawn_kw = None
        # Spawn arguments take priority upon collision
        submit_kw = utils.merge_mappings(submit_kw, spawn_kw)

        pre_script = submit_kw.pop("pre_script", pre_script)
        post_script = submit_kw.pop("post_script", post_script)
        python_cmd = submit_kw.pop("python_cmd", python_cmd)

        job_parameters = submit_kw.setdefault("parameters", dict())
        job_name = self._ensure_job_name(job_parameters)

        data = func, args, kwargs
        if self.data_directory:
            infile = f"{self.data_directory}/{job_name}.in.{str(uuid4())}.pkl"
            outfile = f"{self.data_directory}/{job_name}.out.%j.pkl"
            ctx = self._io_handler.start_job_io(data, infile, outfile)
            metadata = {"transfer": "file", "infile": infile, "outfile": outfile}
        else:
            ctx = self._io_handler.start_job_io(data)
            metadata = {"transfer": "tcp"}

        with ctx as (pyscript, environment, future):
            script = self._generate_script(
                pyscript,
                pre_script=pre_script,
                post_script=post_script,
                python_cmd=python_cmd,
            )
            job_environment = job_parameters.setdefault("environment", dict())
            job_environment.update(environment)
            job_id = self.submit_script(script=script, metadata=metadata, **submit_kw)
            future.job_id = job_id
        return future

    def _generate_script(
        self,
        script: str,
        pre_script: Optional[str] = None,
        post_script: Optional[str] = None,
        python_cmd: Optional[str] = None,
    ) -> str:
        if not pre_script:
            pre_script = self.pre_script
        if not post_script:
            post_script = self.post_script
        if not python_cmd:
            python_cmd = self.python_cmd
        if not python_cmd:
            python_cmd = defaults.PYTHON_CMD
        if not pre_script and not post_script:
            return f"#!/usr/bin/env {python_cmd}\n{script}"
        if not pre_script:
            pre_script = ""
        if not post_script:
            post_script = ""
        return f"{pre_script}\ntype {python_cmd}\n{python_cmd} <<EOF\n{script}EOF\n\n{post_script}"

    def get_result(self, job_id: int) -> Any:
        return self._io_handler.get_job_result(job_id)

    def get_future(self, job_id: int, **kw) -> Optional[base_io.Future]:
        future = self._io_handler.get_future(job_id)
        if future is not None:
            return future
        metadata = self._get_metadata(job_id, **kw)
        if not metadata:
            return None
        if metadata["transfer"] == "file":
            return file_io.Future(
                job_id=job_id,
                filename=metadata["outfile"],
                client=weakref.proxy(self),
            )

    def wait_done(self, job_id: int, *args, **kw) -> str:
        timeout = kw.get("timeout", None)
        t0 = time.time()
        status = super().wait_done(job_id, *args, **kw)
        if timeout is not None:
            timeout -= time.time() - t0
            timeout = max(timeout, 0)
        future = self._io_handler.get_future(job_id)
        if future is not None:
            future.exception(timeout=timeout)
        return status

    def clean_job_artifacts(self, job_id: int, raise_on_error=False, **kw):
        properties = self.get_job_properties(job_id, **kw)
        if properties is None:
            return None
        metadata = self._get_metadata(job_id, properties=properties, **kw)
        if not metadata:
            return
        if metadata["transfer"] == "file":
            self._cleanup_job_io_artifact(job_id, metadata["infile"])
            self._cleanup_job_io_artifact(job_id, metadata["outfile"])
        super().clean_job_artifacts(
            job_id, raise_on_error=raise_on_error, properties=properties, **kw
        )

    def _get_metadata(
        self, job_id: int, properties: Optional[dict] = None, **kw
    ) -> Optional[dict]:
        if properties is None:
            properties = self.get_job_properties(job_id, **kw)
        if properties is None:
            return None
        metadata = properties.get("comment")
        if metadata is None:
            return None
        return json.loads(metadata)
