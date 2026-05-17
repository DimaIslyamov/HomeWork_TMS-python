import os
import re


current_directory = os.getcwd()
input_file_path = os.path.join(current_directory, "input.txt")

with open(input_file_path, "r") as read_file:
    text = read_file.read()

    numbers = re.findall(r"\d+", text)
    total = sum(int(number) for number in numbers)

    print(f"Total: {total}")
