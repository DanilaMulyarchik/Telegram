from file_finder import check_file_exist
from data_manager import *
import random


def get_random_word_list():
    words = []
    all_words = data_main_read()['words']
    if check_file_exist('data') is None:
        while len(words) < 5:
            random_word = random.choice(all_words)
            if random_word in words:
                continue
            words.append(random_word)

        data_save(words)
    else:
        words = data_read()['words']
    return words
