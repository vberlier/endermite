__all__ = ['build_guard', 'print_exc', 'crop_traceback_until']

from pathlib import Path
from contextlib import contextmanager
from traceback import print_exception


class BuildError(Exception):
    """Raised from another exception with some context information."""


@contextmanager
def build_guard(context_info):
    """Convert exceptions to BuildError with the given context information."""
    try:
        yield
    except BuildError: # pylint: disable = try-except-raise
        raise
    except Exception as exc:
        raise BuildError(context_info) from exc


def print_exc(exc):
    """Display an exception."""
    print_exception(exc.__class__, exc, exc.__traceback__)


def crop_traceback_until(exc, path):
    """Crop traceback information until a given path."""
    trace = exc.__traceback__
    while True:
        filepath = Path(trace.tb_frame.f_code.co_filename).absolute()
        if path in filepath.parents:
            exc.with_traceback(trace)
            break
        if not trace.tb_next:
            break
        trace = trace.tb_next
