import os

from homeWorks.task_07_caesar_cipher.cezar_chiper import (
    cezar_cipher,
    Mode,
    Language)


current_directory = os.getcwd()

input_file_path = os.path.join(current_directory, "input.txt")
encrypted_file_path = os.path.join(current_directory, "encrypted.txt")


with open(input_file_path, "r", encoding='utf-8') as read_file:
    lines = read_file.readlines()


encrypted_lines = []

for line_number, line in enumerate(lines, start=1):
    encrypted_line = cezar_cipher(
        text=line,
        shift=line_number,
        mode=Mode.ENCRYPT,
        language=Language.EN
    )

    encrypted_lines.append(encrypted_line)

with open(encrypted_file_path, "w", encoding='utf-8') as write_file:
    write_file.writelines(encrypted_lines)