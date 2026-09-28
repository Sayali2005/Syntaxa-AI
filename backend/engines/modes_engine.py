import re
from typing import List
from backend.models.schemas import IssueItem, ErrorCategory, ErrorSeverity, WritingMode

CONTRACTIONS = {
    r"\bcan't\b": ("cannot", 'Expand contraction "can\'t" to "cannot" for professional formality.'),
    r"\bwon't\b": ("will not", 'Expand contraction "won\'t" to "will not" for professional formality.'),
    r"\bdon't\b": ("do not", 'Expand contraction "don\'t" to "do not" for formal tone.'),
    r"\bdoesn't\b": ("does not", 'Expand contraction "doesn\'t" to "does not".'),
    r"\bdidn't\b": ("did not", 'Expand contraction "didn\'t" to "did not".'),
    r"\bisn't\b": ("is not", 'Expand contraction "isn\'t" to "is not".'),
    r"\baren't\b": ("are not", 'Expand contraction "aren\'t" to "are not".'),
    r"\bwasn't\b": ("was not", 'Expand contraction "wasn\'t" to "was not".'),
    r"\bweren't\b": ("were not", 'Expand contraction "weren\'t" to "were not".'),
    r"\bhasn't\b": ("has not", 'Expand contraction "hasn\'t" to "has not".'),
    r"\bhaven't\b": ("have not", 'Expand contraction "haven\'t" to "have not".'),
    r"\bhadn't\b": ("had not", 'Expand contraction "hadn\'t" to "had not".'),
    r"\bit's\b": ("it is", 'In professional writing, expand "it\'s" to "it is" where appropriate.')
}

ACADEMIC_REPLACEMENTS = [
    (r'\ba lot of\b', 'numerous', 'Academic style favors precise quantifiers like "numerous" or "substantial" over "a lot of".'),
    (r'\bkind of\b|\bsort of\b', 'somewhat', 'Avoid colloquial hedges like "kind of" in academic writing.'),
    (r'\bhuge\b', 'substantial', 'Use formal terms like "substantial" or "extensive" instead of "huge".'),
    (r'\bstuff\b', 'materials', 'Replace vague slang "stuff" with "materials", "factors", or "data".'),
    (r'\bi think that\b', 'the evidence indicates that', 'Academic conventions avoid personal opinion markers like "I think that" in favor of objective evidence.')
]

SIMPLE_REPLACEMENTS = [
    (r'\butilize\b', 'use', 'Simplify "utilize" to "use".'),
    (r'\butilizes\b', 'uses', 'Simplify "utilizes" to "uses".'),
    (r'\bcommence\b', 'begin', 'Simplify "commence" to "begin".'),
    (r'\bfacilitate\b', 'help', 'Simplify "facilitate" to "help" or "enable".'),
    (r'\bendeavor\b', 'try', 'Simplify "endeavor" to "try".'),
    (r'\bterminate\b', 'end', 'Simplify "terminate" to "end".')
]

CONCISE_REPLACEMENTS = [
    (r'\bpast history\b', 'history', '"Past history" is redundant; history is inherently in the past.'),
    (r'\bfuture plans\b', 'plans', '"Future plans" is redundant; plans are inherently forward-looking.'),
    (r'\bend result\b', 'result', '"End result" is redundant; a result is inherently at the end.'),
    (r'\bcompletely eliminate\b', 'eliminate', '"Completely eliminate" is redundant.'),
    (r'\bvery unique\b', 'unique', 'Uniqueness is an absolute state; something cannot be "very unique".')
]

def apply_mode_transformations(mode: WritingMode, doc, issues: List[IssueItem]) -> List[IssueItem]:
    """
    Augments and filters detected issues according to the chosen writing mode.
    """
    filtered_issues = list(issues)
    issue_counter = len(issues) + 100

    if mode == WritingMode.PROFESSIONAL:
        for sent_idx, sent in enumerate(doc.sents):
            sent_text = sent.text
            for pattern, (repl, expl) in CONTRACTIONS.items():
                for match in re.finditer(pattern, sent_text, re.IGNORECASE):
                    matched = match.group(0)
                    start_char = sent.start_char + match.start()
                    end_char = sent.start_char + match.end()
                    formatted_repl = repl.capitalize() if matched.istitle() else repl
                    filtered_issues.append(IssueItem(
                        id=f"mode-{issue_counter}",
                        category=ErrorCategory.CLARITY,
                        error_type="Formal Tone (Contraction)",
                        start_idx=start_char,
                        end_idx=end_char,
                        sentence_idx=sent_idx,
                        original_text=matched,
                        replacement=formatted_repl,
                        alternative_replacements=[],
                        short_message=f'Expand contraction "{matched}" to "{formatted_repl}".',
                        rule_explanation=expl,
                        context_snippet=sent_text,
                        severity=ErrorSeverity.SUGGESTION
                    ))
                    issue_counter += 1

    elif mode == WritingMode.ACADEMIC:
        for sent_idx, sent in enumerate(doc.sents):
            sent_text = sent.text
            for pattern, repl, expl in ACADEMIC_REPLACEMENTS:
                for match in re.finditer(pattern, sent_text, re.IGNORECASE):
                    matched = match.group(0)
                    start_char = sent.start_char + match.start()
                    end_char = sent.start_char + match.end()
                    formatted_repl = repl.capitalize() if matched.istitle() else repl
                    filtered_issues.append(IssueItem(
                        id=f"mode-{issue_counter}",
                        category=ErrorCategory.VOCABULARY,
                        error_type="Academic Diction",
                        start_idx=start_char,
                        end_idx=end_char,
                        sentence_idx=sent_idx,
                        original_text=matched,
                        replacement=formatted_repl,
                        alternative_replacements=[],
                        short_message=f'Upgrade informal "{matched}" to academic "{formatted_repl}".',
                        rule_explanation=expl,
                        context_snippet=sent_text,
                        severity=ErrorSeverity.SUGGESTION
                    ))
                    issue_counter += 1

    elif mode == WritingMode.SIMPLE:
        for sent_idx, sent in enumerate(doc.sents):
            sent_text = sent.text
            for pattern, repl, expl in SIMPLE_REPLACEMENTS:
                for match in re.finditer(pattern, sent_text, re.IGNORECASE):
                    matched = match.group(0)
                    start_char = sent.start_char + match.start()
                    end_char = sent.start_char + match.end()
                    formatted_repl = repl.capitalize() if matched.istitle() else repl
                    filtered_issues.append(IssueItem(
                        id=f"mode-{issue_counter}",
                        category=ErrorCategory.CLARITY,
                        error_type="Plain Language Simplification",
                        start_idx=start_char,
                        end_idx=end_char,
                        sentence_idx=sent_idx,
                        original_text=matched,
                        replacement=formatted_repl,
                        alternative_replacements=[],
                        short_message=f'Simplify complex word "{matched}" to "{formatted_repl}".',
                        rule_explanation=expl,
                        context_snippet=sent_text,
                        severity=ErrorSeverity.SUGGESTION
                    ))
                    issue_counter += 1

    elif mode == WritingMode.CONCISE:
        for sent_idx, sent in enumerate(doc.sents):
            sent_text = sent.text
            for pattern, repl, expl in CONCISE_REPLACEMENTS:
                for match in re.finditer(pattern, sent_text, re.IGNORECASE):
                    matched = match.group(0)
                    start_char = sent.start_char + match.start()
                    end_char = sent.start_char + match.end()
                    formatted_repl = repl.capitalize() if matched.istitle() else repl
                    filtered_issues.append(IssueItem(
                        id=f"mode-{issue_counter}",
                        category=ErrorCategory.CLARITY,
                        error_type="Tautology / Redundancy",
                        start_idx=start_char,
                        end_idx=end_char,
                        sentence_idx=sent_idx,
                        original_text=matched,
                        replacement=formatted_repl,
                        alternative_replacements=[],
                        short_message=f'Eliminate redundancy "{matched}" -> "{formatted_repl}".',
                        rule_explanation=expl,
                        context_snippet=sent_text,
                        severity=ErrorSeverity.SUGGESTION
                    ))
                    issue_counter += 1

    return filtered_issues
