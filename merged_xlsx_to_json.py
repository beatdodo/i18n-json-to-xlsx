import openpyxl
import json
from collections import defaultdict

# 讀取 Excel 檔案
wb = openpyxl.load_workbook('./i18n-output/merged/merged.xlsx')
sheet = wb.active

# 取得所有語系名稱
langs = sheet[1][1:]
lang_codes = [cell.value for cell in langs]

# 取得每一列資料，轉換為字典
translations = defaultdict(dict)
for row in sheet.iter_rows(min_row=2):
    key = row[0].value
    for i, lang_code in enumerate(lang_codes):
        value = row[i + 1].value
        if value is not None and value != '':
            translations[key][lang_code] = value

# 按照 key 轉換成多個 JSON 檔案
for lang_code in lang_codes:
    lang_data = {}
    for key, value in translations.items():
        keys = key.split('.')
        node = lang_data
        for i, k in enumerate(keys):
            if i == len(keys) - 1:
                node[k] = value[lang_code]
            else:
                node = node.setdefault(k, {})
    with open(lang_code + '.json', 'w', encoding='utf-8') as f:
        json.dump(lang_data, f, ensure_ascii=False, indent=4)
