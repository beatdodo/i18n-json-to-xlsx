import os
import pandas as pd
import numpy as np
import json

file_prefixes = ['apicodes', 'privileges', 'menu', 'backend', '']
lang_dirs = ['zh-cn', 'en', 'th-TH']

# 翻譯本地的
merged_dir = './i18n-output/merged/'
output_dir = './i18n-merged-xlsx-to-json-local/'

def set_value(obj, keys, value):
    for k in keys[:-1]:
        if k not in obj:
            obj[k] = {}
        elif not isinstance(obj[k], dict):
            if isinstance(obj[k], str):
                obj[f'Dup{k}'] = obj.pop(k)
                obj[k] = {}
            else:
                print('error1', pd.isna(obj[k]))
                raise ValueError(f'Conflict at {k}: value "{obj[k]}" already exists')
        obj = obj[k]
    if keys[-1] in obj:
        raise ValueError(f'Conflict at {keys[-1]}: value "{obj[keys[-1]]}" already exists')
    obj[keys[-1]] = value

for lang in lang_dirs:
    for file_prefix in file_prefixes:
        # 檢查輸出目錄是否存在，如不存在則創建目錄
        lang_dir = f"{output_dir}{lang}/"
        if not os.path.isdir(lang_dir):
            os.makedirs(lang_dir)

        # 讀取輸入檔案
        input_path = f"{merged_dir}{file_prefix}-merged.xlsx"
        if not os.path.isfile(input_path):
            continue
        df = pd.read_excel(input_path)

        # 取出當前語系的數據
        lang_data = df[['Key', lang]].set_index('Key').to_dict()[lang]

        # 將數據寫入輸出檔案
        output_path = f"{lang_dir}{file_prefix}-{lang}.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            obj = {}
            for key, value in lang_data.items():
                # 將 nan 轉成空字串
                value = '' if pd.isna(value) else value

                keys = key.split('.')
                set_value(obj, keys, value)
            f.write(json.dumps(obj, indent=4, ensure_ascii=False))

    # 輸出整合檔案的數據
    input_path = f"{merged_dir}merged.xlsx"
    if not os.path.isfile(input_path):
        continue
    df = pd.read_excel(input_path)

    # 取出當前語系的數據
    lang_data = df[['Key', lang]].set_index('Key').to_dict()[lang]

    # 將數據寫入輸出檔案
    output_path = f"{lang_dir}{lang}.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        obj = {}
        for key, value in lang_data.items():
            # 將 nan 轉成空字串
            value = '' if pd.isna(value) else value

            keys = key.split('.')
            set_value(obj, keys, value)
        f.write(json.dumps(obj, indent=4, ensure_ascii=False))
