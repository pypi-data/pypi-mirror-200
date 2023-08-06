import os
from typing import Iterator, Optional

import pytest
from ..client import SlurmBaseRestClient
from ..client import SlurmScriptRestClient
from ..client import SlurmPythonJobRestClient
from ..concurrent.futures import SlurmRestExecutor
from .mock_slurm import mock_slurm_clients


@pytest.fixture(scope="session")
def slurm_log_directory(request, tmp_path_factory):
    path = request.config.getoption("slurm_log_directory")
    if path and path == "tmpdir":
        return str(tmp_path_factory.mktemp("slurm_log_root"))
    if path and not os.path.isdir(path):
        pytest.skip(f"{path} is not mounted")
    return path


@pytest.fixture(scope="session")
def slurm_data_directory(request, tmp_path_factory):
    path = request.config.getoption("slurm_data_directory")
    if path and path == "tmpdir":
        return str(tmp_path_factory.mktemp("slurm_data_root"))
    if path and not os.path.isdir(path):
        pytest.skip(f"{path} is not mounted")
    return path


@pytest.fixture(scope="session")
def slurm_env() -> dict:
    url = os.environ.get("SLURM_URL", "mock")
    token = os.environ.get("SLURM_TOKEN", "mock")
    user_name = os.environ.get("SLURM_USER", "mock")
    return {
        "url": url,
        "token": token,
        "user_name": user_name,
        "mock": url == "mock" or token == "mock" or user_name == "mock",
    }


@pytest.fixture(scope="session")
def log_directory(slurm_log_directory, tmp_path_factory, slurm_env) -> Optional[str]:
    if slurm_log_directory:
        return os.path.join(slurm_log_directory, slurm_env["user_name"], "slurm_log")
    elif slurm_env["mock"]:
        return str(tmp_path_factory.mktemp("slurm_log"))
    else:
        return None


@pytest.fixture(scope="session")
def data_directory(slurm_data_directory, slurm_env) -> Optional[str]:
    if slurm_data_directory:
        return os.path.join(slurm_data_directory, slurm_env["user_name"], "slurm_data")
    else:
        return None


@pytest.fixture(scope="session")
def slurm_config(log_directory, tmp_path_factory, slurm_env) -> dict:
    params = dict(slurm_env)
    mock = params.pop("mock")
    params["log_directory"] = log_directory
    if mock:
        tmpdir = tmp_path_factory.mktemp("slurm_mock")
        with mock_slurm_clients(tmpdir):
            yield params
    else:
        yield params


@pytest.fixture
def slurm_base_client(slurm_config) -> Iterator[SlurmBaseRestClient]:
    with SlurmBaseRestClient(**slurm_config) as client:
        yield client


@pytest.fixture
def slurm_script_client(slurm_config) -> Iterator[SlurmScriptRestClient]:
    with SlurmScriptRestClient(**slurm_config) as client:
        yield client


@pytest.fixture
def slurm_python_client(
    slurm_config, data_directory
) -> Iterator[SlurmPythonJobRestClient]:
    with SlurmPythonJobRestClient(
        max_workers=8, data_directory=data_directory, **slurm_config
    ) as client:
        yield client


@pytest.fixture
def slurm_pool(slurm_python_client) -> Iterator[SlurmRestExecutor]:
    with SlurmRestExecutor(client=slurm_python_client) as pool:
        yield pool
