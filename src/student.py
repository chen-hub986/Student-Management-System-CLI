from dataclasses import dataclass, field
from typing import List, Dict, Any
from src.exceptions import InvalidScoreException


@dataclass
class Student:
    name: str
    _scores: List[float] = field(default_factory=list, init=False, repr=False)

    def __init__(self, name: str, scores: List[float]):
        self.name = name
        self.scores = scores

    @property
    def scores(self):
        return self._scores

    @scores.setter
    def scores(self, values: List[float]):
        if not all(isinstance(score, (int, float)) for score in values):
            raise InvalidScoreException("成績無效，請確保所有成績都是數字。")

        if not values:
            raise InvalidScoreException("成績列表不能為空。")

        if any(score < 0 or score > 100 for score in values):
            raise InvalidScoreException("成績無效，請確保成績在 0 到 100 之間。")

        self._scores = values

    @property
    def average_score(self) -> float:
        if not self._scores:
            return 0.0
        return sum(self._scores) / len(self._scores)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "scores": self.scores
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Student':
        return cls(name=data['name'], scores=data['scores'])
