import os
import h5py
from silx.io.url import DataUrl
from silx.io import h5py_utils


def ensure_nxclass(group: h5py.Group) -> None:
    if group.attrs.get("NX_class"):
        return
    groups = [s for s in group.name.split("/") if s]
    n = len(groups)
    if n == 0:
        group.attrs["NX_class"] = "NXroot"
    elif n == 1:
        group.attrs["NX_class"] = "NXentry"
    else:
        group.attrs["NX_class"] = "NXcollection"


def select_default_plot(nxdata):
    parent = nxdata.parent
    for name in nxdata.name.split("/")[::-1]:
        if not name:
            continue
        parent.attrs["default"] = name
        parent = parent.parent


def create_url(url: str, **open_options) -> DataUrl:
    url = DataUrl(url)
    filename = url.file_path()
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    open_options.setdefault("mode", "a")
    with h5py_utils.open_item(filename, "/", **open_options) as parent:
        data_path = url.data_path()
        if not data_path:
            data_path = ""
        groups = [""] + [s for s in data_path.split("/") if s]
        if len(groups) == 1:
            groups.append("results")
        data_path = "/".join(groups)
        groups[0] = "/"

        ensure_nxclass(parent)
        for group in groups:
            if group in parent:
                parent = parent[group]
            else:
                parent = parent.create_group(group)
            ensure_nxclass(parent)

        return DataUrl(f"{filename}::{data_path}")


def get_nxentry(h5item):
    parts = [s for s in h5item.name.split("/") if s]
    if parts:
        return h5item.file[parts[0]]
    else:
        raise ValueError("HDF5 item must be part of an NXentry")
