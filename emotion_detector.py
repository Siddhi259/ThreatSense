"""
src/emotion_detector.py — ThreatSense
Core engine that scans a message for emotional manipulation signals.
Enhanced with NLP preprocessing (stopword removal + stemming).
"""

import json
import os
from src.preprocessor import preprocess, tokenize
from src.nlp_enhancer import nlp_pipeline, simple_stem

KEYWORDS_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "keywords.json")

with open(KEYWORDS_PATH, "r") as f:
    EMOTION_KEYWORDS = json.load(f)

_STEMMED_KEYWORDS = {}
for _emo, _data in EMOTION_KEYWORDS.items():
    _STEMMED_KEYWORDS[_emo] = [simple_stem(kw) for kw in _data["keywords"]]


def detect_emotions(message: str, use_nlp: bool = True) -> dict:
    """
    ThreatSense emotion detection engine.
    Scans message for each of 5 psychological manipulation categories.

    Parameters
    ----------
    message  : raw input text
    use_nlp  : apply stopword removal + stemming before matching

    Returns
    -------
    dict  {emotion: {detected, matched, count, weight}}
    """
    cleaned = preprocess(message)

    if use_nlp:
        tokens  = tokenize(cleaned)
        nlp_out = nlp_pipeline(tokens)
        stemmed_text = " ".join(nlp_out["stemmed"])
        plain_text   = " ".join(nlp_out["filtered"])
    else:
        stemmed_text = cleaned
        plain_text   = cleaned

    results = {}
    for emotion, data in EMOTION_KEYWORDS.items():
        matched     = []
        stem_kws    = _STEMMED_KEYWORDS[emotion]
        orig_kws    = data["keywords"]

        for orig_kw, stem_kw in zip(orig_kws, stem_kws):
            if orig_kw in plain_text or stem_kw in stemmed_text:
                if orig_kw not in matched:
                    matched.append(orig_kw)

        results[emotion] = {
            "detected": len(matched) > 0,
            "matched":  matched,
            "count":    len(matched),
            "weight":   data["weight"],
        }

    return results


if __name__ == "__main__":
    test_msg = "Your bank account is blocked. Act immediately or face legal action."
    print("ThreatSense Emotion Detector")
    result = detect_emotions(test_msg)
    for emotion, info in result.items():
        if info["detected"]:
            print(f"[{emotion.upper()}] matched: {info['matched']}")
