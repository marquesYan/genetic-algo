"""Data structures used for genetic algorithm"""

import secrets
from dataclasses import dataclass
from typing import List, Tuple


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

    # How many genes at most to apply the crossover
    most_crossover_genes: int = 4

    def __post_init__(self):
        # FIXME make sure most_crossover_genes is not
        # greater than genes size
        pass


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

    def clone(self) -> "Individual":
        return Individual(
            self.genes.copy(),
            self.fitness,
            self.selected,
        )

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

    def add_all(self, *individuals: Individual) -> None:
        self.individuals.extend(individuals)

    def sort(self) -> None:
        self.individuals.sort(key=lambda i: i.fitness)

    def __getitem__(self, index: int) -> Individual:
        return self.individuals[index]

    def __iter__(self) -> Individual:
        return self.individuals.__iter__()

    def __len__(self) -> Individual:
        return len(self.individuals)


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
    
    def apply_crossover(self) -> None:
        selecteds: List[Individual] = list(filter(
            lambda individual: individual.selected,
            self.population
        ))

        # Make sure selecteds are even, so we have
        # two parent always
        if len(selecteds) % 2 != 0:
            self.population.sort()

            # FIXME should we make sure the most adapted is selected?
            most_adapted = self.population[0]

            selecteds.append(most_adapted)

        for index in range(0, len(selecteds) - 1, 2):
            parent_a = selecteds[index]
            parent_b = selecteds[index + 1]

            childs = crossover(
                parent_a,
                parent_b,
                self.dataset.options.most_crossover_genes
            )

            self.population.add_all(*childs)


def crossover(
    parent_a: Individual,
    parent_b: Individual,
    most_crossover_genes: int,
) -> Tuple[Individual, Individual]:
    child_a = parent_a.clone()
    child_b = parent_b.clone()

    # Take a random number of genes to change
    for _ in range(secrets.randbelow(most_crossover_genes + 1)):
        index = secrets.randbelow(len(parent_a.genes) + 1)

        child_a.genes[index] = parent_b.genes[index]
        child_b.genes[index] = parent_a.genes[index]

    return child_a, child_b
