import datetime
import os

import numpy as np
import pillow_heif  # Убедитесь, что установлен pillow-heif
import rawpy
from PIL import Image

# Убедитесь, что pillow-heif правильно интегрируется с Pillow
pillow_heif.register_heif_opener()


def convert_dng_to_heic(dng_file_path, heic_file_path):
    """
    Функция для конвертации DNG файла в HEIC.
    """
    try:
        # Открываем DNG файл с помощью rawpy
        with rawpy.imread(dng_file_path) as raw:
            # Получаем RGB изображение
            rgb_image = raw.postprocess()

        # Конвертируем в PIL изображение
        pil_image = Image.fromarray(rgb_image)

        # Сохраняем изображение в формате HEIC используя PIL и pillow-heif
        pil_image.save(heic_file_path, format="HEIF", quality=90)

        print(f"Конвертирован и сохранен: {heic_file_path}")
        return True
    except Exception as e:
        print(f"Ошибка при конвертации {dng_file_path}: {e}")
        return False


def convert_all_dng_in_folder(folder_path):
    """
    Функция для поиска и конвертации всех DNG файлов в HEIC в заданной папке и ее подкаталогах.
    """
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.dng'):
                print(f"Найден файл {file}")
                dng_file_path = os.path.join(root, file)
                heic_file_path = os.path.splitext(dng_file_path)[0] + '.heic'

                # Конвертируем DNG в HEIC
                print("Конвертируем...")
                convert_result = convert_dng_to_heic(dng_file_path, heic_file_path)

                # Удаляем исходный DNG файл
                if convert_result:
                    os.remove(dng_file_path)
                    print(f"Удален оригинальный файл: {dng_file_path}")
                else:
                    print("Файл не сконвертировался. Поэтому оставляем как есть.")


if __name__ == "__main__":
    print(f"Начали работу в {datetime.datetime.now()}")
    start_date = datetime.datetime.now()
    # Путь к папке, в которой нужно выполнить конвертацию
    photos_folder = os.path.expanduser('/Volumes/AT1/Yandex.Disk.localized/_Inbox')

    # Запуск конвертации
    convert_all_dng_in_folder(photos_folder)
    print(f"Скрипт отработал в {datetime.datetime.now()}")
    print(f"Время работы: {datetime.datetime.now() - start_date} c.")
