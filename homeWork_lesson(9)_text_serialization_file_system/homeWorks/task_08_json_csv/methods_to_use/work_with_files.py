import os
import json
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


def update_json_to_csv(json_path: str, csv_path: str) -> None:
    try:

        df = pd.read_json(json_path, encoding='utf-8')
        df.to_csv(csv_path, index=False, encoding='utf-8')

    except FileNotFoundError:
        print(f"Файл json не найден {json_path}")

    except Exception as e:
        print(f"Ошибка конвертации {e}")
