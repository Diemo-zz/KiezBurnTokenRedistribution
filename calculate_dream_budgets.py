import pickle
from DreamsList import DreamList
from pprintpp import pprint
from operator import attrgetter
with open("dumped_df_with_names.pickle", "rb") as f:
    df = pickle.load(f)

budget = 9000

dreamlist = DreamList.from_dataframe(df)

funded_dreams = dreamlist.calculate_funding(budget)
pprint(dreamlist.fully_funded_dreams)
lines = [f"# Budget: {budget} \n", "\n", f"# Budget allocated: {funded_dreams} \n \n"]

lines.append(f"## Fully Funded \n")
for dream in dreamlist.fully_funded_dreams:
    lines.append(f"[{dream.name}]({dream.link}) ({', '.join(dream.dreamers)}) got fully funded. ({dream.funded}€) \n \n")

lines.append(f"## Partially Funded \n")
for dream in sorted(dreamlist.dreams, key=lambda x: x.funded):
    lines.append(f"[{dream.name}]({dream.link}) ({', '.join(dream.dreamers)}) got partially funded ({dream.funded}€ of "
                 f"{dream.minimum_budget-dream.preexisting_funding} - {dream.maximum_grant_sought}) "
                 f"({dream.funded*100/dream.maximum_grant_sought if dream.maximum_grant_sought else 100:.2f}%"
                 f" of maximum) \n \n")

lines.append(f"## No funding required/Invalid Dreams \n")
for dream in dreamlist.invalid_dreams:
    lines.append(f"[{dream.name}]({dream.link}) - No funding given \n \n")

with open("Results.md", "w", encoding="utf-8") as f:
    f.writelines(lines)




print("FULLY FUNDED")

print("PARTIALLY FUNDED")
for dream in sorted(dreamlist.dreams, key=lambda x: x.funded):
    print(dream.link, dream.funded, " out of ", dream.maximum_grant_sought, " requested.")