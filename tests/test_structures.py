import secrets

from genetic_algo.structures import Dataset, DatasetItem, Individual, Population


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
    items = [
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
    
    dataset = Dataset(
        expected_weight=20,
        items=items,
    )

    individual = Individual(genes=[1, 0, 0, 1])
    individual.evaluate(dataset)

    assert individual.fitness == 14


def test_individual_evaluation_with_penality(monkeypatch):
    items = [
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
    
    dataset = Dataset(
        expected_weight=12,
        items=items,
    )

    individual = Individual(genes=[1, 0, 0, 1])
    individual.evaluate(dataset)

    assert individual.fitness == -86
