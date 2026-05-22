import csv
import json
import os

import pandas as pd


def save_employee_to_json(new_employee: dict, json_path: str) -> None:
    if os.path.exists(json_path) and os.path.getsize(json_path) > 0:
        with open(json_path, 'r', encoding='utf-8') as f:

            try:
                data = json.load(f)
                if not isinstance(data, list):
                    data = [data]

            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(new_employee)

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def save_employee_to_csv(new_employee: dict, csv_path: str) -> None:
    file_exists = os.path.exists(csv_path)
    file_is_empty = not file_exists or os.path.getsize(csv_path) == 0

    employee_for_csv = new_employee.copy()
    employee_for_csv["languages"] = ", ".join(new_employee["languages"])

    with open(csv_path, "a", encoding="utf-8", newline="") as csv_file:
        fieldnames = employee_for_csv.keys()

        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        if file_is_empty:
            writer.writeheader()

        writer.writerow(employee_for_csv)


def convert_json_to_csv_data(json_path: str) -> pd.DataFrame | None:
    try:
        return pd.read_json(json_path, encoding='utf-8')
    except FileNotFoundError:
        print(f"Файл json не найден {json_path}")
    except ValueError as error:
        print(f"Ошибка чтения json: {error}")

    return None


def save_data_to_csv(csv_data: pd.DataFrame | None, csv_path: str) -> None:
    if csv_data is None:
        return

    csv_data.to_csv(csv_path, index=False, encoding='utf-8')
    print(f"Данные сохранены в CSV: {csv_path}")


def update_json_to_csv(json_path: str, csv_path: str) -> None:
    csv_data = convert_json_to_csv_data(json_path)
    save_data_to_csv(csv_data, csv_path)
