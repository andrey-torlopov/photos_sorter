import os

# Путь к директории с фотографиями
directory_path = "/Volumes/AT1/Yandex.Disk.localized/_Outbox/Photos/2024/09"

# Получаем список всех файлов в директории
files = os.listdir(directory_path)

# Проходимся по всем файлам
for file in files:
    # Проверяем, содержит ли файл суффикс "_1" перед расширением
    if file.endswith("_1.jpg") or file.endswith("_1.jpeg") or file.endswith("_1.png"):
        # Получаем имя файла и расширение
        filename, extension = os.path.splitext(file)

        # Убираем суффикс "_1" из имени файла
        original_filename = filename[:-2] + extension

        # Полные пути к файлам
        file_path = os.path.join(directory_path, file)
        original_file_path = os.path.join(directory_path, original_filename)

        # Проверяем, существует ли файл без суффикса "_1" с тем же расширением
        if os.path.exists(original_file_path):
            # Удаляем дубликат
            os.remove(file_path)
            print(f"Удален дубликат: {file_path}")
        else:
            print(f"Оригинальный файл не найден для: {file_path}")
