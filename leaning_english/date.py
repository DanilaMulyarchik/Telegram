from datetime import datetime


def get_date() -> str:
    """
    Get today date
    :return: date
    """
    current_date = datetime.now()

    formatted_date = current_date.strftime('%d_%m_%Y')

    return formatted_date
