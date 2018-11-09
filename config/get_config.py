import pathlib
import yaml


def get_config():
    path = pathlib.Path(__file__).parent / "config.yaml"
    with open(path, 'r') as file:
        config = yaml.load(file)
    return config
