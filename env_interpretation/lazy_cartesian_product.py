"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   04.04.2020 17:34
"""
from typing import List, Any
from bigfloat import *


class LazyCartesianProduct:
    """
    Class for generating the lazy cartesian product
    """

    def __init__(self, sets: List[List[Any]]):
        self.__sets = sets
        self.__max_size = 0
        self.__factors = [0] * len(self.__sets)
        self.__modulo = [0] * len(self.__sets)
        self.__compute()

    @property
    def max_size(self):
        return self.__max_size

    def __compute(self) -> None:
        fac = 1
        self.__max_size = 1
        for i in range(len(self.__sets) - 1, -1, -1):
            items = len(self.__sets[i])
            self.__max_size *= items
            self.__factors[i] = fac
            self.__modulo[i] = items
            fac *= items

    def get_nth_element(self, n: int) -> List[Any]:
        if n < 0 or n >= self.__max_size:
            raise ValueError("Invalid value of n")
        res = []
        for i in range(len(self.__sets)):
            res.append(self.__sets[i][int(mod(div(BigFloat(n), BigFloat(self.__factors[i])), self.__modulo[i]))])

        return res
