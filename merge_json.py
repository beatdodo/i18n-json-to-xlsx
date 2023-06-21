import os
import json

file_prefixes = ['apicodes', 'privileges', 'menu', 'backend', '']
lang_dirs = ['zh-cn', 'en', 'th-TH']

file_path_local = './i18n-merged-xlsx-to-json-local/'
file_path_market = './i18n-merged-xlsx-to-json/'
output_dir = './i18n-merged-json/'

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

for lang in lang_dirs:
    for file_prefix in file_prefixes:
        # 檢查輸出目錄是否存在，如不存在則創建目錄
        lang_dir = f"{output_dir}{lang}/"
        if not os.path.isdir(lang_dir):
            os.makedirs(lang_dir)

        # 有 file_prefix 需加上 -
        file_name = f"{'{}-'.format(file_prefix) if file_prefix else ''}"

        # 讀取輸入檔案(本地)
        local_input_path = f"{file_path_local}{lang}/{file_name}{lang}.json"
        if not os.path.isfile(local_input_path):
            continue
        with open(local_input_path, 'r', encoding='utf-8') as file_a: 
            data_a = json.load(file_a)

        # 讀取輸入檔案(市場)
        market_input_path = f"{file_path_market}{lang}/{file_name}{lang}.json"
        if not os.path.isfile(market_input_path):
            continue
        with open(market_input_path, 'r', encoding='utf-8') as file_b: 
            data_b = json.load(file_b)
        
        # 合併兩個 JSON 資料
        merged_data = merge_json_objects(data_a, data_b)

        # 按照字母順序排序合併後的資料
        sorted_merged_data = {key: merged_data[key] for key in sorted(merged_data)}

        # 檔案輸出路徑
        output_path = f"{output_dir}{lang}/{file_name}{lang}.json"

        # 寫入合併並排序後的資料到新的檔案 merged.json
        with open(output_path, 'w', encoding='utf-8') as merged_file:
            json.dump(sorted_merged_data, merged_file, indent=4, ensure_ascii=False)
