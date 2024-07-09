import os
from datetime import datetime


def check_file_exist(dirrectory: str):

    current_date = datetime.now().strftime("%Y-%m-%d")

    folder_path = f'C:/Users/USER/Documents/GitHub/Telegram/leaning_english/{dirrectory}'

    for filename in os.listdir(folder_path):
        if filename.startswith(current_date):
            return current_date