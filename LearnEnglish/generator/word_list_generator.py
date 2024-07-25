from os_processing.exist_file import check_file_exist
from managers.data_manager import *
import random
from get_data.get_data import *
import itertools
import config.config


def get_word_list(telegram: str):
    words = []
    all_words = read_data('words', str(get_difficulty(telegram)) + '-level')['words']
    if check_file_exist(f'users/{telegram}/words/{get_difficulty(telegram)}-level', get_date()) is None:
        while len(words) < get_quantity(telegram):
            random_word = random.choice(all_words)
            if random_word not in words:
                words.append(random_word)
        save_data(f'users/{telegram}/words/{get_difficulty(telegram)}-level', get_date(), words=words)
    else:
        words = read_data(f'users/{telegram}/words/{get_difficulty(telegram)}-level', get_date())['words']
    return words


def get_test_word_list(telegram: str):
    all_words = list()
    if check_file_exist(f'users/{telegram}/words/{get_difficulty(telegram)}-level', get_date()) is None:
        all_marks = list(get_all_mark(telegram).keys())[-(config.config.day):]
        for date in all_marks:
            all_words.append(read_data(f'users/{telegram}/words/{get_difficulty(telegram)}-level', date)['words'])
        all_words = list(itertools.chain.from_iterable(all_words))
        test_words = list()
        while len(test_words) < len(all_words) // 2:
            random_word = random.choice(all_words)
            if random_word not in test_words:
                test_words.append(random_word)
        save_data(f'users/{telegram}/words/{get_difficulty(telegram)}-level', str(get_date()), words=test_words)
    else:
        all_words = read_data(f'users/{telegram}/words/{get_difficulty(telegram)}-level', str(get_date()))
    return all_words


def update_word_list(telegram: str):
    old_word_list = get_word_list(telegram)
    if len(old_word_list) < get_quantity(telegram):
        all_words = read_data('words', str(get_difficulty(telegram)) + '-level')['words']
        while len(old_word_list) < get_quantity(telegram):
            random_word = random.choice(all_words)
            if random_word not in old_word_list:
                old_word_list.append(random_word)
    else:
        while len(old_word_list) > get_quantity(telegram):
            old_word_list.pop(-1)
    save_data(f'users/{telegram}/words/{get_difficulty(telegram)}-level', get_date(), words=old_word_list)


