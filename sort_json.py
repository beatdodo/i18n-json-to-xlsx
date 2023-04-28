import json
import os

file_prefixes = ['apicodes', 'privileges', 'menu', '']
lang_dirs = ['zh-cn', 'en', 'th-TH']
source_dir = './i18n/'
output_dir = './i18n-sorted/'

# 將 key 攤平成多層嵌套字典
def build_nested_dict(suffix, value, result_dict):
    if '.' in suffix:
        prefix, *keys = suffix.split('.')
    else:
        prefix, keys = suffix, []

    if keys:
        build_nested_dict('.'.join(keys), value, result_dict.setdefault(prefix, {}))
    else:
        result_dict[prefix] = value

# 排序 key 並將 key 攤平
def sort_and_flatten_json(source_json):
    sorted_keys = sorted(source_json.keys())
    result_json = {}

    for key in sorted_keys:
        value = source_json[key]

        if key.count('.') == 0:
            # 如果 key 沒有 '.'，則加上前綴 "Dup"
            result_json[f'Dup{key}'] = value
        else:
            # 如果 key 有 '.'，則將 key 攤平成多層嵌套字典
            build_nested_dict(key, value, result_json)

    return result_json

# 遍歷所有文件夾與檔案，進行處理
for lang in lang_dirs:
    for prefix in file_prefixes:
        if prefix:
            file_name = f"{prefix}-{lang}.json"
        else:
            file_name = f"{lang}.json"
        source_file_path = os.path.join(source_dir, lang, file_name)
        output_file_path = os.path.join(output_dir, lang, file_name)

        # 讀取 JSON 檔案
        with open(source_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 排序 key 並將 key 攤平
        sorted_data = sort_and_flatten_json(data)

        # 將排序後的數據寫入 JSON 文件
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(sorted_data, f, ensure_ascii=False)
