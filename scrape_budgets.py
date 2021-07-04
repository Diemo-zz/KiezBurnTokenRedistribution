import pickle
from DreamsList import DreamList
from pprintpp import pprint
from operator import attrgetter
with open("dumped_df_with_votes.pickle", "rb") as f:
    df = pickle.load(f)


dreamlist = DreamList.from_dataframe(df)

funded_dreams = dreamlist.calculate_funding(9000)
pprint(dreamlist.fully_funded_dreams)
print(len(dreamlist.fully_funded_dreams))


print("FULLY FUNDED")
for dream in dreamlist.fully_funded_dreams:
    print(dream.link, dream.funded)

print("PARTIALLY FUNDED")
for dream in sorted(dreamlist.dreams, key=lambda x: x.funded):
    print(dream.link, dream.funded, dream.max)