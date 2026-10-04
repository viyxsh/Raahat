# TASK 4 – PPT CONTENT

## Slide A: AI Classification Module
**Title:** AI Classification & Duplicate Detection
- Input: raw SMS text + location + phone
- Category: medical / water / shelter / other (weighted keywords, English + Hinglish)
- Urgency: low / medium / high / critical (severity cues + escalation rules)
- Duplicate check: text similarity (Jaccard + sequence ratio) + distance within 1 km
- Output: category, urgency, status (new / flagged), flag reason
- Stdlib-only Python: fast, works offline, no training data
- LLM-swappable: common `BaseClassifier` interface, rule-based fallback
**Visual:** flow: SMS -> Classifier -> Duplicate check -> Flag logic -> Ticket (+ Table 1 mini sample)
**Speaker note:** Rules give predictable, explainable results in a disaster; an LLM can replace them later without touching the backend.

## Slide B: Human-in-the-Loop Verification
**Title:** AI Suggests, Coordinator Decides
- AI sets only "new" or "flagged"; never verified/assigned
- Flag reasons: possible duplicate, unclear category, low confidence, missing location
- Coordinator verifies or dismisses on the dashboard
- No ticket is auto-deleted or auto-merged, so a genuine call for help is never lost
- Priority list sorted by urgency so critical cases are handled first
**Visual:** New -> Flagged -> Verified -> Assigned, with a "coordinator" icon on the last two arrows.
**Speaker note:** A missed real request is costlier than one extra ticket, so uncertain cases go to a human.
