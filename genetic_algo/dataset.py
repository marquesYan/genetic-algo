"""Load dataset from file into memory"""

import json

from .structures import DatasetItem, Dataset, DatasetOptions


def load_from_file(path: str) -> Dataset:
    with open(path) as fp:
        content = json.load(fp)

    items = []
    for item in content["items"]:
        items.append(DatasetItem(**item))

    return Dataset(
        options=DatasetOptions(
            **content["options"],
        ),
        items=items,
    )
