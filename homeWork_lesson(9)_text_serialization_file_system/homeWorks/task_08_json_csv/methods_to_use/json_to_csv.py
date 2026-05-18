import pandas as pd


def update_json_to_csv(json_path: str, csv_path: str) -> None:
    try:

        df = pd.read_json(json_path, encoding='utf-8')
        df.to_csv(csv_path, index=False, encoding='utf-8')

    except FileNotFoundError:
        print(f"Файл json не найден {json_path}")

    except Exception as e:
        print(f"Ошибка конвертации {e}")
