"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   21.03.2020 00:58
"""
from env_interpretation.utils import gcd, lcm


def test_gcd():
    assert gcd(2, 1) == 1
    assert gcd(3, 5) == 1
    assert gcd(2, 6) == 2
    assert gcd(12, 6) == 6


def test_lcm():
    assert lcm(0, 2) == 0
    assert lcm(5, 6) == 30
    assert lcm(15, 5) == 15
