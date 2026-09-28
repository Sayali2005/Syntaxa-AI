import re
import textstat
from backend.models.schemas import ReadabilityMetrics

def compute_readability(raw_text: str, doc) -> ReadabilityMetrics:
    """
    Computes rigorous readability scores and audience recommendations.
    """
    clean_text = raw_text.strip()
    if not clean_text:
        return ReadabilityMetrics(
            reading_ease=100.0,
            grade_level=1.0,
            reading_level_label="Basic",
            target_audience="General Audience",
            coleman_liau=1.0,
            avg_sentence_length=0.0,
            avg_word_length=0.0,
            complex_words_count=0,
            complex_words_percentage=0.0
        )

    try:
        ease = float(textstat.flesch_reading_ease(clean_text))
        grade = float(textstat.flesch_kincaid_grade(clean_text))
        cl = float(textstat.coleman_liau_index(clean_text))
    except Exception:
        ease = 70.0
        grade = 8.0
        cl = 8.0

    # Ensure ease is bound sensibly [0, 100]
    ease_clamped = max(0.0, min(100.0, ease))

    # Determine label and audience
    if ease_clamped >= 80:
        level_label = "Easy"
        audience = "Suitable for general readers, middle school and above."
    elif ease_clamped >= 65:
        level_label = "Standard / Moderate"
        audience = "Suitable for high school and general professional audiences."
    elif ease_clamped >= 50:
        level_label = "Fairly Difficult / College-Level"
        audience = "Suitable for college-level students and academic readers."
    else:
        level_label = "Challenging / Technical"
        audience = "Suitable for specialized academics, researchers, and subject experts."

    # Average metrics
    sentences = list(doc.sents)
    num_sentences = max(1, len(sentences))
    tokens = [t for t in doc if t.is_alpha]
    num_tokens = max(1, len(tokens))

    avg_sent_len = round(num_tokens / num_sentences, 1)
    total_chars = sum(len(t.text) for t in tokens)
    avg_word_len = round(total_chars / num_tokens, 1)

    # Complex words (> 2 syllables)
    try:
        difficult_words = textstat.difficult_words(clean_text)
    except Exception:
        difficult_words = sum(1 for t in tokens if len(t.text) > 8)

    pct_complex = round((difficult_words / num_tokens) * 100, 1)

    return ReadabilityMetrics(
        reading_ease=round(ease_clamped, 1),
        grade_level=round(grade, 1),
        reading_level_label=level_label,
        target_audience=audience,
        coleman_liau=round(cl, 1),
        avg_sentence_length=avg_sent_len,
        avg_word_length=avg_word_len,
        complex_words_count=difficult_words,
        complex_words_percentage=pct_complex
    )
