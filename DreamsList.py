import dataclasses
from typing import List
import math


@dataclasses.dataclass
class Dream:
    name: List[str]
    min: float
    max: float
    pre: float
    votes: float
    funded: dataclasses.field(init=False) = 0
    fun: dataclasses.field(init=False) = None
    email: str = None
    url: str = None
    link: str = None

    def __post_init__(self):
        self.fun = self.votes - self.pre
        self.funded = 0


class DreamList:
    dreams: List[Dream]
    fully_funded_dreams: List[Dream]
    invalid_dreams = List[Dream]

    @classmethod
    def from_dataframe(cls, df):
        new_df = df.rename(columns= lambda x: x.strip().lower())
        dreamlist = [Dream(**l) for l in new_df.to_dict(orient='records')]

        invalid_dreams = [a for a in dreamlist if math.isnan(a.votes) or a.min == a.max == 1]
        for dream in invalid_dreams:
            dreamlist.remove(dream)
        output = cls(dreamlist)
        output.invalid_dreams = invalid_dreams
        return output

    def __init__(self, dreams_in: List[Dream] = None):
        if dreams_in is None:
            self.dreams = []
        else:
            self.dreams = dreams_in

        self.fully_funded_dreams = []
        self.invalid_dreams = []

    def calculate_total_tokens(self):
        total_tokens = sum(d.fun for d in self.dreams)
        return total_tokens

    def calculate_token_value(self, budget: float):
        total_tokens = self.calculate_total_tokens()
        single_token_value = budget/total_tokens
        return single_token_value

    def calculate_funding(self, budget: float):
        extra_budget = budget
        while extra_budget:
            single_token = self.calculate_token_value(extra_budget)
            extra_budget = 0
            fully_funded = []
            for dream in self.dreams:
                dream.funded += dream.fun*single_token
                if dream.funded > dream.max:
                    difference = dream.funded - dream.max
                    extra_budget += difference
                    dream.funded = dream.max
                    fully_funded.append(dream)
            self.fully_funded_dreams += fully_funded
            for dream in fully_funded:
                self.dreams.remove(dream)
        for dream in self.dreams:
            dream.funded = round(dream.funded)
        for dream in self.fully_funded_dreams:
            dream.fun = round(dream.funded)
        print("BUDGET", budget, sum([dream.funded for dream in self.dreams + self.fully_funded_dreams]))

