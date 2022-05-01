import pickle
from DreamsList import DreamList
import pandas as pd
from operator import attrgetter
from scrape_budget3 import get_dream_as_dictionary
with open("dumped_df_with_names_kb22and_budgets.pickle", "rb") as f:
    df = pickle.load(f)
budget = 9000
dreamlist = DreamList.from_dataframe(df)
exit(0)
total_requested = 0
total_budgeted = 0
total_funding = 0
for dream in dreamlist.dreams:
    total_requested += dream.maximum_grant_sought
    total_budgeted += dream.minimum_budget
    total_funding += dream.preexisting_funding

print(total_requested, len(dreamlist.dreams), len(dreamlist.fully_funded_dreams), len(dreamlist.invalid_dreams))
print(total_requested, total_budgeted, total_funding)

from selenium import webdriver
driver = webdriver.Chrome()
rescraped = []
for dream in dreamlist.invalid_dreams:
    rescrape = get_dream_as_dictionary(driver, dream.link)
    if rescrape.get('minimum_budget'):
        rescraped.append(rescrape)
    else:
        print(rescrape.get('link'))
driver.close()
#import pickle
#
#with open("rescraped.pickle", "wb") as f:
#    pickle.dump(rescraped, f)
with open("rescraped.pickle", "rb") as f:
    rescraped = pickle.load(f)
print(len(rescraped))
print(sum([r.get('minimum_budget') - r.get('prexisting_funding', 0) for r in rescraped]))
exit(0)
funded_dreams = dreamlist.calculate_funding(budget)
lines = [f"# Budget: {budget} \n", "\n", f"# Budget allocated: {funded_dreams} \n \n"]

lines.append(f"## Fully Funded \n")
for dream in dreamlist.fully_funded_dreams:
    lines.append(f"[{dream.name}]({dream.link}) got fully funded. ({dream.funded}€) \n \n")

lines.append(f"## Partially Funded \n")
for dream in sorted(dreamlist.dreams, key=lambda x: x.funded):
    lines.append(f"[{dream.name}]({dream.link}) got partially funded ({dream.funded}€ of "
                 f"{dream.minimum_budget-dream.preexisting_funding} - {dream.maximum_grant_sought}) "
                 f"({dream.funded*100/dream.maximum_grant_sought if dream.maximum_grant_sought else 100:.2f}%"
                 f" of maximum) \n \n")

lines.append(f"## No funding required/Invalid Dreams \n")
for dream in dreamlist.invalid_dreams:
    lines.append(f"[{dream.name}]({dream.link}) - No funding given \n \n")

with open("Intermediate.md", "w", encoding="utf-8") as f:
    f.writelines(lines)