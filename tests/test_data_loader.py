from dataclasses import asdict
import json
from pathlib import Path
from genetic_algo.structures import Dataset, DatasetItem
from genetic_algo.dataset import load_from_file


def test_load_dataset(tmpdir):
    dataset_items = [
        DatasetItem(
            name="Item1",
            value=1,
            weight=0.5,
        )
    ]

    dataset = Dataset(
        expected_weight=10,
        items=dataset_items,
    )

    dataset_file = tmpdir / Path("foo.json")

    with open(dataset_file, "w") as fp:
        json.dump(asdict(dataset), fp)

    result = load_from_file(dataset_file)

    assert result == dataset
