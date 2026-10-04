"""Rule-based category and urgency classifier (English + Hinglish keywords)."""
import re
from .base import BaseClassifier

CATEGORY_KEYWORDS = {
    "medical": {
        "doctor": 2, "medicine": 2, "medical": 2, "ambulance": 3, "injured": 3,
        "injury": 3, "bleeding": 3, "hospital": 2, "fracture": 3, "insulin": 3,
        "oxygen": 3, "pregnant": 3, "unconscious": 3, "ill": 1, "sick": 2,
        "fever": 2, "wound": 2, "dawai": 2, "dawa": 2, "ghayal": 3, "bimar": 2,
        "first aid": 2, "heart": 1, "breathing": 3,
    },
    "water": {
        "water": 3, "drinking": 2, "thirsty": 3, "thirst": 3, "paani": 3,
        "pani": 3, "tanker": 2, "bottle": 1, "bottles": 1, "dehydration": 3,
        "well": 1, "flooded": 1,
    },
    "shelter": {
        "shelter": 3, "tent": 3, "roof": 2, "homeless": 3, "blanket": 2,
        "blankets": 2, "stranded": 2, "evacuate": 3, "evacuation": 3,
        "house": 1, "home": 1, "collapsed": 2, "camp": 2, "ghar": 2,
        "trapped": 1, "rescue": 2, "food": 1, "cold": 1,
    },
}

URGENCY_KEYWORDS = {
    "critical": [
        "dying", "not breathing", "trapped", "unconscious", "bleeding heavily",
        "heavy bleeding", "drowning", "fire", "collapsed", "life threatening",
        "cardiac", "heart attack", "sos", "bachao", "jaan",
    ],
    "high": [
        "urgent", "urgently", "emergency", "injured", "bleeding", "children",
        "child", "kids", "baby", "elderly", "pregnant", "ambulance", "asap",
        "immediately", "jaldi", "fracture", "stranded", "2 days", "3 days",
        "since yesterday",
    ],
    "medium": [
        "need", "needed", "require", "required", "shortage", "running out",
        "please", "help", "chahiye", "zarurat", "madad",
    ],
}

LEVELS = ["low", "medium", "high", "critical"]


def _tokens(text: str) -> str:
    return " " + re.sub(r"[^a-z0-9\s]", " ", text.lower()) + " "


def _has(text: str, kw: str) -> bool:
    return f" {kw} " in text or (" " in kw and kw in text)


class RuleBasedClassifier(BaseClassifier):
    def classify(self, text: str):
        t = _tokens(text)

        scores = {
            cat: sum(w for kw, w in kws.items() if _has(t, kw))
            for cat, kws in CATEGORY_KEYWORDS.items()
        }
        best = max(scores, key=scores.get)
        total = sum(scores.values())
        if scores[best] == 0:
            category, cat_conf = "other", 0.3
        else:
            category = best
            cat_conf = round(scores[best] / total, 2)

        urgency = "low"
        for level in ("critical", "high", "medium"):
            if any(_has(t, kw) for kw in URGENCY_KEYWORDS[level]):
                urgency = level
                break

        # Medical requests are never treated as low priority.
        if category == "medical" and LEVELS.index(urgency) < 1:
            urgency = "medium"
        # Several urgency cues together escalate by one level.
        hits = sum(_has(t, kw) for kw in URGENCY_KEYWORDS["high"])
        if hits >= 3 and urgency == "high":
            urgency = "critical"
        # SMS shouting (ALL CAPS) is a mild urgency signal.
        letters = [c for c in text if c.isalpha()]
        if urgency == "low" and len(letters) > 8 and text.upper() == text:
            urgency = "medium"

        return {"category": category, "urgency": urgency, "confidence": cat_conf}
