import os
import platform


# ==== Вывести имя вашей os ====
os_name = platform.system()
print(f"Operation system: {os_name}")


# ==== Вывести путь до папки, в которой вы находитесь ====
current_folder = os.getcwd()
print(f"Current folder is: {current_folder}")


# ==== Рассортировать файлы по расширениям ====
source_path = os.path.join(current_folder, 'source_files')
sorted_files = os.path.join(current_folder, 'sorted_files')

stats: dict = {}

for file_name in os.listdir(source_path):
    old_files_path = os.path.join(source_path, file_name)

    if os.path.isfile(old_files_path):
        name, extension = os.path.splitext(file_name)

        if extension:
            extension_folder_name = extension[1:]
        else:
            extension_folder_name = "no_extension"

        file_size = os.path.getsize(old_files_path)

        extension_folder_path = os.path.join(sorted_files, extension_folder_name)
        os.makedirs(extension_folder_path, exist_ok=True)

        mew_file_path = os.path.join(extension_folder_path, file_name)
        os.replace(old_files_path, mew_file_path)

        if extension_folder_name not in stats:
            stats[extension_folder_name] = {
                'count': 0,
                'size': 0,
            }

        stats[extension_folder_name]['count'] += 1
        stats[extension_folder_name]['size'] += file_size


# ==== Сообщение после рассортировки ====
for extension_folder_name, info in stats.items():
    print(f"Moved {info['count']} to folders: {extension_folder_name}, "
          f"total size of this files is: {info['size']}")


# ==== Переименование файла ====
csv_folder = os.path.join(sorted_files, "csv")

for file_name in os.listdir(csv_folder):
    old_files_path = os.path.join(csv_folder, file_name)

    if os.path.isfile(old_files_path):
        new_file_name = "new_" + file_name
        new_file_path = os.path.join(csv_folder, new_file_name)

        os.rename(old_files_path, new_file_path)

        print(f"File {file_name} was renamed to {new_file_name}")
        break
