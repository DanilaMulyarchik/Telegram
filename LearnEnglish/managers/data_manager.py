import json


def save_data(directory, file_name, **kwargs):
    with open(f'data/{directory}/{file_name}.json', 'w') as file:
        json.dump(kwargs, file, indent=4)


def read_data(folder: str, file: str):
    with open(f'data/{folder}/{file}.json', 'r') as f:
        return json.load(f)


def update_data(telegram, **kwargs):
    data = read_data('users',telegram)['user']
    for key, value in kwargs.items():
        data[key] = value
    save_data('users', data['telegram'], user=data)