import time
from ..client import SlurmPythonJobRestClient
from ..client.job_io.base_io import Future


class SlurmRestExecutor:
    def __init__(self, client=None, **kw) -> None:
        if client is None:
            self.client = SlurmPythonJobRestClient(**kw)
        else:
            self.client = client

    def submit(self, func, *args, **kwargs) -> Future:
        return self.client.spawn(func, args=args, kwargs=kwargs)

    def map(self, fn, *iterables, timeout=None):
        """From `concurrent.future._base.Executor`

        Returns an iterator equivalent to map(fn, iter).

        Args:
            fn: A callable that will take as many arguments as there are
                passed iterables.
            timeout: The maximum number of seconds to wait. If None, then there
                is no limit on the wait time.

        Returns:
            An iterator equivalent to: map(func, *iterables) but the calls may
            be evaluated out-of-order.

        Raises:
            TimeoutError: If the entire result iterator could not be generated
                before the given timeout.
            Exception: If fn(*args) raises for any values.
        """
        if timeout is not None:
            end_time = timeout + time.monotonic()

        fs = [self.submit(fn, *args) for args in zip(*iterables)]

        # Yield must be hidden in closure so that the futures are submitted
        # before the first iterator value is required.
        def result_iterator():
            try:
                # reverse to keep finishing order
                fs.reverse()
                while fs:
                    # Careful not to keep a reference to the popped future
                    if timeout is None:
                        yield fs.pop().result()
                    else:
                        yield fs.pop().result(end_time - time.monotonic())
            finally:
                for future in fs:
                    future.cancel()

        return result_iterator()

    def shutdown(self, wait: bool = True, cancel_futures: bool = False):
        self.client.cleanup(wait=wait, cancel_futures=cancel_futures)

    def __enter__(self):
        self.client.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown(wait=True)
        return self.client.__exit__(exc_type, exc_val, exc_tb)
