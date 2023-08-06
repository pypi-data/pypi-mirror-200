from contextlib import contextmanager
from typing import Optional

from silx.io import h5py_utils


@contextmanager
def h5context(filename: str, h5path: Optional[str] = None, **openargs):
    with h5py_utils.File(filename, **openargs) as f:
        if h5path:
            yield f[h5path]
        else:
            yield f
