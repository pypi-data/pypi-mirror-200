from typing import Tuple
from silx.io.url import DataUrl


def h5dataset_url_parse(url: str) -> Tuple[str, str, Tuple]:
    obj = DataUrl(url)
    filename = str(obj.file_path())
    h5path = obj.data_path()
    if h5path is None:
        h5path = "/"
    idx = obj.data_slice()
    if idx is None:
        idx = tuple()
    return filename, h5path, idx
