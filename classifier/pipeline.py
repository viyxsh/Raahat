"""Glue: classify + duplicate check + flag logic."""
from .rules import RuleBasedClassifier
from .duplicates import find_duplicate

_classifier = RuleBasedClassifier()
LOW_CONFIDENCE = 0.5


def get_classifier():
    return _classifier


def set_classifier(clf):
    """Swap in an LLM/ML classifier without touching the backend."""
    global _classifier
    _classifier = clf


def analyze(text, lat=None, lng=None, phone=None, existing_tickets=None):
    """Returns dict the backend can merge straight into a ticket:
    category, urgency, status ('new' or 'flagged'), flag_reason,
    duplicate_of, confidence.
    Status is NEVER 'verified'/'assigned' here; that is the coordinator's call.
    """
    res = _classifier.classify(text or "")
    dup_id, dup_score = find_duplicate(text or "", lat, lng, phone,
                                       existing_tickets or [])
    reasons = []
    if dup_id is not None:
        reasons.append(f"possible duplicate of #{dup_id} (similarity {dup_score})")
    if res["category"] == "other":
        reasons.append("category unclear")
    elif res["confidence"] < LOW_CONFIDENCE:
        reasons.append("low classification confidence")
    if lat is None or lng is None:
        reasons.append("location missing")

    return {
        "category": res["category"],
        "urgency": res["urgency"],
        "confidence": res["confidence"],
        "status": "flagged" if reasons else "new",
        "flag_reason": "; ".join(reasons) or None,
        "duplicate_of": dup_id,
    }
