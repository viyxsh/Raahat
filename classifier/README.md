# classifier/ (Task 4)
Rule-based category + urgency classification, duplicate detection, flag logic.
Stdlib only, no installs needed.

## Backend integration (in backend/app, POST /simulate/sms)
```python
from classifier import analyze
existing = [t.dict() for t in db_tickets]   # id, text, phone, lat, lng
r = analyze(msg.message, msg.lat, msg.lng, msg.phone, existing)
ticket = Ticket(text=msg.message, phone=msg.phone, lat=msg.lat, lng=msg.lng,
                category=r["category"], urgency=r["urgency"],
                status=r["status"])          # 'new' or 'flagged'
# optional: store r["flag_reason"], r["duplicate_of"] for the dashboard
```
Run from repo root so `classifier` is importable.

## Swap in an LLM
```python
from classifier import set_classifier
from classifier.llm_classifier import LLMClassifier
set_classifier(LLMClassifier(call_llm=my_fn))
```
## Tests
`python -m pytest classifier/tests` (or run the functions directly)
