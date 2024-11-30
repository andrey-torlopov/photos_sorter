import datetime
import os
import shutil

import pillow_heif
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import ExifTags, Image
from PIL.ExifTags import TAGS

# Определение путей
source_path = '/Volumes/AT1/_tmp/A'
destination_path = '/Volumes/AT1/_tmp/B'


def get_heic_creation_date_pillow_heif(file_path):
    heif_file = pillow_heif.open_heif(file_path)
    exif_data = heif_file.info.get('exif', None)
    if exif_data:
        exif = Image.Exif()
        exif.load(exif_data)
        exif_dict = {Image.ExifTags.TAGS[key]: exif[key] for key in exif if key in Image.ExifTags.TAGS}
        creation_date_str = exif_dict.get('', None)
        # print(f"filename: {file_path}, tags: \n")
        # print(exif_dict)
        # print(exif_dict.get('Created', "???"), exif_dict.get('CreateDate', "???"),
        #       exif_dict.get('DateTimeOriginal', "???"), exif_dict.get('DateTime', "???"))
        creation_date_str = exif_dict.get('DateTime', None)

        if creation_date_str:
            try:
                creation_date_str = creation_date_str.replace(':', '-')
                creation_date = datetime.datetime.strptime(creation_date_str, '%Y-%m-%d %H-%M-%S')
                return creation_date
            except ValueError as e:
                print(f"Ошибка преобразования даты: {e}")
        else:
            print("Дата создания не найдена")
    else:
        print("EXIF данные отсутствуют")
    return None


def get_media_creation_date(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext in ['.heic']:
        return get_heic_creation_date_pillow_heif(file_path)

    if ext in ['.jpg', '.jpeg', '.png', '.tiff', '.bmp', '.gif']:
        try:
            with Image.open(file_path) as img:
                exif_data = img._getexif()
                if exif_data:
                    for tag_id in exif_data:
                        tag = TAGS.get(tag_id, tag_id)
                        data = exif_data.get(tag_id)
                        if tag == 'DateTimeOriginal':
                            return datetime.datetime.strptime(data, '%Y:%m:%d %H:%M:%S')
        except Exception as e:
            print(f"Error reading image metadata: {e}")
    elif ext in ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv']:
        parser = createParser(file_path)
        if parser:
            with parser:
                metadata = extractMetadata(parser)
                if metadata and 'creation_date' in metadata.exportPlaintext():
                    return metadata.get('creation_date')
    return None


def get_unique_filename(target_path, filename):
    base, extension = os.path.splitext(filename)
    counter = 1
    unique_filename = filename
    while os.path.exists(os.path.join(target_path, unique_filename)):
        unique_filename = f"{base}_{counter}{extension}"
        counter += 1
    return unique_filename


def get_creation_time(file_path):
    # Получаем статистическую информацию о файле
    stat = os.stat(file_path)
    # Время создания файла на macOS и некоторых других UNIX-подобных системах
    creation_time = datetime.datetime.fromtimestamp(stat.st_birthtime)
    return creation_time


def move_file(file_path, target_dir, filename):
    # return
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    shutil.move(file_path, os.path.join(target_dir, filename))


for root, dirs, files in os.walk(source_path):
    for file in files:
        if '.DS_Store' in file:
            continue
        file_path = os.path.join(root, file)
        file_creation_time = get_media_creation_date(file_path)
        if file_creation_time is None:
            file_creation_time = get_creation_time(file_path)
        if not isinstance(file_creation_time, datetime.datetime):
            file_creation_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))

        year = file_creation_time.strftime('%Y')
        month = file_creation_time.strftime('%m')
        year_path = os.path.join(destination_path, year)
        month_path = os.path.join(year_path, month)
        unique_file = get_unique_filename(month_path, file)
        # print(f"file: {file_path} date: {file_creation_time}")
        move_file(file_path, month_path, unique_file)

print("Файлы успешно перенесены.")
