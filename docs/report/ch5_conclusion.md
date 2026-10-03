# Chapter 5 — Conclusion
## RAAHAT: AI-Powered Disaster Response and Resource Coordination Platform

*(Times New Roman 14 pt — Chapter heading)*
*(Body: Times New Roman 12 pt, single spacing)*

---

### 5.1 Summary of Work

This project developed RAAHAT — a modular, AI-assisted disaster response and
resource coordination platform — addressing four documented operational gaps in
current emergency relief workflows: digital divide exclusion, unstructured reporting
channels, triage delays from duplicate/spam reports, and fragmented dispatching.

The system was implemented across five integrated modules:

1. **Request Intake (SMS Simulation):** A FastAPI endpoint (`POST /simulate/sms`)
   accepts structured SMS payloads and converts them into typed ticket records,
   replicating the function of an SMS gateway webhook. This enables any person
   with a basic mobile phone to raise a help request without smartphone or internet
   access.

2. **AI Classification:** A rule-based classifier with a modular, LLM-swappable
   interface assigns each ticket a `category` (medical, water, shelter, food, other)
   and `urgency` (critical, high, medium, low). The rule engine achieved 90%
   category accuracy and 85% urgency accuracy on the 20-ticket evaluation dataset.

3. **Duplicate Detection:** Text-similarity analysis using cosine distance on
   TF-IDF vectors flags near-duplicate tickets for human verification rather than
   auto-dismissal, preserving coordinator oversight. Duplicate detection achieved
   100% recall on the test dataset with zero false positive flags.

4. **Coordinator Dashboard:** A React-based web dashboard presents tickets sorted
   by urgency priority with colour-coded status badges. A verify/dismiss workflow
   allows coordinators to act on flagged tickets, updating their status in real time.

5. **Live Map View:** A Leaflet.js map plots each ticket at its GPS coordinates with
   urgency-coloured markers (red: critical, orange: high, yellow: medium, green: low),
   enabling coordinators to identify geographic clustering and dispatch efficiently.

---

### 5.2 Key Outcomes

The end-to-end integration was demonstrated live with 20 seeded test scenarios across
all four request categories and urgency levels. All 21 automated integration tests
passed. The full pipeline — from SMS simulation to dashboard display to map plotting —
completed within 10 seconds per ticket cycle.

**Table 4: RAAHAT Capability Comparison (Final)**

| Capability | Ushahidi | Sahana Eden | Govt. Helpline | RAAHAT |
|------------|----------|-------------|----------------|--------|
| AI-based classification & priority | ✗ | ✗ | ✗ | ✓ |
| Works over SMS (no smartphone needed) | ✗ | ✗ | Partial (call only) | ✓ |
| Automated duplicate/spam detection | ✗ | ✗ | Manual | ✓ |
| Human-in-the-loop verification | ✗ | ✗ | ✗ | ✓ |
| Priority-sorted coordinator dashboard | Partial | ✗ | ✗ | ✓ |
| Live geospatial map of requests | ✓ | Partial | ✗ | ✓ |
| Lightweight for college / local NGO | Partial | ✗ | N/A | ✓ |

RAAHAT demonstrates that all seven capabilities can be delivered simultaneously using
entirely open-source tools and free-tier cloud services, making it immediately
deployable for college-level emergency management cells, local NGOs, and municipal
relief drives.

---

### 5.3 Limitations

**Classifier limitations:** The rule-based engine relies on keyword matching. It does
not handle negation ("I do NOT need water"), transliterated Hindi/regional language
requests ("paani chahiye sector 3"), or multi-category requests ("injured person
needs water and medical help"). These cases require a language model.

**Scale limitations:** The current SQLite storage and single-process Uvicorn server
would not scale beyond approximately 100 concurrent requests. Production deployment
requires PostgreSQL + PostGIS and a multi-worker configuration.

**Simulated SMS:** The current implementation simulates the SMS gateway via an API
call. Real deployment requires integration with a Twilio or MSG91 webhook, which
requires phone number provisioning and billing.

**No volunteer dispatch:** The current system supports ticket management up to the
`assigned` status but does not implement the volunteer matching or notification
pipeline (Volunteer PWA, Telegram alerts) that would complete the end-to-end
dispatch loop.

---

### 5.4 Future Work

1. **LLM Upgrade:** Replace the rule-based classifier with a Gemini or GPT-4 call
   via the existing modular interface (`classify(text) → dict`). No backend refactoring
   is required — only the classifier module changes.

2. **Volunteer PWA:** Implement the offline-first Progressive Web App with IndexedDB
   task queue and Workbox background sync, enabling field volunteers to receive and
   update assignments without continuous connectivity.

3. **Real SMS Gateway:** Replace `POST /simulate/sms` with a Twilio/MSG91 webhook
   handler. The backend schema is identical; only the trigger mechanism changes.

4. **PostgreSQL + PostGIS:** Migrate from SQLite to PostgreSQL with PostGIS to enable
   geo-queries ("find all requests within 2 km of this volunteer") and support
   concurrent write loads during high-volume disaster scenarios.

5. **Redis Priority Queue:** Add a Redis-backed priority queue for real-time volunteer
   matching and rate-limiting of spam requests from a single phone number.

6. **Production Deployment:** Containerise all services with Docker and deploy on a
   free-tier cloud instance (Render, Railway, or AWS EC2), with a GitHub Actions
   CI/CD pipeline for automatic testing on every push.

---

### 5.5 Final Statement

RAAHAT establishes that a lightweight, modular, AI-assisted triage platform — built
entirely with open-source tools and designed for equitable access — is technically
feasible, demonstrably functional, and immediately applicable to localized emergency
management scenarios.

By combining automated classification with explicit human-in-the-loop verification,
RAAHAT embodies the responsible automation principle advocated by the disaster
informatics research community: AI accelerates the decision, but the human makes
the call. This design philosophy ensures that the system remains trustworthy even as
its AI components are upgraded, and that coordinators — not algorithms — remain
accountable for every relief action taken.

---

*References for this chapter: [1] Okolloh 2009 · [2] Duc et al. 2014 · [3] Imran et al. 2015 · [7] Biørn-Hansen et al. 2017 · [10] Stanford HAI 2026*
