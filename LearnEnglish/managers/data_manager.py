import json
from managers.time_manager import get_date


def save_data(directory, file_name, **kwargs):
    with open(f'data/{directory}/{file_name}.json', 'w') as file:
        json.dump(kwargs, file, indent=4)


def read_data(folder: str, file: str):
    with open(f'data/{folder}/{file}.json', 'r') as f:
        return json.load(f)


def update_data(telegram, **kwargs):
    data = read_data(f'users/{telegram}', telegram)
    for key, value in kwargs.items():
        if key in data.keys():
            for key2, value2 in value.items():
                data[key][key2] = value2
    save_data(f'users/{telegram}', telegram, **data)


