import json
import os

from adventure.models import Direction
from adventure.models import Gender


def load_fixture(fixture_file, model_cls):
    """Load the fixtures from a JSON file into model_cls objects.

    Arguments:
        fixture_file (str): path to a json file
        model_cls (type): class to use when instantiating fixtures
    """
    with open(fixture_file) as f:
        json_objs = json.loads(f.read())
    return [model_cls(**obj) for obj in json_objs]


dir_path = os.path.dirname(os.path.realpath(__file__))
genders = load_fixture(os.path.join(dir_path, 'genders.json'), Gender)
directions = load_fixture(os.path.join(dir_path, 'directions.json'), Direction)
