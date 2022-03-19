"""Data structures used for genetic algorithm"""

from dataclasses import dataclass
from typing import List


@dataclass
class DatasetItem:
    name: str
    value: int
    weight: float

@dataclass
class Dataset:
    # Value with the ideal weight
    expected_weight: float

    # Items to test
    items: List[DatasetItem]
    