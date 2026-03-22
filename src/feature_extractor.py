"""
src/feature_extractor.py — ThreatSense
Converts a raw message into a 13-dimensional numeric feature vector
for ML training and prediction.

Features:
  0  fear_count       - number of fear keywords matched
  1  urgency_count    - number of urgency keywords matched
  2  authority_count  - number of authority keywords matched
  3  greed_count      - number of greed keywords matched
  4  trust_count      - number of trust keywords matched
  5  rule_score       - the ThreatSense weighted risk score
  6  emotion_types    - number of distinct emotion categories triggered
  7  msg_length       - character length (normalised 0-1 over 500 chars)
  8  word_count       - word count (normalised 0-1 over 100 words)
  9  caps_ratio       - proportion of UPPERCASE letters
  10 exclaim_count    - number of exclamation marks
  11 url_hint         - 1 if message contains "http", "www", or "click"
  12 question_count   - number of question marks
"""

import re
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.emotion_detector import detect_emotions
from src.risk_scorer import calculate_risk_score


def extract_features(message: str) -> list:
    """Convert a message string into a 13-element numeric feature vector."""
    emotions   = detect_emotions(message)
    score_data = calculate_risk_score(emotions)

    fear_count      = emotions["fear"]["count"]
    urgency_count   = emotions["urgency"]["count"]
    authority_count = emotions["authority"]["count"]
    greed_count     = emotions["greed"]["count"]
    trust_count     = emotions["trust"]["count"]
    rule_score      = score_data["total_score"]
    emotion_types   = len(score_data["active_emotions"])

    msg_len     = min(len(message) / 500.0, 1.0)
    word_count  = min(len(message.split()) / 100.0, 1.0)

    alpha_chars = [c for c in message if c.isalpha()]
    caps_ratio  = sum(1 for c in alpha_chars if c.isupper()) / max(len(alpha_chars), 1)

    exclaim_count  = message.count("!")
    url_hint       = 1 if re.search(r"http|www|click here|link", message, re.I) else 0
    question_count = message.count("?")

    return [
        float(fear_count), float(urgency_count), float(authority_count),
        float(greed_count), float(trust_count), float(rule_score),
        float(emotion_types), msg_len, word_count, caps_ratio,
        float(exclaim_count), float(url_hint), float(question_count),
    ]


FEATURE_NAMES = [
    "fear_count", "urgency_count", "authority_count", "greed_count",
    "trust_count", "rule_score", "emotion_types", "msg_length",
    "word_count", "caps_ratio", "exclaim_count", "url_hint", "question_count",
]


if __name__ == "__main__":
    msg   = "Your bank account is blocked. Act immediately or face legal action."
    feats = extract_features(msg)
    print("ThreatSense Feature Extractor")
    for name, val in zip(FEATURE_NAMES, feats):
        print(f"  {name:20s}: {val:.3f}")
