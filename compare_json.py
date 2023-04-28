import json

with open('local.json', 'r') as f:
    local_data = json.load(f)

with open('market.json', 'r') as f:
    market_data = json.load(f)

merged_data = {}
diff_data = {}

# 檢查 local_data 的每個 key 是否存在於 market_data 中
# 若存在，檢查 value 是否相同
# 若不同，以 market_data 的 value 更新 merged_data
# 並將 local_data 的 key value 寫入 diff_data
for key, value in local_data.items():
    if key not in market_data:
        diff_data[key] = value
    elif market_data[key] != value:
        merged_data[key] = market_data[key]
        diff_data[key] = value
    else:
        merged_data[key] = value

# 將 local_data 中不存在於 market_data 的 key value 寫入 merged_data
for key, value in local_data.items():
    if key not in market_data:
        merged_data[key] = value

with open('merged.json', 'w') as f:
    json.dump(merged_data, f, indent=4, ensure_ascii=False)

with open('diff.json', 'w') as f:
    json.dump(diff_data, f, indent=4, ensure_ascii=False)