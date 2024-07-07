import os
from datetime import datetime


def check_file_exist():

    current_date = datetime.now().strftime("%d_%m_%Y")

    folder_path = 'C:/Users/USER/Documents/GitHub/Telegram/leaning_english/data'

    for filename in os.listdir(folder_path):
        if filename.startswith(current_date):
            return current_date
        else:
            return None


