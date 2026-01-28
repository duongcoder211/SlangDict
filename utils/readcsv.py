import csv

def read_csv(path) -> list[dict[str,str]]:
    data = []
    with open(path, mode='r', newline='', encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=";")
        for row in list(reader)[1:]:
            data.append({"slang": row[0], "mean": row[1].replace('\\\"', '"')})
    return data
