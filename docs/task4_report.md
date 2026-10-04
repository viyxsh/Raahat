# TASK 4 – REPORT CONTENT
(Times New Roman, 12 pt body / 14 pt headings, single spacing)

## CHAPTER 2: EXISTING WORK / LITERATURE REVIEW

### 2.1 Crisis Information Management Systems
Crowdsourced crisis mapping platforms such as Ushahidi, first used during the 2008 post-election violence in Kenya and the 2010 Haiti earthquake, showed that citizen reports (SMS, web, e-mail) can be collected and plotted on a map in near real time. However, these platforms depend largely on volunteers to read, categorise and verify each incoming report manually. During large disasters, the volume of messages exceeds the capacity of human moderators, creating a triage bottleneck.

### 2.2 Classification of Crisis Messages
Imran et al. (2015) surveyed the processing of social media messages in mass emergencies and identified classification (informative vs. non-informative, and by information type such as needs, offers, damage) as the central step before any response can be coordinated. Olteanu et al. (2014) proposed CrisisLex, a lexicon of crisis-related terms for filtering messages, showing that curated keyword lists give a strong, transparent baseline. Starbird et al. (2010) examined how information is produced and propagated during emergencies, motivating filters that favour actionable messages. Nguyen et al. (2017) applied convolutional neural networks to crisis tweets and obtained better accuracy than classic models, but needed large labelled datasets, which are rarely available for a new region or language at the time of a disaster.

### 2.3 Rule-Based vs. Machine-Learning vs. LLM Approaches
Rule-based classifiers are deterministic, need no training data, run instantly on low-end hardware, and can be audited by a coordinator. Their weakness is limited coverage of paraphrases, spelling variants and code-mixed text (e.g. Hinglish, "paani chahiye"). Supervised models (Naive Bayes, SVM, deep networks, BERT-style transformers; Devlin et al., 2019) generalise better but require labelled data and compute. Large language models can classify with few or no examples, but raise concerns about latency, cost, connectivity, and hallucinated or unexplained outputs in a safety-critical domain. Hybrid designs, with rules as a dependable baseline and a model behind a common interface, are therefore attractive.

### 2.4 Duplicate and Near-Duplicate Detection
In disasters, the same need is reported repeatedly by different people, which inflates the request queue. Standard text-similarity measures include Jaccard similarity on token sets, TF-IDF with cosine similarity (Salton & Buckley, 1988), and edit-distance based measures (Levenshtein, 1966). Combining text similarity with spatial proximity is a natural fit for geo-tagged requests, because two near-identical messages from the same neighbourhood are far more likely to describe one incident than two identical messages from distant places.

### 2.5 Human-in-the-Loop Decision Support
Amershi et al. (2014) argue that interactive machine learning, where people review and correct model output, produces more trustworthy systems than full automation. In emergency response, wrongly auto-dismissing a genuine call for help is far costlier than showing a coordinator one extra ticket. Systems should therefore flag uncertain cases rather than silently resolve them.

### 2.6 Research Gap
Existing platforms either rely on manual triage (slow) or on data-hungry models (hard to deploy offline in low-resource regions). Few offer an SMS-first, lightweight pipeline that classifies category and urgency, detects duplicates using text and location together, and keeps a coordinator in control of the final decision. The present project addresses this gap.

### References (Chapter 2)
[1] J. Okolloh, "Ushahidi, or 'testimony': Web 2.0 tools for crowdsourcing crisis information," Participatory Learning and Action, vol. 59, 2009.
[2] M. Imran, C. Castillo, F. Diaz, S. Vieweg, "Processing social media messages in mass emergency: A survey," ACM Computing Surveys, vol. 47, no. 4, 2015.
[3] A. Olteanu, C. Castillo, F. Diaz, S. Vieweg, "CrisisLex: A lexicon for collecting and filtering microblogged communications in crises," ICWSM, 2014.
[4] K. Starbird, L. Palen, A. Hughes, S. Vieweg, "Chatter on the red: What hazards threat reveals about the social life of microblogged information," ACM CSCW, 2010.
[5] D. T. Nguyen, K. Al-Mannai, S. Joty, H. Sajjad, M. Imran, P. Mitra, "Robust classification of crisis-related data on social networks using convolutional neural networks," ICWSM, 2017.
[6] J. Devlin, M. Chang, K. Lee, K. Toutanova, "BERT: Pre-training of deep bidirectional transformers for language understanding," NAACL-HLT, 2019.
[7] G. Salton, C. Buckley, "Term-weighting approaches in automatic text retrieval," Information Processing & Management, vol. 24, no. 5, 1988.
[8] V. I. Levenshtein, "Binary codes capable of correcting deletions, insertions and reversals," Soviet Physics Doklady, vol. 10, no. 8, 1966.
[9] S. Amershi, M. Cakmak, W. B. Knox, T. Kulesza, "Power to the people: The role of humans in interactive machine learning," AI Magazine, vol. 35, no. 4, 2014.
(Please double-check volume/page details before final submission.)

---

## CHAPTER 4 (Task 4 part): CLASSIFICATION METHODOLOGY

### 4.x Classification and Duplicate Detection Methodology
Every incoming SMS ticket passes through a three-stage pipeline in the `classifier/` module before it is stored.

**Stage 1 – Category classification.** The message is lower-cased and punctuation is removed. Three keyword dictionaries (medical, water, shelter) are maintained, each keyword carrying a weight from 1 to 3 (for example "ambulance" = 3, "hospital" = 2, "ill" = 1). Dictionaries include Hinglish terms such as "paani", "dawai" and "ghar". The category score is the sum of the matched weights; the highest-scoring category is chosen, and messages with no match are labelled "other". The confidence is the winning score divided by the total score.

**Stage 2 – Urgency estimation.** Keyword lists for critical (e.g. "trapped", "unconscious", "not breathing"), high (e.g. "injured", "children", "urgent") and medium (e.g. "need", "shortage") cues are checked from the most to the least severe; the first level that matches is assigned, and "low" is the default. Three adjustments follow: medical requests are never below "medium"; three or more high-urgency cues escalate "high" to "critical"; and an all-capital SMS raises "low" to "medium".

**Stage 3 – Duplicate detection and flagging.** Stop words are removed from the message and its similarity to each stored ticket is computed as the larger of the Jaccard token similarity and the character-sequence ratio. A new ticket is a probable duplicate if (a) similarity ≥ 0.6 and the two locations are within 1 km (Haversine distance), or (b) the phone number is the same and similarity ≥ 0.5. The ticket is marked **flagged** (instead of **new**) when it is a probable duplicate, the category is unclear or low-confidence, or coordinates are missing. The reason is recorded.

**Human-in-the-loop.** The classifier only ever produces the statuses *new* or *flagged*. The statuses *verified* and *assigned* can be set only by the coordinator on the dashboard, so no request is dismissed or merged automatically.

**LLM-swappable design.** All classifiers implement a common `BaseClassifier.classify(text)` interface. An `LLMClassifier` can be plugged in with one call (`set_classifier`) and falls back to the rule-based classifier if the model fails, so the rest of the system is unchanged.

**Table 1: Sample requests and classifier output**

| S.No | Sample SMS request | Category | Urgency | Status |
|---|---|---|---|---|
| 1 | NEED WATER SECTOR 3 | Water | Medium | New |
| 2 | Pregnant woman in labour, need ambulance urgently | Medical | Critical | New |
| 3 | Man unconscious and bleeding heavily near bridge | Medical | Critical | New |
| 4 | Family trapped under collapsed house, please help | Shelter | Critical | New |
| 5 | Need tents and blankets for 20 people | Shelter | Medium | New |
| 6 | paani chahiye, bachche pyase hain | Water | Medium | New |
| 7 | Medicine for diabetes patient required | Medical | Medium | New |
| 8 | hello is anyone there | Other | Low | Flagged (category unclear) |
| 9 | "need water in sector 3" sent 100 m from case 1 | Water | Medium | Flagged (duplicate of #1) |

### 4.y Individual Contribution (Task 4)
My contribution to the project was the design and implementation of the classification and duplicate-detection module. I built a rule-based classifier that assigns each SMS request a category (medical, water, shelter, other) and an urgency level (low to critical) using weighted English and Hinglish keyword lists. I implemented a text-similarity and distance-based duplicate checker, and flag logic that marks uncertain or repeated requests for manual review. I structured the module around a common interface so that it can later be replaced by an LLM classifier, and wrote unit tests covering the sample requests of Table 1. I also wrote the integration guide for the backend and the literature review in Chapter 2.
