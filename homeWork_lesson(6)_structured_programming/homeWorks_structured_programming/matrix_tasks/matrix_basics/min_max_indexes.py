from homeWorks_structured_programming.matrix_tasks.matrix_basics.matrix_generator import generate_matrix


def find_min_max_values(matrix):
    min_value = matrix[0][0]
    max_value = matrix[0][0]

    min_position = (0, 0)
    max_position = (0, 0)

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            value = matrix[i][j]

            if value < min_value:
                min_value = value
                min_position = (i, j)

            if value > max_value:
                max_value = value
                max_position = (i, j)

    return min_value, min_position, max_value, max_position


# m = int(input("Введите количество строк: "))
# n = int(input("Введите количество столбцов: "))
#
# matrix = generate_matrix(rows=m, cols=n)
#
# for row in matrix:
#     print(row)
#
# min_value, min_position, max_value, max_position = find_min_max_values(matrix)
#
# print(f"Минимальное значение: {min_value} на позиции {min_position}")
# print(f"Максимальное значение: {max_value} на позиции {max_position}")