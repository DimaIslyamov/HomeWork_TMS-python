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
            column_with.append(j)
        else:
            column_without.append(j)

    return column_with, column_without


# ==== Более python вариант но я пока такое не пишу сам ==== =((
# def find_h_in_columns(matrix, h):
#     columns = list(zip(*matrix)) # zip ??
#
#     column_with = [col for col in columns if h in col]
#     column_without = [col for col in columns if h not in col]
#
#     return column_with, column_without