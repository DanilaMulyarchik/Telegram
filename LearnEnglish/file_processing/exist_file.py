import os
from datetime import datetime


def check_file_exist(directory: str, file: str):
    folder_path = f'C:/Users/USER/Documents/GitHub/Telegram/LearnEnglish/data/{directory}'
    for filename in os.listdir(folder_path):
        if filename.startswith(file):
            return file