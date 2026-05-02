from matrix_basics.matrix_generator import generate_matrix
from matrix_basics.min_max_indexes import find_min_max_values
from matrix_basics.column_percentages import analyze_matrix
from matrix_basics.diagonal_sums import diagonal_sums

from matrix_operations.multiply_by_k_column import multiply_by_k_column
from matrix_operations.sum_width_L_row import sum_with_l_row
from matrix_operations.search_value_columns import find_h_in_columns

from matrix_logic.parity_column import make_even_ones


def menu():
    print("\nВыберите задачу:")
    print("1 - Генерация матрицы")
    print("2 - Min / Max")
    print("3 - Проценты по столбцам")
    print("4 - Диагонали")
    print("5 - Умножение на K-столбец")
    print("6 - Сумма с L-строкой")
    print("7 - Поиск значения в столбцах")
    print("8 - Чётность единиц (0/1)")
    print("0 - Выход")


def main():
    while True:
        menu()
        choice = input("Ваш выбор: ")

        if choice == "0":
            print("Выход...")
            break

        elif choice == "1":
            m = int(input("Строки: "))
            n = int(input("Столбцы: "))
            matrix = generate_matrix(m, n)

            for row in matrix:
                print(*row)

        elif choice == "2":
            m = int(input("Строки: "))
            n = int(input("Столбцы: "))
            matrix = generate_matrix(m, n)

            min_val, min_pos, max_val, max_pos = find_min_max_values(matrix)

            print("Матрица:")
            for row in matrix:
                print(*row)

            print(f"Min: {min_val} {min_pos}")
            print(f"Max: {max_val} {max_pos}")

        elif choice == "3":
            m = int(input("Строки: "))
            n = int(input("Столбцы: "))
            matrix = generate_matrix(m, n)

            total, col_sums, percents = analyze_matrix(matrix)

            for row in matrix:
                print(*row)

            print("Сумма:", total)
            print("Суммы столбцов:", col_sums)
            print("Проценты:", percents)

        elif choice == "4":
            n = int(input("Размер (NxN): "))
            matrix = generate_matrix(n, n)

            main_d, sec_d = diagonal_sums(matrix)

            for row in matrix:
                print(*row)

            print("Главная:", main_d)
            print("Побочная:", sec_d)

        elif choice == "5":
            m = int(input("Строки: "))
            n = int(input("Столбцы: "))
            k = int(input("K (индекс столбца): "))

            matrix = generate_matrix(m, n)
            result = multiply_by_k_column(matrix, k)

            print("Исходная:")
            for row in matrix:
                print(*row)

            print("Результат:")
            for row in result:
                print(*row)

        elif choice == "6":
            m = int(input("Строки: "))
            n = int(input("Столбцы: "))
            l = int(input("L (индекс строки): "))

            matrix = generate_matrix(m, n)
            result = sum_with_l_row(matrix, l)

            print("Исходная:")
            for row in matrix:
                print(*row)

            print("Результат:")
            for row in result:
                print(*row)

        elif choice == "7":
            m = int(input("Строки: "))
            n = int(input("Столбцы: "))
            h = int(input("Число H: "))

            matrix = generate_matrix(m, n)
            with_h, without_h = find_h_in_columns(matrix, h)

            for row in matrix:
                print(*row)

            print("Есть:", with_h)
            print("Нет:", without_h)

        elif choice == "8":
            m = int(input("Строки: "))
            n = int(input("Столбцы: "))

            # генерим только 0/1
            import random
            matrix = [[random.randint(0, 1) for _ in range(n)] for _ in range(m)]

            result = make_even_ones(matrix)

            print("Исходная:")
            for row in matrix:
                print(*row)

            print("Результат:")
            for row in result:
                print(*row)

        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()
