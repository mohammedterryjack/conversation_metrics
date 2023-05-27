from enum import Enum
from typing import List

from numpy import array


def weighted_average(values: List[float], weights: List[float]) -> float:
    weighted_sum = array(values).dot(weights)
    return weighted_sum / len(values)


def reaction(score_a: float, score_b: float) -> float:
    """the difference of scores measured"""
    return score_b - score_a


def reciprocation(score_a: float, score_b: float) -> float:
    """the similarity of scores measured"""
    return 1 / (1 + reaction(score_a, score_b) ** 2)


class MetricDefaults(Enum):
    WEIGHT = 1.0
