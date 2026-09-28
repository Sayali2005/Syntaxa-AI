from typing import List, Dict, Any
from backend.models.schemas import IssueItem, ErrorCategory, QualityScore, ReadabilityMetrics

def calculate_quality_scores(
    word_count: int,
    issues: List[IssueItem],
    readability: ReadabilityMetrics,
    vocab_summary: Dict[str, Any]
) -> QualityScore:
    """
    Computes an empirical, mathematically grounded 0-100 quality score and sub-scores.
    """
    words = max(1, word_count)
    word_factor = max(1.0, words / 100.0)

    # Count issues by category
    grammar_errs = sum(1 for i in issues if i.category == ErrorCategory.GRAMMAR)
    spelling_errs = sum(1 for i in issues if i.category == ErrorCategory.SPELLING)
    punct_errs = sum(1 for i in issues if i.category == ErrorCategory.PUNCTUATION)
    clarity_errs = sum(1 for i in issues if i.category in (ErrorCategory.CLARITY, ErrorCategory.STRUCTURE))
    vocab_errs = sum(1 for i in issues if i.category == ErrorCategory.VOCABULARY)

    # Compute Sub-scores (0 - 100)
    # Grammar deduction
    g_deduction = (grammar_errs / word_factor) * 18.0
    grammar_score = int(max(20, min(100, round(100 - g_deduction))))

    # Spelling deduction
    s_deduction = (spelling_errs / word_factor) * 15.0
    spelling_score = int(max(25, min(100, round(100 - s_deduction))))

    # Punctuation deduction
    p_deduction = (punct_errs / word_factor) * 12.0
    punctuation_score = int(max(30, min(100, round(100 - p_deduction))))

    # Clarity deduction
    c_deduction = (clarity_errs / word_factor) * 10.0
    clarity_score = int(max(35, min(100, round(100 - c_deduction))))

    # Vocabulary score based on TTR and overused words
    ttr = vocab_summary.get("lexical_diversity_ttr", 0.6)
    vocab_base = 65 + (ttr * 35)
    v_deduction = (vocab_errs / word_factor) * 6.0
    vocabulary_score = int(max(30, min(100, round(vocab_base - v_deduction))))

    # Readability score: normalized around standard English readability (ease ~ 60-80 gets highest)
    ease = readability.reading_ease
    if 60 <= ease <= 85:
        r_score = 90 + ((ease - 60) / 25.0) * 10
    elif ease > 85:
        r_score = 85 + (100 - ease) * 0.5  # Slightly high reading ease
    else:
        r_score = max(40, ease * 1.3)
    readability_score = int(max(30, min(100, round(r_score))))

    # Overall weighted score
    overall = int(round(
        0.28 * grammar_score +
        0.20 * spelling_score +
        0.15 * punctuation_score +
        0.15 * clarity_score +
        0.12 * vocabulary_score +
        0.10 * readability_score
    ))
    overall = max(20, min(100, overall))

    return QualityScore(
        overall=overall,
        grammar=grammar_score,
        spelling=spelling_score,
        punctuation=punctuation_score,
        clarity=clarity_score,
        vocabulary=vocabulary_score,
        readability=readability_score
    )
