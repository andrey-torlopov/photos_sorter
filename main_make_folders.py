def proccess_with_make_folders():
    print(f"Начали работу в {datetime.now()}")
    start_date = datetime.now()
    for root, dirs, files in os.walk(source_path):
        for file in files:
            file_path = os.path.join(root, file)

            file_info = FileInfo(file_path=file_path)
            if file_info.is_ignore:
                continue

            if file_info.is_video:
                path_to_move = os.path.join(destination_path, "Videos")
            else:
                path_to_move = os.path.join(destination_path, "Photos")

            year_path = os.path.join(path_to_move, file_info.year)
            target_path = os.path.join(year_path, file_info.month)
            unique_file = get_unique_filename(file_info, target_path, file)

            # Перед перемещением обновляем дату
            # # Принудительно меняем дату
            # desired_date = "25.09.2020"
            # desired_datetime = datetime.strptime(desired_date, "%d.%m.%Y")
            # timestamp = time.mktime(desired_datetime.timetuple())

            # file_info.file_date = timestamp
            #
            change_file_dates(file_path, file_info.file_date)
            print(f"{file_path}, date: {file_info.file_date}: target_path: {target_path}/{unique_file}")
            # move_file(file_path, target_path, unique_file)

    print(f"Скрипт отработал в {datetime.now()}")
    print(f"Время работы: {datetime.now() - start_date} c.")
