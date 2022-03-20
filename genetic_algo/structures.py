"""Data structures used for genetic algorithm"""

from itertools import accumulate
import secrets
from dataclasses import dataclass, field
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
class DatasetOptions:
    selection_size: int = 10


@dataclass
class Dataset:
    # Value with the ideal weight
    expected_weight: float

    # Items to test
    items: List[DatasetItem]

    options: DatasetOptions = DatasetOptions()


@dataclass
class Individual:
    # All genes of the individual. Each value
    # can range from 0 to 1.
    genes: List[int]

    # Current fitness of individual, based in the
    # value assigned in it's genes and in the dataset
    # goal
    fitness: float = 0

    # Detemines whether the individual was selected
    # to the next generation
    selected: bool = False

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

    def sort(self) -> None:
        self.individuals.sort(key=lambda i: i.fitness)


@dataclass
class SteamRoller:
    dataset: Dataset
    population: Population
    generation: int = 0

    def evaluate_population(self) -> None:
        for i in self.population.individuals:
            i.evaluate(self.dataset)

    def select_population(self) -> None:
        """
        Select population that would be selected to the next generation.
        It uses the "rollet" algorithm for the selection process.
        """
        lower = 0
        for i in self.population.individuals:
            if i.fitness < lower:
                lower = i.fitness

        if lower < 0:
            for i in self.population.individuals:
                i.fitness -= lower

        self.population.sort()

        fitness_total = 0
        accumulated_fitness = []
        for i in self.population.individuals:
            fitness_total += i.fitness
            accumulated_fitness.append(fitness_total)

        for _ in range(self.dataset.options.selection_size):
            rand_fitness = secrets.randbelow(int(fitness_total + 1))

            for index, acct_fitness in enumerate(accumulated_fitness):
                if rand_fitness <= acct_fitness:
                    individual = self.population.individuals[index]
                    individual.selected = True
                    break