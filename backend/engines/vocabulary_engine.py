import re
from collections import Counter
from typing import List, Dict, Any, Tuple
from backend.models.schemas import IssueItem, ErrorCategory, ErrorSeverity

# Stopwords to exclude from repetition counts
VOCAB_STOPWORDS = {
    "the", "be", "to", "of", "and", "a", "in", "that", "have", "i", "it",
    "for", "not", "on", "with", "he", "as", "you", "do", "at", "this", "but",
    "his", "by", "from", "they", "we", "say", "her", "she", "or", "an", "will",
    "my", "one", "all", "would", "there", "their", "what", "so", "up", "out",
    "if", "about", "who", "get", "which", "go", "me", "when", "make", "can",
    "like", "time", "no", "just", "him", "know", "take", "people", "into", "year",
    "your", "could", "them", "see", "other", "than", "then", "now", "look", "only",
    "come", "its", "over", "think", "also", "back", "after", "use", "two", "how",
    "our", "work", "first", "well", "way", "even", "new", "want", "because", "any",
    "these", "give", "day", "most", "us", "is", "was", "are", "were", "been"
}

VOCAB_ENHANCEMENT_MAP = {
    "good": {
        "alternatives": ["effective", "useful", "successful", "appropriate", "valuable", "advantageous"],
        "advice": 'The adjective "good" is very generic. Depending on context, consider more precise synonyms such as "effective", "useful", "successful", or "appropriate".'
    },
    "bad": {
        "alternatives": ["suboptimal", "adverse", "detrimental", "deficient", "flawed"],
        "advice": 'Replace "bad" with more analytical adjectives such as "suboptimal", "adverse", or "detrimental".'
    },
    "important": {
        "alternatives": ["crucial", "essential", "vital", "significant", "paramount"],
        "advice": '"Important" is frequently overused. Elevate your writing with "crucial", "essential", or "significant".'
    },
    "very": {
        "alternatives": ["extremely", "considerably", "substantially", "notably"],
        "advice": '"Very" is a weak intensifier. Either remove it or replace the adjective with a stronger word.'
    },
    "big": {
        "alternatives": ["substantial", "extensive", "considerable", "prominent"],
        "advice": 'Replace the conversational word "big" with "substantial", "extensive", or "significant".'
    },
    "things": {
        "alternatives": ["aspects", "elements", "components", "factors"],
        "advice": '"Things" is vague. Specify whether you mean "factors", "aspects", or "components".'
    },
    "thing": {
        "alternatives": ["aspect", "element", "component", "factor"],
        "advice": '"Thing" is imprecise. Use terms like "aspect", "element", or "factor".'
    },
    "show": {
        "alternatives": ["demonstrate", "illustrate", "exhibit", "indicate"],
        "advice": 'Use "demonstrate" or "illustrate" in academic/professional writing instead of "show".'
    },
    "get": {
        "alternatives": ["obtain", "acquire", "receive", "derive"],
        "advice": 'In formal writing, replace "get" with "obtain", "acquire", or "receive".'
    }
}

def analyze_vocabulary(doc, raw_text: str) -> Tuple[List[IssueItem], Dict[str, Any]]:
    """
    Analyzes lexical diversity, repetitive words, and overused expressions.
    Generates intelligent synonym suggestions.
    """
    issues: List[IssueItem] = []
    issue_counter = 1
    sents_list = list(doc.sents)

    content_words = []
    lemma_positions: Dict[str, List[Tuple[int, int, int, str]]] = {} # lemma -> list of (start_idx, end_idx, sent_idx, orig_text)

    for sent_idx, sent in enumerate(sents_list):
        for token in sent:
            if not token.is_alpha or token.is_stop:
                continue
            lemma = token.lemma_.lower()
            if lemma in VOCAB_STOPWORDS or len(lemma) < 3:
                continue

            content_words.append(lemma)
            if lemma not in lemma_positions:
                lemma_positions[lemma] = []
            lemma_positions[lemma].append((token.idx, token.idx + len(token.text), sent_idx, token.text))

    counts = Counter(content_words)
    total_content_words = len(content_words)
    total_unique_words = len(counts)
    ttr = round(total_unique_words / max(1, total_content_words), 2)

    # 1. Overused words with rich synonym alternatives
    repeated_words_summary = []
    for lemma, count in counts.most_common(10):
        if count >= 3 or (lemma in VOCAB_ENHANCEMENT_MAP and count >= 2):
            alts = VOCAB_ENHANCEMENT_MAP.get(lemma, {}).get("alternatives", ["notable", "particular", "specific"])
            repeated_words_summary.append({
                "word": lemma,
                "count": count,
                "suggested_alternatives": alts
            })

            # If it has specific enhancement guidance, flag issues for occurrences beyond the first
            if lemma in VOCAB_ENHANCEMENT_MAP and count >= 2:
                info = VOCAB_ENHANCEMENT_MAP[lemma]
                # Flag the 2nd and subsequent occurrences
                for start_char, end_char, s_idx, orig_t in lemma_positions[lemma][1:]:
                    best_alt = info["alternatives"][0]
                    if orig_t.istitle():
                        best_alt = best_alt.capitalize()
                    
                    issues.append(IssueItem(
                        id=f"vocab-{issue_counter}",
                        category=ErrorCategory.VOCABULARY,
                        error_type="Overused Vocabulary",
                        start_idx=start_char,
                        end_idx=end_char,
                        sentence_idx=s_idx,
                        original_text=orig_t,
                        replacement=best_alt,
                        alternative_replacements=[
                            (a.capitalize() if orig_t.istitle() else a)
                            for a in info["alternatives"][1:4]
                        ],
                        short_message=f'Word "{orig_t}" is repeated {count} times. Consider "{best_alt}".',
                        rule_explanation=info["advice"],
                        context_snippet=sents_list[s_idx].text if s_idx < len(sents_list) else orig_t,
                        severity=ErrorSeverity.SUGGESTION
                    ))
                    issue_counter += 1

    summary = {
        "total_content_words": total_content_words,
        "unique_content_words": total_unique_words,
        "lexical_diversity_ttr": ttr,
        "repeated_words": repeated_words_summary,
        "top_frequent_words": [{"word": k, "frequency": v} for k, v in counts.most_common(8)]
    }

    return issues, summary
