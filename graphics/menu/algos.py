from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Type

import pygame

from algorithms.algo_to_index import index_to_algo
from algorithms.ml_algo import MLAlgo

all_algos_list = list(index_to_algo.values())[1:]
all_algos_list.append(MLAlgo)


@dataclass
class Algo:
    algo_class: Type
    x: int
    y: int
    width: int
    height: int
