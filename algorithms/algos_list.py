from functools import partial

from algorithms.naive import NaiveAlgo
from algorithms.most_crowded import MCAlgo
# from algorithms.most_crowded_time_limit import MCTL
from algorithms.relative_longest_q import RLQTL, RLQRS
from algorithms.cost_based import CostBased

MCTL = partial(MCAlgo, time_limit=10)
