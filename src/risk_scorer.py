"""
src/risk_scorer.py — ThreatSense
Calculates the weighted risk score from detected emotions.

ThreatSense Risk Formula (patent-claim material):
  risk_score = (fear_count × 3) + (urgency_count × 2)
             + (authority_count × 2) + (greed_count × 1)
             + (trust_count × 1)
"""


def calculate_risk_score(emotion_results: dict) -> dict:
    """
    Compute ThreatSense weighted risk score from emotion detection results.

    Returns:
    {
        "total_score"   : 9,
        "breakdown"     : {"fear": 6, "urgency": 2, "authority": 2, ...},
        "active_emotions": ["fear", "urgency", "authority"]
    }
    """
    breakdown = {}
    total     = 0
    active    = []

    for emotion, info in emotion_results.items():
        contribution      = info["count"] * info["weight"]
        breakdown[emotion] = contribution
        total             += contribution
        if info["detected"]:
            active.append(emotion)

    return {
        "total_score":     total,
        "breakdown":       breakdown,
        "active_emotions": active,
    }


if __name__ == "__main__":
    fake_emotions = {
        "fear":      {"detected": True,  "count": 2, "weight": 3, "matched": ["blocked", "illegal"]},
        "urgency":   {"detected": True,  "count": 1, "weight": 2, "matched": ["immediately"]},
        "authority": {"detected": True,  "count": 1, "weight": 2, "matched": ["bank"]},
        "greed":     {"detected": False, "count": 0, "weight": 1, "matched": []},
        "trust":     {"detected": False, "count": 0, "weight": 1, "matched": []},
    }
    score = calculate_risk_score(fake_emotions)
    print("ThreatSense Risk Scorer")
    print("Score :", score["total_score"])
    print("Active:", score["active_emotions"])
