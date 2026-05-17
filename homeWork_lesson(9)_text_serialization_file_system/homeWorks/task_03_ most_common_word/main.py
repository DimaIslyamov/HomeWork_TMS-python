import os


current_directory = os.getcwd()

input_file_path = os.path.join(current_directory, "input.txt")
output_file_path = os.path.join(current_directory, "output.txt")


with (open(input_file_path, "r", encoding='utf-8') as read_file,
      open(output_file_path, "w", encoding='utf-8') as write_file):

    for line in read_file:

        words = line.strip().split()
        word_count = {}

        for word in words:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1

        most_common_word = max(word_count, key=word_count.get)
        count = word_count[most_common_word]

        write_file.write(f"{most_common_word} - {count}\n")

