import secrets
from unittest import mock

from genetic_algo.structures import Dataset, DatasetItem, DatasetOptions, Individual, Population, SteamRoller, crossover

DATASET_ITEMS = [
    DatasetItem(
        name="notebook",
        fitness=5,
        weight=7,
    ),
    DatasetItem(
        name="tv",
        fitness=8,
        weight=8,
    ),
    DatasetItem(
        name="ring",
        fitness=2,
        weight=10,
    ),
    DatasetItem(
        name="videogame",
        fitness=9,
        weight=6,
    ),
]

def test_random_individual(monkeypatch):
    fake_rand = [0, 1, 0, 1, 1]
    expected = Individual(genes=fake_rand.copy())

    def mockrand(*args):
        assert args == (2,)
        return fake_rand.pop(0)

    monkeypatch.setattr(secrets, "randbelow", mockrand)

    result = Individual.random(5)

    assert result == expected


def test_individual_evaluation(monkeypatch):    
    dataset = Dataset(
        expected_weight=20,
        items=DATASET_ITEMS,
    )

    individual = Individual(genes=[1, 0, 0, 1])
    individual.evaluate(dataset)

    assert individual.fitness == 14


def test_individual_evaluation_with_penality(monkeypatch):
    dataset = Dataset(
        expected_weight=12,
        items=DATASET_ITEMS,
    )

    individual = Individual(genes=[1, 0, 0, 1])
    individual.evaluate(dataset)

    assert individual.fitness == -86


def test_steam_roller_rollet_selection(monkeypatch):
    dataset = Dataset(
        expected_weight=20,
        items=DATASET_ITEMS,
        options=DatasetOptions(
            selection_size=1,
        )
    )

    individuals = [
        Individual(genes=[1, 0, 0, 1]),
        Individual(genes=[0, 1, 0, 1]),
    ]

    sr = SteamRoller(
        dataset,
        population=Population(
            individuals,
        )
    )

    def mockrand(*args):
        assert args == (32,)
        return 10

    monkeypatch.setattr(secrets, "randbelow", mockrand)

    sr.evaluate_population()
    sr.select_population()

    assert individuals[0].selected is True
    assert individuals[1].selected is False


def test_crossover_returns_flipped_genes(monkeypatch):
    parent_a = Individual(genes=[1, 0, 0, 1], selected=True)
    parent_b = Individual(genes=[0, 1, 0, 1], selected=True)
        
    expected_child_a = Individual(genes=[1, 1, 0, 1], selected=True)
    expected_child_b = Individual(genes=[0, 0, 0, 1], selected=True)

    monkeypatch.setattr(
        secrets,
        "randbelow",
        mock.Mock(side_effect=[2, 1, 3])
    )

    child_a, child_b = crossover(parent_a, parent_b, 4)

    assert child_a == expected_child_a
    assert child_b == expected_child_b


def test_steam_roller_apply_crossover_adds_childs_to_population(monkeypatch):
    dataset = Dataset(
        expected_weight=20,
        items=DATASET_ITEMS,
        options=DatasetOptions(
            selection_size=1,
            most_crossover_genes=2,
        )
    )

    sr = SteamRoller(
        dataset,
        population=Population.random(4, 2)
    )

    monkeypatch.setattr(secrets, "randbelow", lambda _: 1)

    sr.apply_crossover()

    assert len(sr.population) == 8
