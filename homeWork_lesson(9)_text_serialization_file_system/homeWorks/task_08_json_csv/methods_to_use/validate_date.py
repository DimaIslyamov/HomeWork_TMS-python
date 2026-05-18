from datetime import datetime


def get_validated_date(prompt: str) -> str:
    while True:
        date_str = input(prompt).strip()

        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return date_str

        except ValueError:
            print("Неверный формат даты!")
