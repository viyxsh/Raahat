import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from classifier import analyze

CASES = [
    ("NEED WATER SECTOR 3", "water", "medium"),
    ("Pregnant woman in labour, need ambulance urgently", "medical", "critical"),
    ("Man unconscious and bleeding heavily near bridge", "medical", "critical"),
    ("Family trapped under collapsed house, please help", "shelter", "critical"),
    ("Need tents and blankets for 20 people", "shelter", "medium"),
    ("paani chahiye, bachche pyase hain", "water", "medium"),
    ("Medicine for diabetes patient required", "medical", "medium"),
    ("hello is anyone there", "other", "low"),
]


def test_cases():
    for text, cat, urg in CASES:
        r = analyze(text, 23.21, 77.41)
        assert (r["category"], r["urgency"]) == (cat, urg), (text, r)


def test_duplicate_flagged():
    first = {"id": 1, "text": "NEED WATER SECTOR 3", "phone": "+911", "lat": 23.21, "lng": 77.41}
    r = analyze("need water in sector 3", 23.2101, 77.4101, "+912", [first])
    assert r["status"] == "flagged" and r["duplicate_of"] == 1


def test_far_away_not_duplicate():
    first = {"id": 1, "text": "NEED WATER SECTOR 3", "phone": "+911", "lat": 23.21, "lng": 77.41}
    r = analyze("NEED WATER SECTOR 3", 23.40, 77.80, "+912", [first])
    assert r["duplicate_of"] is None and r["status"] == "new"


def test_missing_location_flagged():
    assert analyze("need tent")["status"] == "flagged"
