import json
import pandas as pd
import os

### 
# 此頁功能為將 .json 的 key 攤平後整理為 .xlsx

def json_to_excel(data, prefix="", result=None):
    if result is None:
        result = []
    for key, value in data.items():
        if isinstance(value, dict):
            json_to_excel(value, prefix + key + ".", result)
        else:
            result.append((prefix + key, value))
    return result

# 檔案前綴
file_prefixes = ['apicodes', 'privileges', 'menu', 'backend', '']
# 語系
lang_dirs = ['zh-cn', 'en', 'th-TH']

for lang in lang_dirs:
    for file_prefix in file_prefixes:
        # 有 file_prefix 需加上 -
        file_name = f"{'{}-'.format(file_prefix) if file_prefix else ''}"
        json_file_path = f"./i18n/{lang}/{file_name}{lang}.json"

        # 檢查檔案是否存在
        if os.path.isfile(json_file_path):
            # 讀取 JSON 檔案
            with open(json_file_path) as f:
                data = json.load(f)

            # 將 JSON 轉換成 DataFrame
            result = json_to_excel(data)

            df = pd.DataFrame(result, columns=["Key", "Value"])

            # 根據 Key 進行排序
            df_sorted = df.sort_values("Key")

            # 指定匯出的 .xlsx 檔案的路徑
            output_path = f"./i18n-output/{lang}/{file_name}{lang}.xlsx"

            # 將 DataFrame 寫入 Excel 檔案
            with pd.ExcelWriter(output_path) as writer:
                df_sorted.to_excel(writer, index=False)
        else:
            print(f"{json_file_path} not found")
