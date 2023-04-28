import pandas as pd
import os

# 檔案前綴
file_prefixes = ['apicodes', 'privileges', 'menu', 'backend', '']

# lang 資料夾列表
lang_dirs = ['zh-cn', 'en', 'th-TH']

for file_prefix in file_prefixes:
    if file_prefix:
        # 有 file_prefix 需加上 -
        file_name = '{}-'.format(file_prefix)
    else:
        file_name = ''

    dfs = []

    for lang_dir in lang_dirs:
        try:
            file_path = f'./i18n-output/{lang_dir}/{file_name}{lang_dir}.xlsx'
            df = pd.read_excel(file_path)
            df = df.rename(columns={'Value': lang_dir})
            dfs.append(df)
        except:
            pass

    # Merge all dataframes based on the 'Key' column
    merged = pd.concat(dfs).groupby('Key').first().reset_index()

    # Specify the order of columns based on lang_dirs
    columns = ['Key'] + lang_dirs
    merged = merged[columns]

    # Output the merged file
    output_path = f'./i18n-output/merged/{file_name}merged.xlsx'
    merged.to_excel(output_path, index=False, na_rep='')

# Merge all files
# dfs = []
# for file_prefix in file_prefixes:
#     file_path = f'./i18n-output/merged/{file_prefix}merged.xlsx'
#     if os.path.isfile(file_path):
#         df = pd.read_excel(file_path)
#         dfs.append(df)

# if len(dfs) > 0:
#     merged_all = pd.concat(dfs).groupby('Key').first().reset_index()

#     # Specify the order of columns based on lang_dirs
#     columns = ['Key'] + lang_dirs
#     merged_all = merged_all[columns]

#     # Output the merged file
#     output_path = './i18n-output/merged/merged.xlsx'
#     merged_all.to_excel(output_path, index=False, na_rep='')
