def sum_with_l_row(matrix, l):
    result = []

    for i in range(len(matrix)):
        row = []

        for j in range(len(matrix[i])):
            value = matrix[i][j] + matrix[i][l]
            row.append(value)

        result.append(row)

    return result


# добавление проверки если пользователь ввел больше l = 10
# if l >= len(matrix):
#     print("Неверный индекс строки")