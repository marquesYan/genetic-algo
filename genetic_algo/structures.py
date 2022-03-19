"""Data structures used for genetic algorithm"""

import secrets
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


@dataclass
class Individual:
    # All genes of the individual. Each value
    # can range from 0 to 1.
    genes: List[int]

    @staticmethod
    def random(genes_size: int) -> "Individual":
        genes = []
        for _ in range(genes_size):
            genes.append(secrets.randbelow(2))
        return Individual(genes)


@dataclass
class Population:
    # All individuals of population
    individuals: List[Individual]

    @staticmethod
    def random(individuals_size: int, genes_size: int) -> "Population":
        individuals = []
        for _ in range(individuals_size):
            individuals.append(Individual.random(genes_size))

        return Population(individuals)
