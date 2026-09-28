import re
from typing import List, Tuple
from backend.models.schemas import IssueItem, ErrorCategory, ErrorSeverity

# List of (phrase_pattern, replacement, explanation, error_type)
CLARITY_RULES = [
    (
        r'\bdue to the fact that\b',
        'because',
        '"Due to the fact that" is wordy and bureaucratic. Replacing it with "because" makes your sentence direct and easy to read.',
        'Wordiness & Redundancy'
    ),
    (
        r'\bin order to\b',
        'to',
        '"In order to" can almost always be simplified to "to" without losing any meaning.',
        'Wordiness & Redundancy'
    ),
    (
        r'\bfor the purpose of\b',
        'for',
        '"For the purpose of" is needlessly verbose. Use "for" or "to".',
        'Wordiness & Redundancy'
    ),
    (
        r'\bat the present time\b|\bat this point in time\b',
        'currently',
        'Use "currently" or "now" instead of lengthy temporal fillers.',
        'Clarity & Directness'
    ),
    (
        r'\bin the event that\b',
        'if',
        '"In the event that" adds unnecessary words; "if" conveys the exact conditional meaning.',
        'Clarity & Directness'
    ),
    (
        r'\bhas the ability to\b|\bhave the ability to\b',
        'can',
        '"Has the ability to" is wordy; "can" is crisp and direct.',
        'Nominalization / Verbosity'
    ),
    (
        r'\bmake a decision\b',
        'decide',
        'Nominalization: replace the noun phrase "make a decision" with the dynamic verb "decide".',
        'Nominalization'
    ),
    (
        r'\btake into consideration\b|\bgive consideration to\b',
        'consider',
        'Convert the noun phrase "take into consideration" into the active verb "consider".',
        'Nominalization'
    ),
    (
        r'\bconduct an investigation into\b',
        'investigate',
        'Replace "conduct an investigation into" with the concise verb "investigate".',
        'Nominalization'
    ),
    (
        r'\bis an indication of\b|\bare an indication of\b',
        'indicates',
        'Use the strong verb "indicates" instead of the noun construction "is an indication of".',
        'Nominalization'
    ),
    (
        r'\bdespite the fact that\b|\bin spite of the fact that\b',
        'although',
        'Replace wordy clauses with "although" or "even though".',
        'Wordiness & Redundancy'
    ),
    (
        r'\buntil such time as\b',
        'until',
        '"Until such time as" is archaic legalistic phrasing; replace with "until".',
        'Archaic Phrasing'
    ),
    (
        r'\ba large number of\b|\ba significant number of\b',
        'many',
        'Simplify "a large number of" to "many" or "numerous".',
        'Wordiness & Redundancy'
    ),
    (
        r'\bin close proximity to\b',
        'near',
        'Use "near" or "close to" rather than the verbose "in close proximity to".',
        'Wordiness & Redundancy'
    ),
    (
        r'\ba majority of\b',
        'most',
        'Replace "a majority of" with "most" for greater clarity.',
        'Wordiness & Redundancy'
    ),
    (
        r'\bas a consequence of\b',
        'because of',
        'Use "because of" or "due to" instead of "as a consequence of".',
        'Wordiness & Redundancy'
    ),
    (
        r'\bwith reference to\b|\bwith regard to\b',
        'regarding',
        'Replace "with reference to" with "regarding" or "about".',
        'Clarity & Directness'
    ),
    (
        r'\bit is important to note that\b',
        'notably,',
        '"It is important to note that" is an empty filler phrase. Start directly with the main idea or use "notably".',
        'Filler Phrase'
    ),
    (
        r'\bneedless to say\b',
        '',
        'If something is truly needless to say, omitting the phrase strengthens the sentence.',
        'Filler Phrase'
    )
]

def check_clarity(doc, raw_text: str) -> List[IssueItem]:
    """
    Detect wordiness, bureaucratic expressions, nominalizations, and filler phrases.
    Suggests concise, dynamic alternatives.
    """
    issues: List[IssueItem] = []
    issue_counter = 1

    for sent_idx, sent in enumerate(doc.sents):
        sent_text = sent.text
        for pattern, replacement, explanation, error_type in CLARITY_RULES:
            for match in re.finditer(pattern, sent_text, re.IGNORECASE):
                matched_text = match.group(0)
                start_char = sent.start_char + match.start()
                end_char = sent.start_char + match.end()
                
                # Preserve capitalization of first word if needed
                formatted_replacement = replacement
                if matched_text and matched_text[0].isupper() and replacement:
                    formatted_replacement = replacement[0].upper() + replacement[1:]

                issues.append(IssueItem(
                    id=f"clarity-{issue_counter}",
                    category=ErrorCategory.CLARITY,
                    error_type=error_type,
                    start_idx=start_char,
                    end_idx=end_char,
                    sentence_idx=sent_idx,
                    original_text=matched_text,
                    replacement=formatted_replacement,
                    alternative_replacements=[],
                    short_message=f'Simplify "{matched_text}" to "{formatted_replacement}".' if formatted_replacement else f'Remove filler phrase "{matched_text}".',
                    rule_explanation=explanation,
                    context_snippet=sent_text,
                    severity=ErrorSeverity.SUGGESTION
                ))
                issue_counter += 1

    return issues
