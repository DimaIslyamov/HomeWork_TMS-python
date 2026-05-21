def run_menu(json_path: str, csv_path: str) -> None:
    while True:

        print("1. Конвертировать JSON в CSV")
        print("2. Добавить сотрудника в JSON")
        print("3. Добавить сотрудника в CSV")
        print("4. Найти сотрудника по имени")
        print("5. Фильтр по языку")
        print("6. Средний рост по году рождения")
        print("0. Выход")

        choice = input("Выберите действие: ")

# ////  some choice here = if bla bla bla

        if choice == "0":
            break