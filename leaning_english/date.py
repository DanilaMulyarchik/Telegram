from datetime import datetime


def get_date() -> str:
    """
    Get today date
    :return: date
    """
    current_date = datetime.now()

    formatted_date = current_date.strftime('%Y-%m-%d')

    return formatted_date
