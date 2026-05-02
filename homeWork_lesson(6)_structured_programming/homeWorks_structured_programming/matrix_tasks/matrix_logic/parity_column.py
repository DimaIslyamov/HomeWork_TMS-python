def make_even_ones(matrix: list[list[int]]) -> list[list[int]]:
    result = []

    for row in matrix:
        ones_count = row.count(1)

        if ones_count % 2 == 0:
            new_row = row + [0]
        else:
            new_row = row + [1]

        result.append(new_row)

    return result


# matrix_1 = [
#     [1, 0, 1],
#     [1, 1, 1],
#     [0, 0, 1]
# ]
#
# new_matrix = make_even_ones(matrix_1)
#
# for rows in new_matrix:
#     print(*rows)