import json
from itertools import accumulate

import pytest

from earcut import deviation, earcut


@pytest.mark.parametrize(
    "name,num_triangles,error",
    [
        ("building", 13, 0),
        ("dude", 106, 2e-15),
        ("water", 2482, 0.0008),
        ("water2", 1212, 0),
        ("water3", 197, 0),
        ("water3b", 25, 0),
        ("water4", 705, 0),
        ("water-huge", 5177, 0.0011),
        ("water-huge2", 4462, 0.0028),
        ("degenerate", 0, 0),
        ("bad-hole", 42, 0.019),
        ("empty-square", 0, 0),
        ("issue16", 12, 4e-16),
        ("issue17", 11, 2e-16),
        ("steiner", 9, 0),
        ("issue29", 40, 2e-15),
        ("issue34", 139, 0),
        ("issue35", 844, 0),
        ("self-touching", 124, 2e-13),
        ("outside-ring", 64, 0),
        ("simplified-us-border", 120, 0),
        ("touching-holes", 57, 0),
        ("hole-touching-outer", 77, 0),
        ("hilbert", 1024, 0),
        ("issue45", 10, 0),
        ("eberly-3", 73, 0),
        ("eberly-6", 1429, 2e-14),
        ("issue52", 109, 0),
        ("shared-points", 4, 0),
        ("bad-diagonals", 7, 0),
        ("issue83", 0, 0),
        ("issue107", 0, 0),
        ("issue111", 19, 0),
        ("boxy", 57, 0),
        ("collinear-diagonal", 14, 0),
        ("issue119", 18, 0),
        ("hourglass", 2, 0),
        ("touching2", 8, 0),
        ("touching3", 15, 0),
        ("touching4", 20, 0),
        ("rain", 2681, 0),
        ("issue131", 12, 0),
        ("infinite-loop-jhl", 0, 0),
        ("filtered-bridge-jhl", 25, 0),
        ("issue149", 2, 0),
        ("issue142", 4, 0.13),
    ],
)
def test_foo(name, num_triangles, error):
    with open(f"./tests/fixtures/{name}.json") as f:
        polygon = json.loads(f.read())

    data = [v for ring in polygon for point in ring for v in point]
    holeIndices = list(accumulate(len(r) for r in polygon))[:-1]

    triangles = earcut(data, holeIndices, 2)
    assert len(triangles) == num_triangles * 3
    if triangles:
        assert deviation(data, holeIndices, 2, triangles) <= error
