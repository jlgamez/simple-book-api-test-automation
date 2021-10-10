import json


def load_data_from_file(file):
    with open(file) as cnfg_file:
        config_data = json.load(cnfg_file)
    return config_data
