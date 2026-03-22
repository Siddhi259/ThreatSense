"""
src/batch_analyzer.py — ThreatSense
Batch processing — analyze a CSV file of messages all at once.

Usage:
  python -m src.batch_analyzer data/test_cases.csv
  python -m src.batch_analyzer my_emails.csv --output results/
"""

import csv
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.emotion_detector import detect_emotions
from src.risk_scorer import calculate_risk_score
from src.classifier import classify


def analyze_message(message: str) -> dict:
    """Run the full ThreatSense pipeline on one message."""
    emotions   = detect_emotions(message)
    score_data = calculate_risk_score(emotions)
    result     = classify(score_data)
    result["emotions_detail"] = emotions
    return result


def process_csv(input_path: str, output_dir: str = None) -> list:
    """Read a CSV file and run ThreatSense on every message."""
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    rows = []
    with open(input_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            msg      = row[0].strip().strip('"')
            expected = row[1].strip() if len(row) > 1 else ""
            if msg.lower() in ("message", "msg", "text"):
                continue
            rows.append((msg, expected))

    results = []
    for msg, expected in rows:
        r = analyze_message(msg)
        results.append({
            "message":        msg,
            "risk_level":     r["risk_level"],
            "risk_score":     r["total_score"],
            "active_emotions": ", ".join(r["active_emotions"]),
            "explanation":    r["explanation"],
            "expected":       expected,
            "correct":        (r["risk_level"] == expected.upper()) if expected else "N/A",
        })

    if output_dir is None:
        output_dir = os.path.dirname(input_path)
    os.makedirs(output_dir, exist_ok=True)

    timestamp  = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path   = os.path.join(output_dir, f"threatsense_results_{timestamp}.csv")
    fieldnames = ["message", "risk_level", "risk_score",
                  "active_emotions", "explanation", "expected", "correct"]

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\n✅ ThreatSense results saved → {out_path}")
    return results, out_path


def print_batch_report(results: list):
    """Print a human-readable ThreatSense batch summary."""
    total   = len(results)
    counts  = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    correct = 0
    graded  = 0

    print("\n" + "═" * 66)
    print("  🛡  THREATSENSE — BATCH ANALYSIS REPORT")
    print("═" * 66)

    for i, r in enumerate(results, 1):
        emoji = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(r["risk_level"], "⬜")
        counts[r["risk_level"]] += 1
        msg_preview = r["message"][:55] + "..." if len(r["message"]) > 55 else r["message"]

        verdict = ""
        if r["correct"] is True:
            verdict = " ✔"; correct += 1; graded += 1
        elif r["correct"] is False:
            verdict = f" ✗ (expected {r['expected']})"; graded += 1

        print(f"\n  [{i:02d}] {emoji} {r['risk_level']:6s}  Score:{r['risk_score']:3d}{verdict}")
        print(f"       {msg_preview}")
        if r["active_emotions"]:
            print(f"       Emotions: {r['active_emotions']}")

    print("\n" + "─" * 66)
    print(f"  Total messages : {total}")
    print(f"  🔴 HIGH        : {counts['HIGH']}")
    print(f"  🟡 MEDIUM      : {counts['MEDIUM']}")
    print(f"  🟢 LOW         : {counts['LOW']}")
    if graded:
        print(f"  Accuracy       : {correct}/{graded} = {(correct/graded)*100:.1f}%")
    print("═" * 66)


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "data/test_cases.csv"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "data"
    results, _ = process_csv(input_file, output_dir)
    print_batch_report(results)
