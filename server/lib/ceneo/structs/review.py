from dataclasses import dataclass


@dataclass
class Review:
    id: str
    author: str
    recommendation: str | None
    score_count: float
    verified: bool
    published_date: str | None
    bought_date: str | None
    votes_yes: int
    votes_no: int
    text: list
    pros: list
    cons: list

    def pros_count(self):
        return len(self.pros)

    def cons_count(self):
        return len(self.cons)
