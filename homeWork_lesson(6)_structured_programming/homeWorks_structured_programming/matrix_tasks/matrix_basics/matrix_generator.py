from random import randint


def generate_matrix(rows: int, cols: int) -> list:
    gen_matrix = []

    for i in range(rows):
        gen_row = []
        for j in range(cols):
            gen_row.append(randint(0, 100))
        gen_matrix.append(gen_row)

    return gen_matrix


# m = int(input("Введите количество строк: "))
# n = int(input("Введите количество столбцов: "))
#
# matrix = generate_matrix(rows=m, cols=n)
#
# for row in matrix:
#     print(*row)
