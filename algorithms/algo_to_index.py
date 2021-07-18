from algorithms.cost_based import CostBased
from algorithms.most_crowded import MCAlgo, MCTL
from algorithms.naive import NaiveAlgo
from algorithms.relative_longest_q import RLQTL, RLQRS

algo_to_index = {
    None: 0,
    NaiveAlgo: 1,
    MCAlgo: 2,
    MCTL: 3,
    RLQTL: 4,
    RLQRS: 5,
    CostBased: 6,
}

index_to_algo = {val: key for key, val in algo_to_index.items()}


def algos_list_to_num(algos):
    base = max(algo_to_index.values()) + 1
    algos_indices = [algo_to_index[algo.__class__] if algo is not None else algo_to_index[algo] for algo in algos]

    return sum(element * base ** i for i, element in enumerate(reversed(algos_indices)))
