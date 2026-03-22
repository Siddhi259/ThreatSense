"""
src/nlp_enhancer.py — ThreatSense
NLP enhancement layer — stopword removal + basic stemming.
Built with pure Python (zero external dependencies).
"""

STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "if", "in", "on", "at", "to",
    "for", "of", "with", "by", "from", "is", "are", "was", "were", "be",
    "been", "being", "have", "has", "had", "do", "does", "did", "will",
    "would", "could", "should", "may", "might", "shall", "can", "need",
    "i", "you", "he", "she", "it", "we", "they", "me", "him", "her",
    "us", "them", "my", "your", "his", "its", "our", "their",
    "this", "that", "these", "those", "what", "which", "who",
    "not", "no", "nor", "so", "yet", "both", "either", "each",
    "few", "more", "most", "other", "some", "such",
    "than", "then", "when", "where", "how", "all", "any",
    "just", "as", "up", "out", "about", "into", "through",
    "during", "before", "after", "above", "below", "between",
    "here", "there", "again", "once", "very", "too", "also",
}

SUFFIXES = [
    "ingly", "edly", "ness", "ment", "tion", "sion",
    "ing", "ied", "ies", "ed", "er", "ly", "al", "s",
]


def simple_stem(word: str) -> str:
    """Strip common suffixes to get approximate root form."""
    if len(word) <= 4:
        return word
    for suffix in SUFFIXES:
        if word.endswith(suffix) and len(word) - len(suffix) >= 3:
            return word[: -len(suffix)]
    return word


def remove_stopwords(tokens: list) -> list:
    """Remove common words that carry no emotional signal."""
    return [t for t in tokens if t not in STOPWORDS]


def stem_tokens(tokens: list) -> list:
    """Stem every token in a list."""
    return [simple_stem(t) for t in tokens]


def nlp_pipeline(tokens: list) -> dict:
    """
    Full ThreatSense NLP pipeline on a token list.
    Returns both filtered tokens AND stemmed tokens.
    """
    filtered = remove_stopwords(tokens)
    stemmed  = stem_tokens(filtered)
    return {
        "filtered": filtered,
        "stemmed" : stemmed,
    }


if __name__ == "__main__":
    sample_tokens = ["your", "account", "has", "been", "blocked", "act", "immediately"]
    result = nlp_pipeline(sample_tokens)
    print("ThreatSense NLP Enhancer")
    print("Filtered:", result["filtered"])
    print("Stemmed :", result["stemmed"])
