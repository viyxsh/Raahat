# Chapter 1 — Introduction
## RAAHAT: AI-Powered Disaster Response and Resource Coordination Platform

*(Times New Roman 14 pt — Chapter heading)*
*(Body: Times New Roman 12 pt, single spacing)*

---

### 1.1 Background and Motivation

Natural disasters, flash floods, and large-scale local emergencies expose a consistent
operational failure in relief management: the absence of a unified, real-time channel
through which affected people can reach coordinators, and through which coordinators
can dispatch the right resource to the right location at the right time.

During the 2013 Uttarakhand floods and the 2015 Chennai floods, responders relied
primarily on ad-hoc phone trees and WhatsApp broadcast groups. Messages were
forwarded out of sequence, urgent requests were buried under forwarded images, and
identical distress calls from the same family consumed multiple rescue teams while
adjacent households went unaided [8]. This is not a failure of good intentions — it is a
failure of information architecture.

Four specific operational gaps define the problem:

**Digital Divide Exclusion.** Web portals and mobile applications require smartphones
and stable internet connectivity. In flood-affected or power-cut zones — precisely the
environments where emergency reporting is most critical — a significant fraction of the
affected population relies on basic feature phones capable only of SMS [6].

**Unstructured Channels.** Heavy dependence on phone calls and scattered messaging
groups leads to message overload, information loss, and uncoordinated relief efforts.
There is no automated pipeline to convert a plain-text distress message into an
actionable, structured record that a coordinator can triage and assign [8, 9].

**Triage Delays and Noise.** Duplicate reports — the same incident forwarded across
multiple channels by well-meaning bystanders — and false or spam reports exhaust
scarce responder capacity. Studies of crisis-period Twitter activity show that up to 30%
of messages during an emergency are rumours or duplicates [5]. Manual de-duplication
at scale is infeasible.

**Fragmented Dispatching.** Even when a legitimate request is received, there is no
automated mechanism to match it with the nearest available volunteer or resource,
causing further delays [3].

---

### 1.2 Motivation from Research

The growth of agentic AI systems provides a timely opportunity. The Stanford AI Index
2026 reports a 280% year-over-year growth in "Agentic AI" job postings, reflecting
industry-wide recognition that supervised AI agents — systems that act but defer to
humans on high-stakes decisions — are now technically feasible and practically valuable
[10].

In the disaster management domain, Imran et al. (2015) surveyed the state of social
media processing during mass emergencies and identified automated classification of
crisis messages as the single highest-impact unsolved problem in the field [3]. Their
subsequent work on AIDR (Artificial Intelligence for Disaster Response) demonstrated
that machine learning classifiers trained on crisis tweets could achieve accuracy
comparable to trained human volunteers [4].

Existing open-source platforms — Ushahidi and Sahana Eden — provide crowdsourced
incident mapping and resource management respectively, but neither incorporates
automated classification, urgency prioritization, or SMS-first intake designed for
low-connectivity environments [1, 2]. RAAHAT is designed to fill precisely this gap.

---

### 1.3 Project Objective

RAAHAT (Rapid AI-Assisted Help and Triage) aims to develop a lightweight,
AI-assisted disaster response coordination platform with the following specific
objectives:

1. **SMS-First Intake:** Accept emergency requests via SMS simulation (and, in
   production, via Twilio/MSG91 gateway) so that any person with a basic mobile
   phone can raise a help request without a smartphone or internet connection.

2. **Automated Classification:** Classify each incoming request by category
   (medical, water, shelter, food, other) and urgency (critical, high, medium, low)
   using a rule-based AI classifier designed with an LLM-swappable interface.

3. **Duplicate and Spam Detection:** Detect near-duplicate reports using
   text-similarity analysis and flag them for human verification rather than
   auto-dismissing, preserving coordinator oversight.

4. **Coordinator Dashboard:** Provide a priority-sorted, real-time request list
   with status badges (new, flagged, verified, assigned) and a verify/dismiss
   workflow for flagged tickets.

5. **Live Map View:** Plot all active requests on an interactive geospatial map
   with urgency-coloured markers, enabling coordinators to identify geographic
   clusters and dispatch volunteers efficiently.

6. **Human-in-the-Loop Design:** Ensure that no high-stakes action — verification,
   dismissal, assignment — is taken by the system autonomously. Every AI decision
   is surfaced for human confirmation.

---

### 1.4 Scope

**In Scope (current implementation)**

- SMS-to-ticket intake pipeline (simulated via `POST /simulate/sms`)
- Rule-based AI classification: category and urgency assignment
- Text-similarity duplicate detection with coordinator verification workflow
- FastAPI backend with REST API and SQLite/PostgreSQL storage
- React coordinator dashboard with priority-sorted ticket list and status badges
- Leaflet.js live map with urgency-coloured markers
- End-to-end integration demonstration with 20 seeded test scenarios

**Future Scope**

- Volunteer PWA with offline-first task management and background sync
- Real SMS gateway integration (Twilio / MSG91 webhook)
- USSD support for feature phones without SMS data capability
- PostgreSQL + PostGIS geo-queries for nearest-volunteer matching
- Redis priority queue for high-throughput request handling
- LLM upgrade: Gemini/GPT-4 as the classification engine
- Telegram bot for real-time coordinator alerts
- Production deployment on cloud infrastructure with Docker and CI/CD

---

### 1.5 Report Structure

- **Chapter 2** — Literature Review: analysis of existing disaster management platforms and
  AI-based crisis message classification research.
- **Chapter 3** — System Description: architecture, technology stack, and component
  specifications for each module.
- **Chapter 4** — Methodology, Results, and Discussion: working principle of each module,
  end-to-end validation results, and individual contributions.
- **Chapter 5** — Conclusion: summary of outcomes, limitations, and future directions.

---

*References for this chapter: [1] Okolloh 2009 · [2] Duc et al. 2014 · [3] Imran et al. 2015 · [4] Imran et al. 2014 · [5] Mendoza et al. 2010 · [6] Munro 2013 · [8] Palen & Liu 2007 · [9] Vieweg et al. 2010 · [10] Stanford HAI 2026*
