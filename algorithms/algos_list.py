from functools import partial

from algorithms.most_crowded import MCAlgo

# from algorithms.most_crowded_time_limit import MCTL

MCTL = partial(MCAlgo, time_limit=10)
