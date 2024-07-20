import json
from managers.time_manager import get_date


def save_data(directory, file_name, **kwargs):
    with open(f'data/{directory}/{file_name}.json', 'w') as file:
        json.dump(kwargs, file, indent=4)


def read_data(folder: str, file: str):
    with open(f'data/{folder}/{file}.json', 'r') as f:
        return json.load(f)


def update_data(telegram, **kwargs):
    data = read_data('users', telegram)['user']
    marks = read_data('users', telegram)['marks']
    for key, value in kwargs.items():
        if key in data.keys():
            data[key] = value
        else:
            marks[key] = value
    if get_date() not in marks.keys():
        marks[get_date()] = 0
    save_data('users', data['telegram'], user=data, marks=marks)