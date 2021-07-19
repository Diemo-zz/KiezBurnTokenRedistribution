#I should have committed the original pickle holding the numbers

with open("results.md", "r", encoding="utf8") as f:
    first_lines = f.readlines()

with open("SecondResults.md", "r", encoding="utf8") as f:
    second_lines = f.readlines()

first_lines = list(filter(lambda x: x.startswith("["), first_lines))
second_lines = list(filter(lambda x: x.startswith("["), second_lines))

first_names = [r.split("]")[0] for r in first_lines]
second_names = [r.split("]")[0] for r in second_lines]
print(first_names)
print(second_names)
cancelled_dreams = set(first_names) - set(second_names)
print( cancelled_dreams)

to_delete = []
for line in first_lines:
    if line.split("]")[0] in cancelled_dreams:
        to_delete.append(line)

for element in to_delete:
    first_lines.remove(element)

import re

lines = []
for first, second in zip(sorted(first_lines), sorted(second_lines)):
    if first == second:
        continue
    name = first.split("]")[0].lstrip("[")
    first_brackets = re.findall('\(.*?\)', first)
    second_brackets = re.findall('\(.*?\)', second)
    try:
        first_amount = float(first_brackets[1][1:4].strip().strip("€"))
        second_amount = float(second_brackets[1][1:4].strip().strip("€"))
    except Exception as e:
        first_amount = float(first_brackets[2][1:4].strip().strip("€"))
        second_amount = float(second_brackets[2][1:4].strip().strip("€"))
    lines.append(f"{name}: {second_amount-first_amount} \n")

with open("difference.txt", "w", encoding="utf8") as f:
    f.writelines(lines)
