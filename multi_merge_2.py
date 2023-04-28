import pandas as pd
import os

# 檔案前綴
file_prefix = 'privileges'

# 有 file_prefix 需加上 -
file_name = f"{'{}-'.format(file_prefix) if file_prefix else ''}"

# 語系
lang_dirs = ['zh-cn', 'en', 'th-TH']

# 讀取 Excel 檔案
dfs = []
for lang_dir in lang_dirs:
    file_path = f"./i18n-output/{lang_dir}/{file_name}{lang_dir}.xlsx"
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        df = df.rename(columns={"Value": lang_dir})
        dfs.append(df)

# 合併所有 Excel 檔案
merged = dfs[0]
for i in range(1, len(dfs)):
    merged = pd.merge(merged, dfs[i], on='Key', how='outer')

# 根據 lang_dirs 的順序重新排序 column
columns = ["Key"]
for lang_dir in lang_dirs:
    columns.append(lang_dir)
merged = merged[columns]

# 指定匯出的 .xlsx 檔案的路徑
output_path = f"./i18n-output/merged/{file_name}merged.xlsx"

merged.to_excel(output_path, index=False, na_rep='')
