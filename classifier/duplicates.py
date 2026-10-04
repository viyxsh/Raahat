"""Text-similarity duplicate detection (stdlib only)."""
import math
import re
from difflib import SequenceMatcher

STOPWORDS = {"a", "an", "the", "is", "are", "we", "i", "to", "of", "in", "at",
             "and", "for", "need", "needed", "please", "help", "us", "my", "our",
             "urgent", "urgently", "required", "send"}


def normalize(text: str) -> list:
    words = re.sub(r"[^a-z0-9\s]", " ", text.lower()).split()
    return [w for w in words if w not in STOPWORDS]


def text_similarity(a: str, b: str) -> float:
    ta, tb = normalize(a), normalize(b)
    if not ta or not tb:
        return 0.0
    sa, sb = set(ta), set(tb)
    jaccard = len(sa & sb) / len(sa | sb)
    seq = SequenceMatcher(None, " ".join(ta), " ".join(tb)).ratio()
    return round(max(jaccard, seq), 3)


def distance_km(lat1, lng1, lat2, lng2):
    if None in (lat1, lng1, lat2, lng2):
        return None
    p = math.pi / 180
    a = (math.sin((lat2 - lat1) * p / 2) ** 2 +
         math.cos(lat1 * p) * math.cos(lat2 * p) * math.sin((lng2 - lng1) * p / 2) ** 2)
    return 12742 * math.asin(math.sqrt(a))


def find_duplicate(text, lat, lng, phone, existing, text_threshold=0.6,
                   radius_km=1.0):
    """Return (ticket_id, score) of the best matching earlier ticket, or (None, 0)."""
    best_id, best_score = None, 0.0
    for t in existing:
        sim = text_similarity(text, t.get("text", ""))
        dist = distance_km(lat, lng, t.get("lat"), t.get("lng"))
        near = dist is None or dist <= radius_km
        same_phone = bool(phone) and phone == t.get("phone")
        is_dup = (sim >= text_threshold and near) or (same_phone and sim >= 0.5)
        if is_dup and sim > best_score:
            best_id, best_score = t.get("id"), sim
    return best_id, best_score
