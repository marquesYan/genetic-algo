"""Data structures used for genetic algorithm"""

from random import shuffle
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
    # Value with the ideal weight
    expected_weight: float

    selection_size: int = 10

    # How many generations to run
    max_generations: int = 100

    # How many individuals to use for each generation
    population_size: int = 100

    # How many genes at most to apply the crossover
    most_crossover_genes: int = 4

    # How many individuals at most to mutate
    most_mutation_individuals: int = 10

    # How many genes at most to mutate
    most_mutation_genes: int = 2

    def __post_init__(self):
        # FIXME make sure most_crossover_genes is not
        # greater than genes size
        pass


@dataclass
class Dataset:
    # Items to test
    items: List[DatasetItem]

    options: DatasetOptions


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
        
        if weight > dataset.options.expected_weight:
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

    def sort_by_fitness(self) -> None:
        self.individuals.sort(
            reverse=True,
            key=lambda i: i.fitness
        )

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

    @staticmethod
    def from_dataset(dataset: Dataset) -> "SteamRoller":
        return SteamRoller(
            dataset,
            Population.random(
                dataset.options.population_size,
                len(dataset.items),
            )
        )

    def evaluate_population(self) -> None:
        for i in self.population:
            i.evaluate(self.dataset)

    def select_population(self) -> None:
        """
        Select population that would be selected to the next generation.
        It uses the "rollet" algorithm for the selection process.
        """
        lower = 0
        for i in self.population:
            if i.fitness < lower:
                lower = i.fitness

        if lower < 0:
            for i in self.population:
                i.fitness -= lower

        self.population.sort_by_fitness()

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
            self.population.sort_by_fitness()

            # FIXME should we make sure the most adapted is selected?
            most_adapted = self.population[0]

            selecteds.append(most_adapted)
        
        # Ensure parents are randomly assigned
        shuffle(selecteds)

        for index in range(0, len(selecteds) - 1, 2):
            parent_a = selecteds[index]
            parent_b = selecteds[index + 1]

            childs = crossover(
                parent_a,
                parent_b,
                self.dataset.options.most_crossover_genes
            )

            self.population.add_all(*childs)

    def apply_mutation(self) -> None:
        mutation_len = secrets.randbelow(
            self.dataset.options.most_mutation_individuals
        )

        # Loop through all randomly selected individuals
        for _ in range(mutation_len):
            index = secrets.randbelow(len(self.population))
            target = self.population[index]
            mutate(target, self.dataset.options.most_mutation_genes)

    def apply_artificial_filter(self) -> None:
        # TODO ability to apply elitism

        new_individuals = list(
            filter(
                lambda individual: individual.selected,
                self.population,
            )
        )

        self.population = Population(new_individuals[:self.dataset.options.population_size])

    def smash(self) -> Population:
        # FIXME what to return here?
        for self.generation in range(self.dataset.options.max_generations):
            self.evaluate_population()
            self.select_population()
            self.apply_crossover()
            self.apply_mutation()
            self.evaluate_population()
            self.apply_artificial_filter()            

        return self.population

def crossover(
    parent_a: Individual,
    parent_b: Individual,
    most_crossover_genes: int,
) -> Tuple[Individual, Individual]:
    child_a = parent_a.clone()
    child_b = parent_b.clone()

    # Take a random number of genes to change
    for _ in range(secrets.randbelow(most_crossover_genes + 1)):
        index = secrets.randbelow(len(parent_a.genes))

        child_a.genes[index] = parent_b.genes[index]
        child_b.genes[index] = parent_a.genes[index]

    return child_a, child_b


def mutate(invididual: Individual, most_mutation_genes: int) -> None:
    # Loop through all randomly selected genes
    for _ in range(secrets.randbelow(most_mutation_genes)):
        gene = secrets.randbelow(len(invididual.genes))
        invididual.genes[gene] ^= 1