from abc import ABC, abstractmethod
from typing import Dict


class BaseClassifier(ABC):
    """Any classifier (rules, LLM, ML model) must implement this.

    classify() returns:
        {"category": "medical|water|shelter|other",
         "urgency": "low|medium|high|critical",
         "confidence": float in [0, 1]}
    """

    @abstractmethod
    def classify(self, text: str) -> Dict:
        ...
