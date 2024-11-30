import os
import subprocess
import time

# Исправляем даты.
# Берем дату создания контента (если она есть и проставляем ее)


# Директория с фотографиями
photos_directory = "/Users/andreytorlopov/Downloads/2013P"

# Список форматов фотографий
PHOTOS_EXT = ['.jpg', '.jpeg', '.png', '.tiff', '.bmp', '.gif']

# Функция для получения даты "Content created" с использованием exiftool


def get_content_created_date(file_path):
    try:
        result = subprocess.run(
            ["exiftool", "-DateTimeOriginal", "-s3", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            date_str = result.stdout.strip()
            if date_str:
                return time.mktime(time.strptime(date_str, "%Y:%m:%d %H:%M:%S"))
        print(f"Не удалось получить дату для файла: {file_path}")
        return None
    except Exception as e:
        print(f"Ошибка при обработке файла {file_path}: {e}")
        return None

# Функция для изменения системных дат файла


def change_file_dates(file_path, timestamp):
    try:
        os.utime(file_path, (timestamp, timestamp))
        print(f"Даты изменены для файла: {file_path}")
    except Exception as e:
        print(f"Ошибка изменения дат для файла {file_path}: {e}")

# Основной скрипт


def process_photos(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in PHOTOS_EXT:
                file_path = os.path.join(root, file)
                content_created_timestamp = get_content_created_date(file_path)
                if content_created_timestamp:
                    change_file_dates(file_path, content_created_timestamp)


# Запуск обработки
process_photos(photos_directory)
