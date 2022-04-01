"""Load dataset from file into memory"""

from dataclasses import asdict
from datetime import datetime
import json
import os
from pathlib import Path
from typing import List

from .structures import DatasetItem, Dataset, DatasetOptions, Individual


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


def save_result(dataset: Dataset, results: List[Individual]) -> None:
    # Create a directory for reports
    today = datetime.now().strftime("%Y-%m-%d")
    report_dir = Path("report", today)
    os.makedirs(report_dir, exist_ok=True)

    results_file = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.json")

    parsed_results = list(map(asdict, results))

    with open(report_dir / results_file, "w") as fp:
        json.dump({
            "dataset_options": asdict(dataset.options),
            "results": parsed_results,
        }, fp, indent=4)

    print(f"[+] Results saved at: {report_dir / results_file}")