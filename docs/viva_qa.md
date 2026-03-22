# 🎓 ThreatSense — Viva Q&A Guide
## ThreatSense

---

## SECTION 1 — Project Overview

**Q1. What is ThreatSense?**
ThreatSense is an ThreatSense that
analyzes the textual content of digital messages to identify psychological
manipulation patterns. It detects social engineering attacks (phishing, smishing,
vishing) by recognizing emotional triggers — fear, urgency, authority, greed, and
trust — instead of relying on URL blacklists or malware signatures.

**Q2. Why the name ThreatSense?**
ThreatSense combines "Threat" (cyber attack) and "Sense" (detect / perceive).
The name reflects the system's ability to sense threats through psychological
pattern recognition, not technical payload inspection.

**Q3. What problem does ThreatSense solve?**
Traditional phishing tools fail against zero-day attacks because they depend on
known signatures. ThreatSense addresses this by detecting the manipulation intent
of a message, making it effective against brand-new attack campaigns that carry
no malicious link or attachment.

**Q4. What is the uniqueness of ThreatSense?**
Four key novelties:
1. Emotion-weighted scoring — asymmetric weights per psychological category
2. Pure Python NLP — zero external dependencies (no NLTK/spaCy needed)
3. Hybrid detection — rule engine + ML ensemble second opinion
4. Explainability — natural-language explanation of why a message was flagged

---

## SECTION 2 — System Architecture

**Q5. Explain the ThreatSense architecture.**
Six-stage pipeline:
1. Input Module — accepts email, SMS, or chat text
2. Preprocessor — lowercase, strip symbols, tokenize
3. NLP Enhancer — stopword removal + suffix stemming
4. Emotion Detection Engine — keyword matching across 5 categories
5. Risk Scorer — weighted formula produces numeric score
6. Classifier + Alert — maps to HIGH/MEDIUM/LOW with recommendation
Parallel: ML ensemble (RF + LR) provides second opinion with confidence %

**Q6. What is the ThreatSense risk scoring formula?**
risk_score = (fear × 3) + (urgency × 2) + (authority × 2)
           + (greed × 1) + (trust × 1)
Fear = 3 because it is the strongest psychological predictor of compliance.
Urgency and Authority = 2 because they reinforce fear. Greed and Trust = 1.

**Q7. What are the ThreatSense risk thresholds?**
Score ≥ 7  → HIGH RISK    — do not act, report immediately
Score 4–6  → MEDIUM RISK  — verify through official channels
Score ≤ 3  → LOW RISK     — likely safe

---

## SECTION 3 — NLP & Detection

**Q8. What NLP techniques does ThreatSense use?**
Three, all pure Python:
1. Tokenization — split() after preprocessing
2. Stopword removal — 80+ common function words filtered
3. Suffix stemming — strips -ing, -ed, -ion, -ly etc. so "arrested" → "arrest"

**Q9. Why no NLTK in ThreatSense?**
Zero dependencies → deployable anywhere. Custom stemmer targets manipulation
language specifically. Every line of code is explainable in the viva.

**Q10. How does ThreatSense handle multi-word phrases?**
Preprocessor rebuilds a searchable string from filtered tokens, allowing phrases
like "act now" or "limited time" to match as substrings.

---

## SECTION 4 — Machine Learning

**Q11. What ML model does ThreatSense use?**
An ensemble: Random Forest (100 trees, balanced weights) + Logistic Regression
(scaled features, L2 regularization). Final prediction averages both models'
probability outputs.

**Q12. What features does the ThreatSense ML model use?**
13 numeric features: emotion counts (5), rule score, active emotion types,
normalised message length, normalised word count, CAPS ratio, exclamation count,
URL hint indicator, question mark count.

**Q13. What accuracy does ThreatSense achieve?**
93.3% on 25% test split. 88.3% ± 6.7% on 5-fold cross-validation.
HIGH risk class: precision=1.00, recall=1.00, F1=1.00 (perfect).

**Q14. Why is the ML model a "second opinion"?**
The rule engine always runs — it needs no training data and works on zero-day
attacks from day one. The ML model adds confidence when both agree and flags
uncertainty when they disagree.

---

## SECTION 5 — Implementation

**Q15. What is the ThreatSense tech stack?**
Python 3 (core), scikit-learn (ML), Streamlit (UI), JSON/CSV/Pickle (storage),
HTML/CSS (reports), pytest (testing). No heavy infrastructure required.

**Q16. How many CLI modes does ThreatSense have?**
8 modes: interactive, --demo, --train, --evaluate, --batch, --stats,
--history, --report

**Q17. What are the 4 tabs in the ThreatSense Streamlit UI?**
Scan (single message), Batch (CSV upload), History (past scans), Stats (charts)

---

## SECTION 6 — Testing

**Q18. How was ThreatSense tested?**
1. 15 unit tests — all passing (tests/test_detector.py)
2. Batch test — 90% accuracy on 10 labeled messages
3. ML evaluation — 93.3% test accuracy, 88.3% cross-validation

---

## SECTION 7 — Patent

**Q19. Why is ThreatSense patent-worthy?**
The specific combination of: (a) five-category emotion taxonomy with asymmetric
weights, (b) zero-signature detection, and (c) explainable output is novel over
existing patents US11936686B2 and US11240266B1 which use general NLP features
without psychological weighting.

**Q20. What are the 5 ThreatSense patent claims?**
1. Emotion-category keyword matching with weighted scoring
2. The formula: fear×3 + urgency×2 + authority×2 + greed×1 + trust×1
3. Zero-signature zero-day detection
4. Explainable natural-language risk output
5. Cross-platform applicability

---

## SECTION 8 — Quick-Fire Questions

| Question | Answer |
|---|---|
| Full form of ThreatSense | Threat Detection + Sense (perceive/detect) |
| What is phishing? | Fraudulent messages tricking users |
| What is zero-day? | Attack with no known signature |
| What is tokenization? | Splitting text into words |
| What is stopword? | Common word with no emotional signal |
| What is stemming? | Reducing word to root form |
| What is Random Forest? | Ensemble of decision trees |
| What is cross-validation? | Testing accuracy across multiple splits |
| What is precision? | Of predicted HIGH, how many were actually HIGH |
| What is recall? | Of actual HIGH messages, how many did we catch |
| What is F1 score? | Harmonic mean of precision and recall |
| Why fear weight = 3? | Strongest predictor of social engineering |
| What is pickle? | Python module to save/load trained ML models |
| What is Streamlit? | Python library for web UIs without HTML/JS |
| GitHub repo name? | threatsense |
