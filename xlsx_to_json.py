import os
import pandas as pd
import numpy as np

file_prefixes = ['apicodes', 'privileges', 'menu', 'backend', '']
lang_dirs = ['zh-cn', 'en', 'th-TH']
merged_dir = './i18n-translated/merged/'
output_dir = './i18n-merged-xlsx-to-json/'

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
            f.write('{\n')
            for key, value in lang_data.items():
                value = str(value).replace('"', '\\"')  # 將雙引號替換為轉譯字符
                f.write(f'  "{key}": "{value}",\n')
                if pd.isna(value):
                    value = ''
                f.write(f'  "{key}": "{value}",\n')
            f.write('}')
    
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
        f.write('{\n')
        for key, value in lang_data.items():
            value = str(value).replace('"', '\\"')  # 將雙引號替換為轉譯字符
            f.write(f'  "{key}": "{value}",\n')
            if pd.isna(value):
                value = ''
            f.write(f'  "{key}": "{value}",\n')
        f.write('}')
