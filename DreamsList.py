import dataclasses
from typing import List
import math


@dataclasses.dataclass
class Dream:
    name: str
    dreamers: List[str]
    minimum_budget: float
    maximum_budget: float
    preexisting_funding: float
    total_funding: float
    funded: dataclasses.field(init=False) = 0
    total_votes: dataclasses.field(init=False) = None
    maximum_grant_sought: dataclasses.field(init=False) = None
    email: str = None
    url: str = None
    link: str = None

    def __post_init__(self):
        self.funded = 0.0
        self.calculate_votes()
        self.calculate_grant()

    def calculate_votes(self):
        self.total_votes = self.total_funding - self.preexisting_funding

    def calculate_grant(self):
        self.maximum_grant_sought = self.maximum_budget - self.preexisting_funding

    def is_valid(self):
        try:
            funding = float(self.total_votes)
        except Exception as e:
            print(e)
            return False
        dont_need_money = funding <= 0 or self.maximum_grant_sought == 0 \
                          or self.maximum_budget == self.minimum_budget == self.preexisting_funding
        return not dont_need_money

    def apply_funding(self, vote_value: float):
        value = self.total_votes*vote_value
        if value > self.maximum_budget:
            value = self.maximum_budget
        self.funded = value
        return self.funded

    def is_fully_funded(self):
        return self.funded >= self.maximum_budget

class DreamList:
    dreams: List[Dream]
    fully_funded_dreams: List[Dream]
    invalid_dreams = List[Dream]

    @classmethod
    def from_dataframe(cls, df):
        new_df = df.rename(columns= lambda x: x.strip().lower())
        dreamlist = [Dream(**l) for l in new_df.to_dict(orient='records')]

        invalid_dreams = [a for a in dreamlist if not a.is_valid()]
        for dream in invalid_dreams:
            dreamlist.remove(dream)
        output = cls(dreamlist)
        output.invalid_dreams = invalid_dreams
        return output

    def __init__(self, dreams_in: List[Dream] = None):
        if dreams_in is None:
            dreams_in = []

        self.fully_funded_dreams = []
        self.invalid_dreams = [a for a in dreams_in if not a.is_valid()]
        self.dreams = [a for a in dreams_in if a not in self.invalid_dreams]

    def calculate_total_tokens(self):
        total_tokens = sum(d.total_votes for d in self.dreams)
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
                dream.funded += dream.total_votes * single_token
                if dream.funded > dream.maximum_budget:
                    difference = dream.funded - dream.maximum_budget
                    extra_budget += difference
                    dream.funded = dream.maximum_budget
                    fully_funded.append(dream)
            self.fully_funded_dreams += fully_funded
            for dream in fully_funded:
                self.dreams.remove(dream)
        for dream in self.dreams:
            dream.funded = round(dream.funded)
        for dream in self.fully_funded_dreams:
            dream.funded = round(dream.funded)
        return sum([dream.funded for dream in self.dreams + self.fully_funded_dreams])

