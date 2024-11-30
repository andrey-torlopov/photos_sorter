import datetime
import os

import pillow_heif
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
from PIL.ExifTags import TAGS


class FileInfo:
    file_path: str
    is_video: bool
    is_ignore: bool
    ext: str

    def __init__(self, file_path):
        self.file_path = file_path
        self.is_video = False
        self.is_ignore = False
        self.ext = os.path.splitext(file_path)[1].lower()
        self.file_date = None
        self.proccess()

    def set_custom_date(self, file_date: datetime) -> None:
        self.file_date = file_date
        self.year = self.file_date.strftime('%Y')
        self.month = self.file_date.strftime('%m')
        self.day = self.file_date.strftime('%d')
        self.hour = self.file_date.strftime('%H')
        self.minute = self.file_date.strftime('%M')

    def proccess(self):
        if '.DS_Store' in self.file_path:
            self.is_ignore = True
            return
        if self.ext in ['.aae']:
            self.is_ignore = True
            return
        self.is_video = self.ext in ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv']
        self.default_date = self.get_default_date()
        self.process_media_creation_date()

    def process_media_creation_date(self):
        ext = os.path.splitext(self.file_path)[1].lower()

        if ext in ['.heic']:
            creation_date = self.get_heic_creation_date_pillow_heif()
            self.file_date = creation_date

        if ext in ['.jpg', '.jpeg', '.png', '.tiff', '.bmp', '.gif']:
            try:
                with Image.open(self.file_path) as img:
                    exif_data = img._getexif()
                    if exif_data:
                        for tag_id in exif_data:
                            tag = TAGS.get(tag_id, tag_id)
                            data = exif_data.get(tag_id)
                            if tag == 'DateTimeOriginal':
                                self.file_date = datetime.datetime.strptime(data, '%Y:%m:%d %H:%M:%S')
            except Exception as e:
                print(f"{self.file_path}\nError reading image metadata: {e}")

        elif ext in ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv']:
            try:
                parser = createParser(self.file_path)
                if parser:
                    with parser:
                        metadata = extractMetadata(parser)
                        if metadata and 'creation_date' in metadata.exportPlaintext():
                            self.file_date = metadata.get('creation_date')
            except Exception as e:
                print(f"Проблема с видеофайлом: {self.file_path}\n{e}")

        if self.file_date is None:
            self.file_date = self.default_date

        self.year = self.file_date.strftime('%Y')
        self.month = self.file_date.strftime('%m')
        self.day = self.file_date.strftime('%d')
        self.hour = self.file_date.strftime('%H')
        self.minute = self.file_date.strftime('%M')

    def get_heic_creation_date_pillow_heif(self):
        try:
            heif_file = pillow_heif.open_heif(self.file_path)
            exif_data = heif_file.info.get('exif', None)
            if exif_data:
                exif = Image.Exif()
                exif.load(exif_data)
                exif_dict = {Image.ExifTags.TAGS[key]: exif[key] for key in exif if key in Image.ExifTags.TAGS}
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
        except Exception as e:
            print(f"Ошибка при открытии HEIC файла {self.file_path}: {e}")
        return None

    def get_default_date(self) -> datetime:
        stat = os.stat(self.file_path)
        creation_time = datetime.datetime.fromtimestamp(stat.st_birthtime)
        modification_time = datetime.datetime.fromtimestamp(stat.st_mtime)
        system_file_date = datetime.datetime.fromtimestamp(os.path.getctime(self.file_path))
        return self.get_earliest_date([creation_time, modification_time, system_file_date])

    def get_earliest_date(self, dates):
        # Фильтруем None и возвращаем наименьшую дату
        valid_dates = [date for date in dates if date is not None]
        return min(valid_dates) if valid_dates else None
