from pkg.m0 import t0
from pkg.m1 import t1
from pkg.m2 import t2
from pkg.m3 import t3
from pkg.m4 import t4
from pkg.m5 import t5


def test_all() -> None:
    assert t0().year >= 2020
    assert t1().year >= 2020
    assert t2().year >= 2020
    assert t3().year >= 2020
    assert t4().year >= 2020
    assert t5().year >= 2020
