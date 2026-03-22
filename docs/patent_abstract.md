# ThreatSense — Patent Abstract

## Title
ThreatSense: ThreatSense: Emotion-Based Social Engineering Attack Detection System and Method

## Abstract
A computer-implemented system and method, branded as ThreatSense, for detecting
social engineering cyber attacks by analyzing emotional manipulation patterns in
digital communications. The system receives text input, applies NLP preprocessing
(stopword removal and suffix stemming), identifies psychological trigger categories
through a weighted keyword taxonomy (Fear, Urgency, Authority, Greed, Trust),
computes a risk score using a novel weighted formula, classifies the threat level
as HIGH / MEDIUM / LOW, and outputs a natural-language security recommendation
with explainable detection rationale. An optional Machine Learning ensemble
(Random Forest + Logistic Regression) provides a second-opinion prediction with
confidence percentage.

## Claims

### Claim 1 — Core Detection Method
A computer-implemented method for detecting social engineering attacks comprising:
receiving digital text input from email, SMS, or chat; preprocessing the text;
scanning against a five-category emotion keyword dictionary; computing a weighted
risk score; classifying the threat level; generating a user warning.

### Claim 2 — Weighted Emotional Scoring System
The method of Claim 1, wherein:
  risk_score = (fear × 3) + (urgency × 2) + (authority × 2)
             + (greed × 1) + (trust × 1)

### Claim 3 — Zero-Day and Signature-Free Detection
The method of Claim 1, wherein threat detection operates independently of URL
blacklists, file attachment inspection, or known malware signatures.

### Claim 4 — Explainable Risk Output
The system of Claim 1, wherein the alert includes a natural-language explanation
of specific manipulation tactics detected and a risk-specific recommendation.

### Claim 5 — Cross-Platform Applicability
The method of Claim 1, applicable to email, SMS, instant messaging, social media,
and voice-to-text call transcripts.

## System Name
ThreatSense

## Patent Domain
Cybersecurity + Behavioral Analysis + Natural Language Processing

## Filing Jurisdiction
Indian Patent Office (IPO) — Patents Act 1970
