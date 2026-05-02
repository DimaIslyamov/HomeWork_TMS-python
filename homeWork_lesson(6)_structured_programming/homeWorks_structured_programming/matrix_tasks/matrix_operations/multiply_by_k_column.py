def multiply_by_k_column(matrix, k):
    result = []

    for i in range(len(matrix)):
        row = []

        for j in range(len(matrix[i])):
            value = matrix[i][j] * matrix[i][k]
            row.append(value)

        result.append(row)

    return result


# добавление проверки если пользователь ввел больше k = 10
# if k >= len(matrix[0]):
#     print("Неверный индекс столбца")
