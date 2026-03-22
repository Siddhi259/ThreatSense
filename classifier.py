"""
src/classifier.py — ThreatSense
Converts numeric risk score into HIGH / MEDIUM / LOW risk level
with a human-readable explanation and security recommendation.
"""

HIGH_THRESHOLD   = 7
MEDIUM_THRESHOLD = 4


def classify(score_data: dict) -> dict:
    """
    ThreatSense threat classifier.

    Input : output of calculate_risk_score()
    Output: {
        "risk_level"    : "HIGH" | "MEDIUM" | "LOW",
        "label_emoji"   : "🔴" | "🟡" | "🟢",
        "recommendation": "...",
        "explanation"   : "..."
    }
    """
    total  = score_data["total_score"]
    active = score_data["active_emotions"]

    if total >= HIGH_THRESHOLD:
        level = "HIGH"
        emoji = "🔴"
        recommendation = (
            "DO NOT click any links or share personal information. "
            "Report this message to your IT/security team immediately."
        )
    elif total >= MEDIUM_THRESHOLD:
        level = "MEDIUM"
        emoji = "🟡"
        recommendation = (
            "Be cautious. Verify the sender through official channels "
            "before taking any action."
        )
    else:
        level = "LOW"
        emoji = "🟢"
        recommendation = (
            "Message appears safe. Stay alert and always double-check "
            "unexpected requests."
        )

    if active:
        emotions_str = ", ".join(e.capitalize() for e in active)
        explanation  = f"Detected psychological manipulation via: {emotions_str}."
    else:
        explanation = "No significant emotional manipulation patterns found."

    return {
        "risk_level":     level,
        "label_emoji":    emoji,
        "recommendation": recommendation,
        "explanation":    explanation,
        "total_score":    total,
        "breakdown":      score_data["breakdown"],
        "active_emotions": active,
    }


if __name__ == "__main__":
    fake_score = {
        "total_score":    10,
        "breakdown":      {"fear": 6, "urgency": 2, "authority": 2, "greed": 0, "trust": 0},
        "active_emotions": ["fear", "urgency", "authority"],
    }
    result = classify(fake_score)
    print("ThreatSense Classifier")
    print(result["label_emoji"], result["risk_level"])
    print(result["explanation"])
    print(result["recommendation"])
