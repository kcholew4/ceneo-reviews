from dataclasses import dataclass


@dataclass
class Review:
    id: str
    author: str
    recommendation: str
    score_count: int
    verified: bool
    published_date: str
    bought_date: str
    votes_yes: int
    votes_no: int
    text: str
    pros: list
    cons: list
