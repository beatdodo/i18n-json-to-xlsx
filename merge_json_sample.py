import json

def merge_json_objects(obj1, obj2):
    merged_obj = {}

    for key in obj1:
        if key in obj2:
            if isinstance(obj1[key], dict) and isinstance(obj2[key], dict):
                merged_obj[key] = merge_json_objects(obj1[key], obj2[key])
            else:
                merged_obj[key] = obj2[key]
        else:
            merged_obj[key] = obj1[key]

    for key in obj2:
        if key not in obj1:
            merged_obj[key] = obj2[key]

    return merged_obj

# 讀取 A.json
with open('A.json', 'r', encoding='utf-8') as file_a:
    data_a = json.load(file_a)

# 讀取 B.json
with open('B.json', 'r', encoding='utf-8') as file_b:
    data_b = json.load(file_b)

# 合併兩個 JSON 資料
merged_data = merge_json_objects(data_a, data_b)

# 寫入合併後的資料到新的檔案 merged.json
with open('merged.json', 'w', encoding='utf-8') as merged_file:
    json.dump(merged_data, merged_file, indent=4, ensure_ascii=False)

print('合併完成，已寫入 merged.json')
