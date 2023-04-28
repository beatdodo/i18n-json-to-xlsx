import pandas as pd

# 檔案前綴
file_prefix = 'apicodes'

# 有 file_prefix 需加上 -
file_name = f"{'{}-'.format(file_prefix) if file_prefix else ''}"

file1 = pd.read_excel(f'./i18n-output/zh-cn/{file_name}zh-cn.xlsx')
file2 = pd.read_excel(f'./i18n-output/en/{file_name}en.xlsx')

merged = pd.merge(file1, file2, on='Key', how='outer')

# Rename the value columns from the second Excel file
merged.rename(columns={'Value_x': 'zh-cn', 'Value_y': 'en'}, inplace=True)
# merged = merged[['Key', merged.columns[1], merged.columns[2]]]

# 指定匯出的 .xlsx 檔案的路徑
output_path = f'./i18n-output/merged/{file_name}merged.xlsx'

merged.to_excel(output_path, index=False, na_rep='')
