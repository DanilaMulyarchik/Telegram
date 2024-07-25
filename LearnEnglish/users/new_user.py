from managers.data_manager import save_data
from os_processing.exist_file import *


def create_new_user(telegram: str, **kwargs):
    create_dir('users', telegram)
    create_dir(f'users/{telegram}', 'words')
    create_dir(f'users/{telegram}/words', '1-level')
    create_dir(f'users/{telegram}/words', '2-level')
    save_data(f'users/{telegram}', telegram, user=kwargs['user'], marks=kwargs['marks'], test_marks=kwargs['test_marks'])