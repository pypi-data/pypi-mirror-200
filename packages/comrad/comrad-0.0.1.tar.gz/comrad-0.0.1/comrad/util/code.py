from typing import Callable

from pyodide_dill import dill


def code_to_text(func: Callable) -> str:
    """
    This function will attempt to access the source and globals of an object and write the source for these.
    """
    parts = []
    for name, mod in dill.detect.globalvars(func).items():
        parts.append(dill.source.importable(mod, alias=name))

    parts.append(dill.source.getsource(func))

    return "\n".join(parts)
