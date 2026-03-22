"""
src/preprocessor.py — ThreatSense
Text cleaning and normalization before analysis.
"""

import re


def preprocess(text: str) -> str:
    """
    Clean and normalize input text.
    Steps:
      1. Lowercase
      2. Remove special characters (keep spaces and letters)
      3. Strip extra whitespace
    """
    if not text or not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize(text: str) -> list:
    """Split text into individual words (tokens)."""
    cleaned = preprocess(text)
    return cleaned.split()


if __name__ == "__main__":
    sample = "Your BANK account is BLOCKED! Act NOW."
    print("ThreatSense Preprocessor")
    print("Original :", sample)
    print("Cleaned  :", preprocess(sample))
    print("Tokens   :", tokenize(sample))
