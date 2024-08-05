from managers.data_manager import read_data
from managers.time_manager import get_date


def get_action(telegram: str):
    return read_data(f'users/{telegram}', telegram)['user']['action']


def get_test_date(telegram: str):
    return read_data(f'users/{telegram}', telegram)['user']['test_date']


def get_day_mark(telegram: str):
    return int(read_data(f'users/{telegram}', telegram)['user']['day_mark'])


def get_mark(telegram: str):
    return int(read_data(f'users/{telegram}', telegram)['marks'][get_date()])


def get_all_mark(telegram: str) -> dict:
    return read_data(f'users/{telegram}', telegram)['marks']


def get_test_mark(telegram: str):
    return read_data(f'users/{telegram}', telegram)['test_marks'][get_date()]


def get_all_test_mark(telegram: str) -> dict:
    return read_data(f'users/{telegram}', telegram)['test_marks']


def get_index(telegram: str):
    return int(read_data(f'users/{telegram}', telegram)['user']['index'])


def get_difficulty(telegram: str):
    return int(read_data(f'users/{telegram}', telegram)['user']['difficulty'])


def get_quantity(telegram: str):
    return int(read_data(f'users/{telegram}', telegram)['user']['quantity'])


def get_tag_or_value(telegram: str):
    return 'marks' if get_test_date(telegram) != get_date() else 'test_marks'