import json
import os

def save_json(data, filepath):

    """
    Save python into json file

    """

    os.makedirs(os.path.dirname(filepath), exist_ok = True)

    with open(filepath, "w", encoding = "utf-8") as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"Saved data to {filepath}")

def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)