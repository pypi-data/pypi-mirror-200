import builtins
from typing import List, Type
import tblib


class SlurmError(Exception):
    pass


class SlurmHttpError(SlurmError):
    pass


def raise_chained_errors(
    errors: List[str], exc_class: Type[Exception] = SlurmHttpError
):
    try:
        if len(errors) > 1:
            raise_chained_errors(errors[:-1], exc_class=exc_class)
    except exc_class as e:
        raise exc_class(errors[-1]) from e
    else:
        raise exc_class(errors[-1])


class RemoteSlurmException(SlurmError):
    pass


def remote_exception_from_tb(
    exc_cls: str, exc_msg: str, tb: str
) -> RemoteSlurmException:
    tb = tblib.Traceback.from_string(tb).as_traceback()
    try:
        exc_cls = getattr(builtins, exc_cls)
    except AttributeError:
        exc_cls = RemoteSlurmException
    return exc_cls(exc_msg).with_traceback(tb)


def reraise_remote_exception_from_tb(exc_cls: str, exc_msg: str, tb: str) -> None:
    raise remote_exception_from_tb(exc_cls, exc_msg, tb)
