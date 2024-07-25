import os


def check_file_exist(directory: str, file: str):
    folder_path = f'C:/Users/USER/Documents/GitHub/Telegram/LearnEnglish/data/{directory}'
    for filename in os.listdir(folder_path):
        if filename.startswith(file):
            return file


def check_dir_exist(directory: str, name: str):
    folder_path = f'C:/Users/USER/Documents/GitHub/Telegram/LearnEnglish/data/{directory}/{name}'
    return True if os.path.isdir(folder_path) else False


def create_dir(path: str, name: str):
    folder_path = f'C:/Users/USER/Documents/GitHub/Telegram/LearnEnglish/data/{path}/{name}'
    try:
        os.makedirs(folder_path)
    except Exception as e:
       pass
