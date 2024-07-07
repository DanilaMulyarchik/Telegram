from translate import Translator
from faker import Faker
from file_finder import check_file_exist
from data_manager import *


def get_random_word_list():
    words = []
    if check_file_exist() is None:
        for i in range(5):
            random_word_en = get_generate_words_with_length(5, 10)

            translator = Translator(from_lang='en', to_lang='ru')
            random_word_ru = translator.translate(random_word_en)

            words.append((random_word_en, random_word_ru))
        settings_save(words, False)
    else:
        words = settings_read('words')
    return words


def get_generate_words_with_length(min_length, max_length):
    fake = Faker()
    while True:
        word = fake.word()
        if min_length <= len(word) <= max_length:
            return word
