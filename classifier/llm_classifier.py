"""Drop-in LLM classifier. Same interface as RuleBasedClassifier.

Enable with:  from classifier import set_classifier
              set_classifier(LLMClassifier(call_llm=my_function))
`call_llm(prompt: str) -> str` is any function returning the model's text.
Falls back to the rule-based result if the LLM output is invalid.
"""
import json
from .base import BaseClassifier
from .rules import RuleBasedClassifier

PROMPT = (
    "Classify this disaster-relief request. Reply ONLY with JSON: "
    '{{"category": "medical|water|shelter|other", '
    '"urgency": "low|medium|high|critical"}}\nRequest: {text}'
)


class LLMClassifier(BaseClassifier):
    def __init__(self, call_llm):
        self.call_llm = call_llm
        self.fallback = RuleBasedClassifier()

    def classify(self, text):
        try:
            data = json.loads(self.call_llm(PROMPT.format(text=text)))
            if (data["category"] in ("medical", "water", "shelter", "other")
                    and data["urgency"] in ("low", "medium", "high", "critical")):
                return {**data, "confidence": 0.9}
        except Exception:
            pass
        return self.fallback.classify(text)
