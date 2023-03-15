from dataclasses import dataclass


@dataclass
class Review:
    id: str
    author: str
    recommendation: str
    scoreCount: int
    verified: bool
    dates: tuple
    votes: tuple
    text: str
    features: tuple
