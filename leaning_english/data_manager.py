import json
from date import get_date


def data_save(words: list) -> None:
    data = {'words': words}
    with open(f'data/{get_date()}.json', 'w') as file:
        json.dump(data, file, indent=4)


def data_main_read() -> str:
    with open(f'data/main.json', 'r') as file:
        loaded_data = json.load(file)
        return loaded_data

def data_read() -> str:
    with open(f'data/{get_date()}.json', 'r') as file:
        loaded_data = json.load(file)
        return loaded_data