import os
import time
from datetime import datetime


def change_file_dates(file_path: str, date_time: datetime, is_print_log: bool = False) -> None:
    """
    Функция изменения времени в файле. Передаем путь и объект datetime.
    """
    try:
        # Преобразуем datetime в timestamp
        timestamp = time.mktime(date_time.timetuple())

        # Устанавливаем дату изменения и последнего открытия
        os.utime(file_path, (timestamp, timestamp))

        if is_print_log:
            print(f"Даты изменены для файла: {file_path}")
    except Exception as e:
        if is_print_log:
            print(f"Ошибка изменения дат для файла {file_path}: {e}")


def update_dates_in_folder():
    pass
    # Проставляем указаную дату

    # Укажите дату, которую хотите установить
    # desired_date = "01.06.2023"
    # desired_datetime = datetime.strptime(desired_date, "%d.%m.%Y")
    # timestamp = time.mktime(desired_datetime.timetuple())
    # photos_directory = "/Volumes/photo/Поездки/2023"

    # Основной скрипт прогона обновления
    # # Список форматов фотографий
    # PHOTOS_EXT = ['.heic', '.jpg', '.jpeg', '.png', '.tiff', '.bmp', '.gif']

    # def process_photos(directory):
    #     for root, _, files in os.walk(directory):
    #         for file in files:
    #             ext = os.path.splitext(file)[1].lower()
    #             if ext in PHOTOS_EXT:
    #                 file_path = os.path.join(root, file)
    #                 change_file_dates(file_path, timestamp)

    # Укажите директорию с фотографиями


if __name__ == '__main__':
    update_dates_in_folder()
