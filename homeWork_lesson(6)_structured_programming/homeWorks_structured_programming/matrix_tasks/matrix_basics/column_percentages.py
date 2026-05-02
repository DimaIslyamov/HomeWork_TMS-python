from homeWorks_structured_programming.matrix_tasks.matrix_basics.matrix_generator import generate_matrix

def analyze_matrix(matrix):
    total_sum: int = 0
    column_sums = [0] * len(matrix[0])
    percentages = []

    # подсчет суммы всех элементов
    for row in matrix:
        for value in row:
            total_sum += value

    # сумма столбцов
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            column_sums[j] += matrix[i][j]

    # проценты этих столбцов
    for col_sum in column_sums:
        percent = round((col_sum / total_sum) * 100, 2)
        percentages.append(percent)

    return total_sum, column_sums, percentages


# m = int(input("Введите количество строк: "))
# n = int(input("Введите количество столбцов: "))
#
# matrix = generate_matrix(rows=m, cols=n)
#
# total_sum, column_sums, percentages = analyze_matrix(matrix)
#
# print(total_sum)
# print(*column_sums)
# print(*percentages)

