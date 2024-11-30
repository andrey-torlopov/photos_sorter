import re
from datetime import datetime


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


# Пример использования
# filename = "2008-01-30--15-04__1.txt"
# try:
#     extracted_date = extract_date_from_filename(filename)
#     print("Извлеченная дата:", extracted_date)
# except ValueError as e:
#     print(e)
