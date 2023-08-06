import builtins
import io
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def custom_open():
    """
    Monkey patch open to use a temporary file instead of /dev/null when /dev/null is not available in random
    access mode, e.g. pyodide.

    :return:
    """
    import _pyio

    with tempfile.TemporaryDirectory() as dir:
        testfile = f"{dir}/notdevnull"
        Path(testfile).touch()
        old_open = _pyio.open

        def open_tempfile(_, *args, **kwargs):
            return old_open(testfile, *args, **kwargs)

        def new_open(*args, **kwargs):
            try:
                return old_open(*args, **kwargs)
            except io.UnsupportedOperation:
                return open_tempfile(*args, **kwargs)

        builtins.open = _pyio.open = new_open

        try:
            yield
        finally:
            builtins.open = _pyio.open = old_open


with custom_open():
    import dill

    sys.modules[dill.__name__] = dill

__all__ = ["dill"]
