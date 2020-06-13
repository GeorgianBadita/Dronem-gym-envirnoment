"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   21.03.2020 00:54
"""
from typing import List

from env_interpretation import State, settings
import numpy as np


def gcd(a: int, b: int) -> int:
    """
    Function to compute the gcd of two numbers
    :return: gcd of a and b
    """

    if b == 0:
        return a
    return gcd(b, a % b)


def lcm(a: int, b: int) -> int:
    """
    Function to compute the lcm of two numbers
    :return: lcm of a and b
    """
    return a * b // gcd(a, b)


def check_if_done(state: State, max_iter: int = settings.MAXIMUM_NUM_ITER) -> bool:
    if state.time >= max_iter:
        return True
    return (np.array(state.robots_data[1:]) == 0).all()


def n_from_prod(arrays: List[List[int]], arr: List[int]):
    assert len(arrays) == len(arr)
    n = 0
    for i in range(len(arr)):
        idx = arrays[i].index(arr[i])
        mult = np.prod([len(p) for p in arrays[i + 1:]], dtype=int)
        n += idx * mult

    return int(n)
