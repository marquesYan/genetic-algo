"""Data structures used for genetic algorithm"""

import secrets
from dataclasses import dataclass
from typing import List


@dataclass
class DatasetItem:
    # Identification of the item
    name: str

    # The fitness associated with item.
    # Higher fitness increases the chance of
    # the item to be considered in the solution
    fitness: int

    # The weight associated with the solution.
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

    # Current fitness of individual, based in the
    # value assigned in it's genes and in the dataset
    # goal
    fitness: float = 0

    @staticmethod
    def random(genes_size: int) -> "Individual":
        genes = []
        for _ in range(genes_size):
            genes.append(secrets.randbelow(2))
        return Individual(genes)

    def evaluate(self, dataset: Dataset) -> None:
        # Reset fitness
        self.fitness = 0

        # Weight of the individual based in the dataset
        weight = 0

        for index, gene in enumerate(self.genes):
            if gene == 1:
                item: DatasetItem = dataset.items[index]
                weight += item.weight
                self.fitness += item.fitness
        
        if weight > dataset.expected_weight:
            # FIXME improve penality system
            self.fitness -= 100

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
