"""
classifier/classifier.py
Rule-based classifier — works standalone until Bhuvnesh's full version is ready.
Interface contract: classify(text) -> {category, urgency, is_duplicate}
"""

import re
from difflib import SequenceMatcher

# ── keyword rules ─────────────────────────────────────────────────────────────

CATEGORY_RULES = {
    "medical":  ["blood", "injury", "injur", "hospital", "unconscious", "ambulance",
                 "medicine", "doctor", "dying", "icu", "oxygen", "patient", "fever",
                 "wound", "fracture", "heart", "accident", "emergency medical"],
    "water":    ["water", "flood", "drowning", "drinking", "pipeline", "thirst",
                 "paani", "flooding", "waterlog", "water log"],
    "shelter":  ["shelter", "roof", "trapped", "house", "building", "stuck",
                 "collapsed", "collapse", "tent", "temporary shelter", "homeless", "displaced"],
    "food":     ["food", "hungry", "hunger", "starving", "starvation", "meals",
                 "ration", "eat", "milk", "baby food", "grain"],
}

URGENCY_RULES = {
    "critical": ["unconscious", "dying", "trapped", "critical", "oxygen machine",
                 "icu", "collapsed roof", "not working icu", "life threatening",
                 "road accident", "severe", "drowning"],
    "high":     ["urgent", "urgently", "immediately", "blood", "flood", "ambulance",
                 "need now", "please help", "asap", "emergency", "right now",
                 "not available", "no food", "no water", "baby"],
    "medium":   ["need", "require", "help", "needed", "required"],
}


def _clean(text: str) -> str:
    return text.lower().strip()


def _classify_category(text: str) -> str:
    t = _clean(text)
    scores = {cat: 0 for cat in CATEGORY_RULES}
    for cat, keywords in CATEGORY_RULES.items():
        for kw in keywords:
            # Word boundary or exact presence
            if re.search(r'\b' + re.escape(kw) + r'\b', t):
                # Primary survival needs get high priority over contextual locations like 'camp'
                weight = 2 if cat in ("food", "medical", "water") else 1
                scores[cat] += weight
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "other"


def _classify_urgency(text: str) -> str:
    t = _clean(text)
    for level in ("critical", "high", "medium"):
        for kw in URGENCY_RULES[level]:
            if kw in t:
                return level
    return "low"


# ── duplicate store (in-memory for dev, shared with DB in prod) ───────────────

_seen_messages: list[str] = []
DUPLICATE_THRESHOLD = 0.60   # threshold for near duplicate flags


def _similarity(a: str, b: str) -> float:
    sa = set(_clean(a).split())
    sb = set(_clean(b).split())
    if not sa or not sb:
        return 0.0
    # Jaccard + sequence ratio blend
    jaccard = len(sa & sb) / len(sa | sb)
    ratio = SequenceMatcher(None, _clean(a), _clean(b)).ratio()
    # Check substring containment (e.g. "NEED WATER SECTOR 3" inside longer string)
    contains = 0.8 if (_clean(a) in _clean(b) or _clean(b) in _clean(a)) else 0.0
    return max(jaccard, ratio, contains)


def _is_duplicate(text: str) -> bool:
    for prev in _seen_messages:
        if _similarity(text, prev) >= DUPLICATE_THRESHOLD:
            return True
    _seen_messages.append(text)
    return False


# ── public interface ──────────────────────────────────────────────────────────

def classify(text: str) -> dict:
    """
    Returns:
        {
            "category":     "medical" | "water" | "shelter" | "food" | "other",
            "urgency":      "critical" | "high" | "medium" | "low",
            "is_duplicate": bool
        }
    """
    return {
        "category":     _classify_category(text),
        "urgency":      _classify_urgency(text),
        "is_duplicate": _is_duplicate(text),
    }
