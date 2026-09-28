import re
from typing import Tuple
from backend.models.schemas import LanguageInfo

# Common English function words
ENGLISH_STOPWORDS = {
    "the", "be", "to", "of", "and", "a", "in", "that", "have", "i",
    "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
    "this", "but", "his", "by", "from", "they", "we", "say", "her",
    "she", "or", "an", "will", "my", "one", "all", "would", "there",
    "their", "what", "so", "up", "out", "if", "about", "who", "get",
    "which", "go", "me", "when", "make", "can", "like", "time", "no",
    "just", "him", "know", "take", "people", "into", "year", "your",
    "good", "some", "could", "them", "see", "other", "than", "then",
    "now", "look", "only", "come", "its", "over", "think", "also",
    "back", "after", "use", "two", "how", "our", "work", "first",
    "well", "way", "even", "new", "want", "because", "any", "these",
    "give", "day", "most", "us", "is", "was", "are", "were", "been"
}

def detect_language(text: str) -> LanguageInfo:
    """
    Identifies language and confidence of the input text.
    Currently optimizes for English as the primary supported language,
    with an extensible architecture for multilingual scaling.
    """
    clean_text = text.strip()
    if not clean_text:
        return LanguageInfo(detected_language="English", confidence=1.0, is_supported=True)
    
    # Check for non-Latin scripts
    has_cjk = bool(re.search(r'[\u4e00-\u9fff\u3040-\u30ff]', clean_text))
    has_cyrillic = bool(re.search(r'[\u0400-\u04ff]', clean_text))
    has_arabic = bool(re.search(r'[\u0600-\u06ff]', clean_text))
    has_devanagari = bool(re.search(r'[\u0900-\u097f]', clean_text))
    
    if has_cjk:
        return LanguageInfo(detected_language="Chinese/Japanese", confidence=0.96, is_supported=False)
    if has_cyrillic:
        return LanguageInfo(detected_language="Russian/Cyrillic", confidence=0.95, is_supported=False)
    if has_arabic:
        return LanguageInfo(detected_language="Arabic", confidence=0.95, is_supported=False)
    if has_devanagari:
        return LanguageInfo(detected_language="Hindi/Devanagari", confidence=0.97, is_supported=False)

    # Word-level English feature analysis
    words = [w.lower() for w in re.findall(r'\b[a-zA-Z]+\b', clean_text)]
    if not words:
        return LanguageInfo(detected_language="English", confidence=0.90, is_supported=True)

    english_stopword_matches = sum(1 for w in words if w in ENGLISH_STOPWORDS)
    ratio = english_stopword_matches / len(words)

    # Spanish / French / German markers check
    romance_markers = sum(1 for w in words if w in {"el", "la", "de", "en", "y", "los", "del", "las", "por", "un", "con", "no", "una", "le", "et", "est", "que", "une", "dans", "pour", "pas", "sur", "der", "die", "und", "in", "den", "von", "zu", "das", "mit"})
    romance_ratio = romance_markers / len(words)

    if romance_ratio > 0.35 and romance_ratio > ratio:
        return LanguageInfo(detected_language="Romance/Germanic (Non-English)", confidence=0.88, is_supported=False)

    # Calculate confidence based on stopword density and latin orthography
    confidence = min(0.99, max(0.85, 0.75 + ratio * 0.5))
    return LanguageInfo(detected_language="English", confidence=round(confidence, 2), is_supported=True)
