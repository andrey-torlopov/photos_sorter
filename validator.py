import re
from datetime import datetime


def validate_date_in_filename(file, file_info) -> bool:
    year, month, day = extract_date_components_from_filename(file)
    # Проверяем, что компоненты даты из имени файла совпадают с file_info
    if year != str(file_info.year) or month != f"{file_info.month:02}" or day != f"{file_info.day:02}":
        return False
    return True


def extract_date_components_from_filename(filename) -> (str, str, str):
    '''
    Извлекаем компоненты даты из имени файла
    '''
    # Регулярное выражение для извлечения компонентов даты из формата файла
    match = re.match(r"(\d{4})-(\d{2})-(\d{2})", filename)
    if match:
        year, month, day = match.groups()
        # Возвращаем компоненты как строки с добавлением "0", если нужно
        return year, f"{int(month):02}", f"{int(day):02}"
    else:
        raise ValueError("Невозможно извлечь компоненты даты из имени файла")
