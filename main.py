import os
import shutil
import time
from datetime import datetime

import pillow_heif
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
from PIL.ExifTags import TAGS

from file_info import FileInfo
from fix_photo_date import change_file_dates
from unique_file_name import get_unique_filename
from validator import validate_date_in_filename

# source_path = '/Volumes/photo/Photos/2014'
# destination_path = source_path  # '/Volumes/AT/_OUTBOX'

is_use_custom_date = False
custom_date = '20.08.2024'
is_sort_photos = False
is_force_update_date_metadata = False


def move_file(file_path, target_dir, filename):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    shutil.move(file_path, os.path.join(target_dir, filename))


# folders_list = [f'/Volumes/photo/Photos/{x}' for x in range(2020, 2025)]
folders_list = ['/Volumes/photo/Photos/2020/08']
source_paths = folders_list
target_paths = folders_list


def process_files() -> None:
    for i in range(len(source_paths)):
        print(f'Начали обработку папки: {source_paths[i]}')
        process_files_in_folder(source_paths[i], target_paths[i])
        print(f'Закончили обработку папки: {source_paths[i]}\n')


def process_files_in_folder(source: str, target: str) -> None:
    print(f"Начали работу в {datetime.now()}")
    start_date = datetime.now()
    elements_count = 0
    for root, dirs, files in os.walk(source):
        for file in files:
            file_path = os.path.join(root, file)

            file_info = FileInfo(file_path=file_path)
            if file_info.is_ignore:
                continue
            elements_count += 1
            # Принудительно меняем дату
            if is_use_custom_date:
                desired_datetime = datetime.strptime(custom_date, "%d.%m.%Y")
                timestamp = time.mktime(desired_datetime.timetuple())
                file_info.set_custom_date(desired_datetime)
                os.utime(file_path, (timestamp, timestamp))  # Обновление времени доступа и изменения

            if is_sort_photos:
                if file_info.is_video:
                    path_to_move = os.path.join(target, "Videos")
                else:
                    path_to_move = os.path.join(target, "Photos")

                year_path = os.path.join(path_to_move, file_info.year)
                target_folder = os.path.join(year_path, file_info.month)
            else:
                # Сохраняем оригинальную структуру папок относительно source_path
                relative_path = os.path.relpath(root, source)
                if relative_path == ".":
                    relative_path = ""  # Убираем точку для корневой папки

                target_folder = os.path.join(target, relative_path)

                # Убедимся, что папка назначения существует
                os.makedirs(target_folder, exist_ok=True)

            # Генерируем уникальное имя файла
            unique_file = get_unique_filename(file_info, target_folder, file)

            # Обновляем дату файла перед перемещением
            if is_force_update_date_metadata:
                change_file_dates(file_path, file_info.file_date)

            # target_path = os.path.join(target_folder, unique_file)
            # print(f"{file_path}, date: {file_info.file_date}: target_path: {target_path}")

            if not validate_date_in_filename(file, file_info):
                print(f'🔴 Файл: {file_path} различается дата имя файла')

            # Перемещаем файл с новым уникальным именем
            # move_file(file_path, target_folder, unique_file)

    print(f"Завершили работу в {datetime.now()}, общее время: {datetime.now() - start_date}. Обработали: {elements_count} элементов")


if __name__ == '__main__':
    process_files()
