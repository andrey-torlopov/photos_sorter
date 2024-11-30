import os

from file_info import FileInfo


def get_unique_filename0(target_path, filename) -> str:
    base, extension = os.path.splitext(filename)
    counter = 1
    unique_filename = filename
    while os.path.exists(os.path.join(target_path, unique_filename)):
        unique_filename = f"{base}_{counter}{extension}"
        counter += 1
    return unique_filename


def get_unique_filename(file_info: FileInfo, target_path, filename) -> str:
    '''
    Формируем уникальное имя файла. Проверяем если такого файла нет, то добавляем суффикс с индексом.
    Если и такой файл уже существует - увеличиваем индекс пока не найдем подходящее имя.
    Имя файла - это дата в формате YYYY-mm-DD--HH-MM<__1.jpg>
    '''
    _, extension = os.path.splitext(filename)
    base_with_date = f"{file_info.year}-{file_info.month}-{file_info.day}--{file_info.hour}-{file_info.minute}"
    unique_filename = f"{base_with_date}{extension}"
    counter = 1
    while os.path.exists(os.path.join(target_path, unique_filename)):
        unique_filename = f"{base_with_date}__{counter}{extension}"
        counter += 1

    return unique_filename
