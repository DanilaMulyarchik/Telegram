import json
from date import get_date


def settings_save(words: list, check: bool) -> None:
    data = {'words': words, 'check': check}
    with open(f'data/{get_date()}.json', 'w') as file:
        json.dump(data, file, indent=4)


def settings_read(parametr: str) -> str:
    with open(f'data/{get_date()}.json', 'r') as file:
        loaded_data = json.load(file)
        if parametr == 'words':
            return loaded_data['words']
        if parametr == 'check':
            return loaded_data['check']