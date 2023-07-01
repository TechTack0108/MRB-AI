import json


def load_data_json(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return (data)


def save_data_json(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_data_txt(file):
    with open(file, "r", encoding="utf-8") as f:
        data = f.read()
    return (data)
