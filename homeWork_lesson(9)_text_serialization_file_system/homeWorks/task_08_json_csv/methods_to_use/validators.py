from datetime import datetime


def get_validated_date(prompt: str) -> str | None:
    while True:
        date_str = input(prompt).strip()

        if date_str == '0':
            return None

        try:
            datetime.strptime(date_str, '%d.%m.%Y')
            return date_str

        except ValueError:
            print("Неверный формат даты!")


def get_validated_full_name(prompt: str) -> str | None:
    while True:

        full_name = input(prompt).strip()

        if full_name == '0':
            return None

        parts = full_name.split()

        if len(parts) != 2:
            print("Введите имя и фамилию через пробел.")
            continue

        first_name, last_name = parts

        if not first_name.isalpha() or not last_name.isalpha():
            print("Имя и фамилия должны содержать только буквы.")
            continue

        return f"{first_name.title()} {last_name.title()}"
