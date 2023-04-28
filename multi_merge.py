import pandas as pd
import os

# 指定檔案路徑
folder_path = './data'
merged_file_path = os.path.join(folder_path, 'merged.xlsx')

# 讀取合併檔案
try:
    merged = pd.read_excel(merged_file_path)
except FileNotFoundError:
    print(f"{merged_file_path} not found")
    exit()

# 取得所有欄位名稱，去除 'Key' 欄位
columns = list(merged.columns)[1:]

# 設定儲存輸出檔案的資料夾路徑
output_folder_path = './output'
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# 取得資料夾下所有檔案路徑
file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

# 迭代所有檔案，合併資料
for i, file_path in enumerate(file_paths):
    # 跳過已經合併過的檔案
    if i == 0:
        continue

    try:
        # 讀取欲合併的檔案
        file = pd.read_excel(file_path)

        # 將資料與 merged 合併
        merged = pd.merge(merged, file, on='Key', how='outer')

        # 將合併後的資料，選取指定的欄位並重新排序
        merged = merged[['Key'] + columns]

        # 將空值取代為空字串
        merged = merged.fillna('')

    except FileNotFoundError:
        print(f"{file_path} not found")
        continue

# 輸出合併後的資料到新的 Excel 檔案
output_file_path = os.path.join(output_folder_path, 'output.xlsx')
merged.to_excel(output_file_path, index=False)
print(f"Output file saved at {output_file_path}")