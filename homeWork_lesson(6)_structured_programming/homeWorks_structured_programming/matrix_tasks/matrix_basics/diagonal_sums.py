def diagonal_sums(matrix):
    main_sum = 0
    secondary_sum = 0

    n = len(matrix)

    for i in range(n):
        main_sum += matrix[i][i]
        secondary_sum += matrix[i][n - 1 - i]

    return main_sum, secondary_sum


# if len(matrix) != len(matrix[0]):
#     print("Матрица должна быть квадратной")
