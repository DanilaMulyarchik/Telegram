from managers.data_manager import save_data


def create_new_user(folder: str, file: str, **kwargs):
    save_data(folder, file, user=kwargs['user'], marks=kwargs['marks'])