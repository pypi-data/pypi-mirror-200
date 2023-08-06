import gc
import pickle
from concurrent.futures import CancelledError
from concurrent.futures import TimeoutError

import pytest

from ..client.job_io import file_io


def test_file_io(tmpdir):
    infile = str(tmpdir / "infile.pkl")
    outfile = str(tmpdir / "outfile.pkl")
    with file_io.JobFileIoHandler() as handler:
        with handler.start_job_io({"1"}, infile, outfile) as (script, env, future):
            with open(infile, "rb") as f:
                assert pickle.load(f) == {"1"}
            future.job_id = 1234
        with pytest.raises(TimeoutError):
            future.result(timeout=0)
        with open(outfile, "wb") as f:
            pickle.dump(({"1", "2"}, None), f)
        assert future.result() == {"1", "2"}


def test_file_io_cancel(tmpdir):
    infile = str(tmpdir / "infile.pkl")
    outfile = str(tmpdir / "outfile.pkl")
    with file_io.JobFileIoHandler() as handler:
        with handler.start_job_io({"1"}, infile, outfile) as (script, env, future):
            future.job_id = 1234
        future.cancel()
        with pytest.raises(CancelledError):
            future.result()


def test_file_io_cleanup(tmpdir):
    with file_io.JobFileIoHandler() as handler:
        infile = str(tmpdir / "infile1.pkl")
        outfile = str(tmpdir / "outfile1.pkl")
        with handler.start_job_io({"1"}, infile, outfile) as (script, env, future):
            with open(infile, "rb") as f:
                assert pickle.load(f) == {"1"}
            future.job_id = 1
        with pytest.raises(TimeoutError):
            future.result(timeout=0)
        with open(outfile, "wb") as f:
            pickle.dump(({"1", "2"}, None), f)
        assert future.result() == {"1", "2"}

        while gc.collect():
            pass
        assert set(handler.get_job_ids()) == {1}

        infile = str(tmpdir / "infile2.pkl")
        outfile = str(tmpdir / "outfile2.pkl")
        with handler.start_job_io({"1"}, infile, outfile) as (script, env, future):
            future.job_id = 2
        future.cancel()

        while gc.collect():
            pass
        assert set(handler.get_job_ids()) == {2}

    del future
    while gc.collect():
        pass
    assert not handler.get_job_ids()
