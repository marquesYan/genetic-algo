from argparse import ArgumentParser
from pprint import pprint

from .structures import SteamRoller
from .dataset import load_from_file, save_result
    


def main():
    parser = ArgumentParser()
    parser.add_argument(
        '-f', '--dataset-file', help='Dataset file to read',
        required=True
    )

    args = parser.parse_args()

    dataset = load_from_file(args.dataset_file)
    sr = SteamRoller.from_dataset(dataset)
    results = sr.smash()
    pprint(results[:5])

    save_result(dataset, results[:5])
