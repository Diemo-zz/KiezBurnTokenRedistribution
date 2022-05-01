import dataclasses
from typing import List, Dict
import math

class DreamInputException(Exception):
    def __init__(self, message):
        super(DreamInputException, self).__init__()
        self.message = message

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
        except Exception:
            return False
        dont_need_money = funding <= 0 or self.maximum_grant_sought == 0 \
                          or self.maximum_budget == self.minimum_budget == self.preexisting_funding
        return not dont_need_money

    def apply_funding(self, vote_value: float) -> float:
        if vote_value < 0:
            raise DreamInputException(message="vote value must be greater than 0")
        value = self.total_votes*vote_value
        if value > self.maximum_grant_sought:
            value = self.maximum_grant_sought
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
        dictionaries = [l for l in new_df.to_dict(orient='records')]
        dictionaries = [{k: v for k, v in l.items() if not (k == 'budget' or k == 'pre')}  for l in dictionaries]

        #dreamlist = [Dream(**l) for l in new_df.to_dict(orient='records')]
        dreamlist = [Dream(**l) for l in dictionaries]

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
            budget_applied = 0
            for dream in self.dreams:
                dream_budget = dream.apply_funding(single_token)
                budget_applied += dream_budget
            extra_budget = extra_budget - budget_applied
            fully_funded = [d for d in self.dreams if d.is_fully_funded()]
            self.fully_funded_dreams += fully_funded
            for dream in fully_funded:
                self.dreams.remove(dream)
        for dream in self.dreams:
            dream.funded = round(dream.funded)
        for dream in self.fully_funded_dreams:
            dream.funded = round(dream.funded)
        return sum([dream.funded for dream in self.dreams + self.fully_funded_dreams])

