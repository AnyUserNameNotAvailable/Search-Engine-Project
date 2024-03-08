import json

json_filename = "data.json"

def delete_data_from_json(json_file):
    with open(json_file, 'w', encoding='utf-8') as file:
        file.write("[]")
    return []

delete_data_from_json(json_filename)