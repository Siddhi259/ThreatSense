"""
src/logger.py — ThreatSense
Saves every analysis to a persistent JSON log file.
Enables history review, stats dashboard, and research export.
"""

import json
import os
from datetime import datetime

DEFAULT_LOG_PATH = os.path.join(
    os.path.dirname(__file__), "..", "data", "analysis_log.json"
)


def _load_log(path: str) -> list:
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def _save_log(entries: list, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)


def log_analysis(message: str, result: dict, log_path: str = DEFAULT_LOG_PATH) -> dict:
    """Append one ThreatSense analysis result to the log file."""
    entries = _load_log(log_path)
    entry   = {
        "id":              len(entries) + 1,
        "timestamp":       datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "message":         message,
        "risk_level":      result.get("risk_level", "UNKNOWN"),
        "risk_score":      result.get("total_score", 0),
        "active_emotions": result.get("active_emotions", []),
        "score_breakdown": result.get("breakdown", {}),
        "explanation":     result.get("explanation", ""),
    }
    entries.append(entry)
    _save_log(entries, log_path)
    return entry


def get_history(log_path: str = DEFAULT_LOG_PATH) -> list:
    """Return all ThreatSense logged entries."""
    return _load_log(log_path)


def get_stats(log_path: str = DEFAULT_LOG_PATH) -> dict:
    """Compute summary statistics over all ThreatSense logged analyses."""
    entries = _load_log(log_path)
    if not entries:
        return {"total": 0, "by_risk": {}, "top_emotions": [], "avg_score": 0.0}

    by_risk     = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    emotion_cnt = {}
    total_score = 0

    for e in entries:
        level = e.get("risk_level", "LOW")
        by_risk[level] = by_risk.get(level, 0) + 1
        total_score   += e.get("risk_score", 0)
        for emo in e.get("active_emotions", []):
            emotion_cnt[emo] = emotion_cnt.get(emo, 0) + 1

    top_emotions = sorted(emotion_cnt.items(), key=lambda x: x[1], reverse=True)

    return {
        "total":        len(entries),
        "by_risk":      by_risk,
        "top_emotions": top_emotions,
        "avg_score":    round(total_score / len(entries), 2),
    }


def clear_log(log_path: str = DEFAULT_LOG_PATH):
    """Wipe the ThreatSense log file."""
    _save_log([], log_path)
    print(f"ThreatSense log cleared: {log_path}")
