import os
import re

current_folder = os.getcwd()

text_file_name = input("Введите название файла: ")

text_file_path = os.path.join(current_folder, text_file_name)
stop_words_path = os.path.join(current_folder, "stop_words.txt")
result_path = os.path.join(current_folder, "result.txt")

with open(stop_words_path, "r", encoding="utf-8") as file:
    stop_words = file.read().split()

with open(text_file_path, "r", encoding="utf-8") as file:
    text = file.read()

for word in stop_words:
    pattern = re.compile(re.escape(word), re.IGNORECASE)
    text = pattern.sub("*" * len(word), text)

with open(result_path, "w", encoding="utf-8") as file:
    file.write(text)

print(text)