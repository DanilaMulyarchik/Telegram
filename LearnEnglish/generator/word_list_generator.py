from file_processing.exist_file import check_file_exist
from managers.data_manager import *
import random
from managers.time_manager import get_date


def get_word_list(coll: int, difficulty: int):
    words = []
    all_words = read_data('words/levels', str(difficulty) + '-level')['words']
    if check_file_exist('words', get_date()) is None:
        while len(words) < coll:
            random_word = random.choice(all_words)
            if random_word in words:
                continue
            words.append(random_word)

        save_data('words', get_date(), words=words)
    else:
        words = read_data('words', get_date())['words']
    return words