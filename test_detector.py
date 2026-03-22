"""
tests/test_detector.py — ThreatSense
Unit tests for all modules. 15 tests, all should pass.
Run: python tests/test_detector.py
 or: python -m pytest tests/
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.preprocessor    import preprocess, tokenize
from src.emotion_detector import detect_emotions
from src.risk_scorer      import calculate_risk_score
from src.classifier       import classify
from main                 import analyze


# ── Preprocessor ─────────────────────────────────────────────────────────────
def test_preprocess_lowercases():
    assert preprocess("HELLO WORLD") == "hello world"

def test_preprocess_removes_symbols():
    result = preprocess("Hello! @World# $100")
    assert "@" not in result and "!" not in result

def test_preprocess_strips_whitespace():
    assert preprocess("  hello  world  ") == "hello world"

def test_tokenize_splits_words():
    tokens = tokenize("your account is blocked")
    assert "account" in tokens and "blocked" in tokens


# ── Emotion Detector ──────────────────────────────────────────────────────────
def test_detects_fear_keywords():
    result = detect_emotions("Your account is blocked due to illegal activity.")
    assert result["fear"]["detected"] is True

def test_detects_urgency():
    result = detect_emotions("Act immediately to avoid suspension.")
    assert result["urgency"]["detected"] is True

def test_detects_authority():
    result = detect_emotions("This is an official bank notice.")
    assert result["authority"]["detected"] is True

def test_detects_greed():
    result = detect_emotions("You won a free prize!")
    assert result["greed"]["detected"] is True

def test_safe_message_no_emotions():
    result = detect_emotions("Meeting is scheduled for 3pm tomorrow.")
    assert all(not info["detected"] for info in result.values())


# ── Risk Scorer ───────────────────────────────────────────────────────────────
def test_score_high_risk_message():
    result = analyze("Your bank account is blocked. Act immediately or face legal action.")
    assert result["total_score"] >= 7

def test_score_low_risk_message():
    result = analyze("See you at the meeting tomorrow.")
    assert result["total_score"] < 4

def test_score_medium_risk_message():
    result = analyze("Congratulations! You won a free prize. Claim your reward now immediately.")
    assert result["total_score"] >= 4


# ── Classifier ────────────────────────────────────────────────────────────────
def test_classify_high():
    r = classify({"total_score": 9, "breakdown": {}, "active_emotions": ["fear"]})
    assert r["risk_level"] == "HIGH"

def test_classify_medium():
    r = classify({"total_score": 5, "breakdown": {}, "active_emotions": ["urgency"]})
    assert r["risk_level"] == "MEDIUM"

def test_classify_low():
    r = classify({"total_score": 1, "breakdown": {}, "active_emotions": []})
    assert r["risk_level"] == "LOW"


if __name__ == "__main__":
    tests = [
        test_preprocess_lowercases, test_preprocess_removes_symbols,
        test_preprocess_strips_whitespace, test_tokenize_splits_words,
        test_detects_fear_keywords, test_detects_urgency,
        test_detects_authority, test_detects_greed,
        test_safe_message_no_emotions, test_score_high_risk_message,
        test_score_low_risk_message, test_score_medium_risk_message,
        test_classify_high, test_classify_medium, test_classify_low,
    ]
    passed = 0
    print("\n🛡  ThreatSense — Test Suite\n")
    for t in tests:
        try:
            t()
            print(f"  ✔ {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  ✗ {t.__name__} — {e}")
    print(f"\n  {passed}/{len(tests)} tests passed.")
    if passed == len(tests):
        print("  ✅ All tests passing — ThreatSense is ready!\n")
