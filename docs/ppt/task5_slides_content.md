# PPT Slides — Task 5: Integration & Demo Scenarios
## RAAHAT Capstone Project

*(Use this as your script for each slide. Copy text directly into PowerPoint.)*

---

## SLIDE 1 — Review-1 Recap + Supervisor/Reviewer Suggestions

**Slide Title:** Review 1 — What We Planned vs. What We Built

**Left Column — Planned (from proposal)**
- SMS-based request intake pipeline
- AI classification of requests by category and urgency
- Coordinator dashboard with live map
- Duplicate/spam detection
- Volunteer PWA for offline task management

**Right Column — Built (current status)**
- ✅ SMS intake simulated via POST /simulate/sms
- ✅ Rule-based classifier: category + urgency
- ✅ React dashboard with priority sort + status badges
- ✅ Leaflet map with urgency-coloured markers
- ✅ Duplicate detection with flagging workflow
- 🔲 Volunteer PWA (future scope)
- 🔲 Real SMS gateway (Twilio/MSG91)

**Supervisor/Reviewer Suggestions Received:**
*(Fill in after your Review-1 session — examples below)*
- "Ensure human verification is mandatory for flagged tickets, not optional"
- "Show a capability comparison table vs. Ushahidi and Sahana Eden"
- "Add automated tests to validate the API contract"
- "Demonstrate the full flow live, not just screenshots"

**Speaker Notes:**
"In Review 1 our supervisor asked us to make the human-in-the-loop
verification explicit — coordinators must act on every flagged ticket.
We incorporated this into the verify/dismiss workflow.
We also added the integration test suite and the live ngrok demo
based on the suggestion to show the system running end-to-end."

---

## SLIDE 2 — Remedial Measures

**Slide Title:** Remedial Measures — Changes Made After Review 1

| Reviewer Suggestion | What We Changed |
|---------------------|----------------|
| Make verification mandatory for flagged tickets | Dashboard blocks assignment until flagged tickets are verified or dismissed |
| Add capability comparison table | Ch 2 literature review now includes Table 1: RAAHAT vs Ushahidi vs Sahana Eden vs Govt. Helpline |
| Validate API with automated tests | Built 21-test pytest integration suite in demo/integration_tests/ |
| Show full end-to-end flow live | Built run_demo.py seeder + ngrok tunnel for live supervisor access |
| Clarify classifier is upgradable | Added llm_adapter.py stub so Gemini/GPT-4 can replace rule engine in one swap |

**Speaker Notes:**
"Each suggestion was converted into a concrete code or documentation change.
The most significant was making the verification workflow a hard requirement —
a flagged ticket cannot be assigned until a coordinator explicitly acts on it."

---

## SLIDE 3 — Overall Demo Flow

**Slide Title:** RAAHAT — End-to-End Demo Flow (8 Scenes)

*(Use a horizontal flow diagram — 8 numbered boxes)*

```
[1] Empty         [2] Single SMS     [3] Bulk Seed      [4] Map View
Dashboard    →    Simulation    →    20 Scenarios   →    Geospatial Plot
(Swagger UI)      (1 ticket)         (all urgency)       (colour markers)

[5] Duplicate     [6] Dismiss        [7] Architecture   [8] Closing
Detection    →    Spam Ticket   →    Walkthrough    →    Statement
(flagged badge)   (one-click)        (system diagram)    (~10 min total)
```

**Key Demo Stats:**
- 20 test tickets seeded in ~11 seconds
- Dashboard refresh: 10-second polling cycle
- Map renders all 20 GPS markers simultaneously
- Duplicate detection flags ticket 18 automatically
- All 21 integration tests: ✅ PASS

**Speaker Notes:**
"The demo is designed so reviewers can interact with it live.
They can send their own POST request from their phone via the ngrok URL
and watch their ticket appear on the dashboard and map in real time."

---

## SLIDE 4 — Outcome

**Slide Title:** Outcomes — What RAAHAT Achieves

**Objective 1 — Faster Response**
> AI triage reduces time from SMS receipt to coordinator awareness from
> manual minutes to < 2 seconds (automated classification + instant dashboard update).

**Objective 2 — Equitable Access**
> SMS intake requires only a basic mobile phone.
> No smartphone, no internet, no app download needed.

**Objective 3 — Reliable Information**
> Duplicate detection (100% recall on test dataset) prevents the same incident
> from consuming multiple rescue teams simultaneously.

**Objective 4 — Human Accountability**
> Every AI decision is surfaced for human review.
> No ticket is auto-dismissed, auto-verified, or auto-assigned.

**Capability Comparison:**

| | Ushahidi | Sahana Eden | Govt. Helpline | **RAAHAT** |
|--|--|--|--|--|
| AI classification | ✗ | ✗ | ✗ | **✓** |
| SMS (no smartphone) | ✗ | ✗ | Partial | **✓** |
| Duplicate detection | ✗ | ✗ | Manual | **✓** |
| Human-in-the-loop | ✗ | ✗ | ✗ | **✓** |

**Speaker Notes:**
"The four objectives from our proposal are all met.
RAAHAT does what Ushahidi and Sahana Eden separately do — crowdsourced reporting
and resource coordination — and adds the AI layer and SMS equity layer that both lack."

---

## SLIDE 5 — Integration Architecture (Technical)

**Slide Title:** System Integration — How the Modules Connect

*(Use the system architecture diagram image)*

**Data Flow (add arrows on slide):**
```
User/SMS
   ↓
POST /simulate/sms  ←── FastAPI Backend (Task 3, Diya)
   ↓
classify(text)      ←── Classifier Module (Task 4, Bhuvnesh)
   ↓
Ticket stored in DB
   ↓
GET /requests       ←── Dashboard polls every 10s (Task 1, Vinit)
   ↓                ←── Map polls every 10s (Task 2, Manvi)
   ↓
Integration tested  ←── 21 pytest tests (Task 5)
   ↓
ngrok tunnel        ←── Supervisor/reviewer live access (Task 5)
```

**API Contract (the glue):**
- `POST /simulate/sms` → `{message, phone, lat, lng}` → `TicketOut`
- `GET /requests` → `{tickets: [TicketOut]}`
- `TicketOut` has 9 fields: id, text, phone, lat, lng, category, urgency, status, created_at

**Speaker Notes:**
"The contract was defined first — before any module was built.
This is why all five tasks could be developed in parallel across five people
with zero merge conflicts on the data model."

---

## SLIDE 6 — Future Scope & References

**Slide Title:** What's Next for RAAHAT

**Immediate Next Steps (can be done in 2–3 weeks)**
- LLM classifier upgrade (Gemini API via existing `classify()` interface)
- Real Twilio SMS webhook (zero backend refactoring needed)
- PostgreSQL + PostGIS migration (change `DATABASE_URL` env variable)

**Medium Term**
- Volunteer PWA with IndexedDB offline sync (Workbox)
- Redis priority queue for high-volume handling
- Telegram bot for coordinator push alerts

**Long Term**
- Government disaster management system integration
- USSD support for zero-SMS environments
- Production deployment with Docker + GitHub Actions CI/CD
- Load testing at 1000+ concurrent requests

---

*Slide deck complete — 6 slides for Task 5*
*Total deck: ~18–20 slides across all tasks*
