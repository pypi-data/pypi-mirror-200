import h5py
import numpy
from ..data.hdf5.dataset_writer import DatasetWriter


def test_dataset_writer_variable_points(tmpdir):
    expected = list()
    filename = str(tmpdir / "test.h5")
    with h5py.File(filename, mode="w") as f:
        with DatasetWriter(f, "data") as writer:
            for _ in range(11):
                data = numpy.random.random((10, 20))
                writer.add_point(data)
                expected.append(data)
    with h5py.File(filename, mode="r") as f:
        data = f["data"][()]
    numpy.testing.assert_allclose(data, expected)
