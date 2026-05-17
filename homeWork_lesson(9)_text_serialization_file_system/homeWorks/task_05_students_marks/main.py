import os


current_directory = os.getcwd()
students_file_path = os.path.join(current_directory, 'students.txt')

with open(students_file_path, 'r', encoding='utf-8') as file:
    for line in file:
        students = line.split()

        if not students:
            continue

        student_surname, student_name, student_marks = students
        grade = int(student_marks)

        if grade < 3:
            print(f"{student_surname} {student_name} - '{student_marks}'")