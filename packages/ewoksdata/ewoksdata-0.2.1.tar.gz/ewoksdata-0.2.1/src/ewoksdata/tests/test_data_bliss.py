import pytest
from ..data import bliss


@pytest.mark.parametrize("lima_names", [(), ("p3",), ("p3", "p4")])
@pytest.mark.parametrize("counter_names", [(), ("diode1",), ("diode1", "diode2")])
def test_iter_bliss_data(lima_names, counter_names, bliss_scan):
    nexpected = len(lima_names) + len(counter_names)
    index = None
    for index, data in bliss.iter_bliss_data(
        str(bliss_scan), 2, lima_names=lima_names, counter_names=counter_names
    ):
        assert len(data) == nexpected
        if "diode1" in counter_names:
            assert data["diode1"] == index
        if "diode2" in counter_names:
            assert data["diode2"] == index
        if "p3" in counter_names:
            assert (data["p3"] == index).all()
        if "p4" in counter_names:
            assert (data["p4"] == index).all()

    if nexpected:
        assert index == 30
    else:
        assert index is None
