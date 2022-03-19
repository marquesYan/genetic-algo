import secrets

from genetic_algo.structures import Individual, Population


def test_random_individual(monkeypatch):
    fake_rand = [0, 1, 0, 1, 1]
    expected = Individual(genes=fake_rand.copy())

    def mockrand(*args):
        assert args == (2,)
        return fake_rand.pop(0)

    monkeypatch.setattr(secrets, "randbelow", mockrand)

    result = Individual.random(5)

    assert result == expected