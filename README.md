<div align="center">

# 🛡 ThreatSense

### Emotion-Aware Social Engineering Attack Detection System

*Detecting cyber threats through psychological manipulation patterns in digital messages*

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red?style=flat-square)
![Accuracy](https://img.shields.io/badge/ML_Accuracy-93.3%25-brightgreen?style=flat-square)
![Tests](https://img.shields.io/badge/Tests-15%2F15_passing-brightgreen?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)

**Final Year Project | Computer Science & Engineering | 2025–2026**

</div>

---

## 📌 What is ThreatSense?

ThreatSense detects social engineering cyber attacks — phishing emails, SMS scams, fraudulent messages — by analyzing **psychological manipulation patterns** in text. Unlike traditional tools that rely on URL blacklists or malware signatures, ThreatSense detects the **human psychology being exploited**: fear, urgency, authority, greed, and trust.

> **Zero-day safe** — no signatures needed. If a message manipulates emotions, ThreatSense catches it.

---

## 🎯 Key Features

| Feature | Description |
|---|---|
| 🧠 5-Category Emotion Engine | Detects Fear, Urgency, Authority, Greed, Trust |
| 📐 Weighted Risk Formula | `(fear×3) + (urgency×2) + (authority×2) + (greed×1) + (trust×1)` |
| 🤖 ML Ensemble | Random Forest + Logistic Regression — 93.3% accuracy |
| 🔤 Pure Python NLP | Stopword removal + stemming, zero external dependencies |
| 🌐 Web Dashboard | 4-tab Streamlit interface: Scan, Batch, History, Stats |
| 💻 CLI Tool | 8 operating modes |
| 📂 Batch Analyzer | Process CSV files of messages |
| 📜 HTML Reports | Self-contained downloadable analysis reports |
| 🗂 Analysis Logger | Persistent JSON history of all scans |

---

## 📁 Project Structure

```
threatsense/
├── main.py                    ← CLI entry point (8 modes)
├── app.py                     ← Streamlit web UI (4 tabs)
├── requirements.txt
├── .gitignore
│
├── src/
│   ├── preprocessor.py        ← Lowercase, remove symbols, tokenize
│   ├── nlp_enhancer.py        ← Stopword removal + suffix stemming
│   ├── emotion_detector.py    ← 5-category keyword emotion engine
│   ├── risk_scorer.py         ← Weighted risk score formula
│   ├── classifier.py          ← HIGH / MEDIUM / LOW + recommendation
│   ├── feature_extractor.py   ← 13-feature vector for ML
│   ├── ml_model.py            ← RF + LR ensemble (93.3% accuracy)
│   ├── batch_analyzer.py      ← CSV batch processing
│   ├── logger.py              ← Persistent JSON analysis log
│   └── report_generator.py   ← HTML report export
│
├── data/
│   ├── keywords.json          ← Emotion keyword dictionary + weights
│   ├── training_data.json     ← 60 labeled training samples
│   └── test_cases.csv         ← 10 labeled test messages
│
├── tests/
│   └── test_detector.py       ← 15 unit tests
│
└── docs/
    ├── patent_abstract.md     ← Patent draft with 5 claims
    └── viva_qa.md             ← 25 viva Q&As across 8 sections
```

---

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/YOUR-USERNAME/threatsense.git
cd threatsense

# 2. Install dependencies
pip install -r requirements.txt

# 3. Train the ML model (first time only)
python main.py --train

# 4. Run demo
python main.py --demo

# 5. Launch web UI
streamlit run app.py
```

---

## 🧠 How ThreatSense Works

```
User Message
     ↓
Preprocessor         → lowercase, remove symbols, tokenize
     ↓
NLP Enhancer         → stopword removal + suffix stemming
     ↓
Emotion Detection    → fear / urgency / authority / greed / trust
     ↓
Risk Scoring         → (fear×3) + (urgency×2) + (authority×2) + (greed×1) + (trust×1)
     ↓
Classification       → ≥7 HIGH  |  4–6 MEDIUM  |  ≤3 LOW
     ↓
ML Second Opinion    → RF + LR ensemble (93.3% accuracy)
     ↓
Alert + Explanation + Recommendation
```

---

## 💻 CLI Commands

```bash
python main.py                          # Interactive mode
python main.py --demo                   # 5 built-in sample messages
python main.py --train                  # Train ML model
python main.py --evaluate               # ML accuracy report
python main.py --batch data/test_cases.csv   # Batch CSV analysis
python main.py --stats                  # Aggregate stats from log
python main.py --history 20             # Last 20 scans
python main.py --report "Your message"  # Analyze + save HTML report
```

---

## 🌐 Web UI Tabs

| Tab | Feature |
|---|---|
| 🔍 Scan | Single message analyzer with emotion badges and score chart |
| 📂 Batch | Upload CSV → analyze all messages with risk summary |
| 📜 History | All past scans with timestamps and risk levels |
| 📊 Stats | Charts: HIGH/MEDIUM/LOW breakdown, top detected emotions |

---

## 📊 Results

| Metric | Value |
|---|---|
| Unit tests | ✅ 15 / 15 passing |
| ML test-set accuracy | **93.3%** |
| ML cross-validation | 88.3% ± 6.7% |
| HIGH risk precision | **1.00** (perfect) |
| HIGH risk recall | **1.00** (perfect) |
| Batch test accuracy | 90% (9/10) |

---

## 🧪 Sample Output

```
🛡 ThreatSense

Message: Your bank account is blocked. Act immediately or face legal action.

🔴 RISK LEVEL : HIGH
📊 RISK SCORE : 13

🧠 Emotion Analysis:
   ✔ Fear       | matched: ['blocked', 'legal']
   ✔ Urgency    | matched: ['immediately']
   ✔ Authority  | matched: ['bank']
   ✗ Greed      | not detected

💡 Detected psychological manipulation via: Fear, Urgency, Authority.
🛡  DO NOT click any links or share personal information.
🤖 ML Second Opinion : HIGH  (86% confidence)  [✔ agrees]
```

---

## 📜 Patent

**Title:** ThreatSense: Emotion-Based Social Engineering Attack Detection System and Method

**Domain:** Cybersecurity + Behavioral Analysis + NLP

**5 Key Claims:**
1. Emotion-category keyword matching with asymmetric weighted scoring
2. Risk formula: `(fear×3) + (urgency×2) + (authority×2) + (greed×1) + (trust×1)`
3. Zero-signature detection — no URL blacklists, no file scanning needed
4. Explainable natural-language risk output
5. Cross-platform (email, SMS, chat, voice-to-text)

See [`docs/patent_abstract.md`](docs/patent_abstract.md)

---

## 🎓 Viva Prep

[`docs/viva_qa.md`](docs/viva_qa.md) — 25 Q&As across 8 sections covering architecture, NLP, ML, testing, future scope, and patent claims.

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.x |
| ML | scikit-learn (Random Forest, Logistic Regression) |
| NLP | Pure Python — no NLTK or spaCy needed |
| UI | Streamlit |
| Storage | JSON / CSV / Pickle |
| Testing | pytest |
| Reports | Self-contained HTML |

---

## 📄 License

MIT License — see [LICENSE](LICENSE)

---

<div align="center">

**🛡 ThreatSense** &nbsp;·&nbsp; Final Year Project &nbsp;·&nbsp; CSE 2025–2026  
*Built by Siddhi Dhus*

</div>
