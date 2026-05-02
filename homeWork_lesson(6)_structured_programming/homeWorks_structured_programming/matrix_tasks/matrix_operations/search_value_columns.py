def find_h_in_columns(matrix, h):
    column_with = []
    column_without = []

    for j in range(len(matrix[0])):
        found_flag = False

        for i in range(len(matrix)):
            if matrix[i][j] == h:
                found_flag = True
                break

        if found_flag:
            column_with.append(matrix[j])
        else:
            column_without.append(matrix[j])

    return column_with, column_without
