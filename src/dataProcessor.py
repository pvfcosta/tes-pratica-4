import json
from collections import defaultdict
import pandas as pd
import math

def read_json_file(file_path):

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in file: {file_path}")

def avg_age_country(filePath):

    data = read_json_file(filePath)

    df = pd.DataFrame(data)

    for row in df.to_dict('records'):
        if row['country'] is None or (type(row['country']) is not str and math.isnan(row['country'])):
            raise ValueError('Missing country from ' + row['name'])
        if row['age'] is None or math.isnan(row['age']):
            raise ValueError('Missing age from ' + row['name'])

    avg_age = df.groupby('country').mean()

    return avg_age.to_dict()

def calculate_average_age(filepath):
    data = read_json_file(filepath)

    ages = []

    if isinstance(data, list):
        for obj in data:
            if 'age' in obj:
                ages.append(obj['age'])
            else:
                raise ValueError("Cada objeto na lista deve conter a chave 'age'. Nome: " + obj['name'])
    else:
        raise ValueError("Os dados do arquivo não representam uma lista de objetos.")

    if ages:
        average_age = sum(ages) / len(ages)
        print(average_age)
        return average_age
    else:
        return 0