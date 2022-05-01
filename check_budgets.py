import pandas as pd
old_dreams = pd.read_csv("df2_19_04.csv")

new_dreams = pd.read_csv("df_2022-04-29.csv")

print(old_dreams.columns)
compare_dict = {}
name_dict = {}
for index, row in old_dreams.iterrows():
    compare_dict[row.link] = [row.minimum_budget - row.preexisting_funding]
    name_dict[row.link] = row['name']
for index, row in new_dreams.iterrows():
    compare_dict.setdefault(row.link, []).append(row.minimum_budget - row.preexisting_funding - 3000)
    name_dict[row.link] = row['name']

for kez, value in compare_dict.items():
    if len(value) != 2:
        print(kez,name_dict.get(kez),  "NOT ENOUGH VALUES")
        continue
    if value[0] != value[1]:
        print(kez, name_dict.get(kez), value)


