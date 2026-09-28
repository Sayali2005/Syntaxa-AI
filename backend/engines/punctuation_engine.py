import re
from typing import List, Dict, Any
from backend.models.schemas import IssueItem, ErrorCategory, ErrorSeverity

QUESTION_STARTERS = {
    "who", "what", "where", "when", "why", "how", "can", "could", "would",
    "should", "is", "are", "was", "were", "do", "does", "did", "have", "has",
    "will", "shall", "may", "might"
}

INTRODUCTORY_TRANSITIONS = {
    "however", "therefore", "furthermore", "moreover", "meanwhile",
    "nevertheless", "in conclusion", "in addition", "for example",
    "for instance", "consequently", "as a result", "firstly", "secondly", "finally"
}

GREETING_WORDS = {"hello", "hi", "hey", "dear"}

def check_punctuation(doc, raw_text: str) -> List[IssueItem]:
    """
    Detect missing terminal punctuation, question marks, introductory commas,
    capitalization issues, and excessive punctuation.
    """
    issues: List[IssueItem] = []
    issue_counter = 1

    for sent_idx, sent in enumerate(doc.sents):
        sent_text = sent.text.strip()
        if not sent_text:
            continue

        sent_start_char = sent.start_char
        sent_end_char = sent.end_char

        # 1. Capitalization at sentence start
        first_token = sent[0] if len(sent) > 0 else None
        if first_token and first_token.text and first_token.text[0].islower() and first_token.is_alpha:
            capitalized = first_token.text.capitalize()
            issues.append(IssueItem(
                id=f"punct-{issue_counter}",
                category=ErrorCategory.PUNCTUATION,
                error_type="Capitalization",
                start_idx=first_token.idx,
                end_idx=first_token.idx + len(first_token.text),
                sentence_idx=sent_idx,
                original_text=first_token.text,
                replacement=capitalized,
                alternative_replacements=[],
                short_message=f'Capitalize the first word of the sentence "{capitalized}".',
                rule_explanation='Every English sentence must begin with a capital letter.',
                context_snippet=sent.text,
                severity=ErrorSeverity.ERROR
            ))
            issue_counter += 1

        # 2. Greeting comma (e.g., "Hello how are you" -> "Hello,")
        if len(sent) >= 2:
            first_word_lower = sent[0].text.lower()
            if first_word_lower in GREETING_WORDS:
                second_token = sent[1]
                # If no comma following greeting
                if second_token.text != ",":
                    issues.append(IssueItem(
                        id=f"punct-{issue_counter}",
                        category=ErrorCategory.PUNCTUATION,
                        error_type="Missing Comma",
                        start_idx=sent[0].idx,
                        end_idx=sent[0].idx + len(sent[0].text),
                        sentence_idx=sent_idx,
                        original_text=sent[0].text,
                        replacement=f"{sent[0].text},",
                        alternative_replacements=[],
                        short_message=f'Add a comma after the greeting "{sent[0].text}".',
                        rule_explanation=f'Direct greetings like "{sent[0].text}" should be followed by a comma when addressing someone.',
                        context_snippet=sent.text,
                        severity=ErrorSeverity.SUGGESTION
                    ))
                    issue_counter += 1

        # 3. Introductory transition missing comma (e.g., "However the results were..." -> "However,")
        if len(sent) >= 2:
            w0 = sent[0].text.lower()
            w_two = (sent[0].text + " " + sent[1].text).lower() if len(sent) > 1 else ""
            if w0 in INTRODUCTORY_TRANSITIONS and sent[1].text != ",":
                issues.append(IssueItem(
                    id=f"punct-{issue_counter}",
                    category=ErrorCategory.PUNCTUATION,
                    error_type="Introductory Comma",
                    start_idx=sent[0].idx,
                    end_idx=sent[0].idx + len(sent[0].text),
                    sentence_idx=sent_idx,
                    original_text=sent[0].text,
                    replacement=f"{sent[0].text},",
                    alternative_replacements=[],
                    short_message=f'Add a comma after introductory transition "{sent[0].text}".',
                    rule_explanation=f'Introductory transitional adverbs such as "{sent[0].text}" should be set off with a comma.',
                    context_snippet=sent.text,
                    severity=ErrorSeverity.SUGGESTION
                ))
                issue_counter += 1
            elif w_two in INTRODUCTORY_TRANSITIONS and len(sent) > 2 and sent[2].text != ",":
                combined_text = sent[0].text + " " + sent[1].text
                end_pos = sent[1].idx + len(sent[1].text)
                issues.append(IssueItem(
                    id=f"punct-{issue_counter}",
                    category=ErrorCategory.PUNCTUATION,
                    error_type="Introductory Comma",
                    start_idx=sent[0].idx,
                    end_idx=end_pos,
                    sentence_idx=sent_idx,
                    original_text=combined_text,
                    replacement=f"{combined_text},",
                    alternative_replacements=[],
                    short_message=f'Add a comma after "{combined_text}".',
                    rule_explanation=f'Introductory phrases like "{combined_text}" require a comma when introducing a clause.',
                    context_snippet=sent.text,
                    severity=ErrorSeverity.SUGGESTION
                ))
                issue_counter += 1

        # 4. Missing terminal punctuation or question mark
        last_char = sent_text[-1]
        has_terminal = last_char in (".", "?", "!", '"', "'", "”")
        
        # Check if sentence is an interrogative question
        tokens_words = [t.text.lower() for t in sent if t.is_alpha]
        is_question = False
        if tokens_words:
            # Check question starter
            if tokens_words[0] in QUESTION_STARTERS:
                is_question = True
            elif len(tokens_words) > 1 and tokens_words[0] in GREETING_WORDS and tokens_words[1] in QUESTION_STARTERS:
                is_question = True

        if not has_terminal:
            target_punct = "?" if is_question else "."
            issues.append(IssueItem(
                id=f"punct-{issue_counter}",
                category=ErrorCategory.PUNCTUATION,
                error_type="Missing Terminal Punctuation",
                start_idx=sent_end_char,
                end_idx=sent_end_char,
                sentence_idx=sent_idx,
                original_text="",
                replacement=target_punct,
                alternative_replacements=[],
                short_message=f'Add a terminal mark "{target_punct}" at the end of the sentence.',
                rule_explanation=f'This sentence is {"a question" if is_question else "a declarative statement"} and should end with a {"question mark (?)" if is_question else "period (.)"}.',
                context_snippet=sent.text,
                severity=ErrorSeverity.ERROR
            ))
            issue_counter += 1
        elif last_char == "." and is_question:
            # Ends in period but is clearly a question! e.g., "How are you." -> "?"
            issues.append(IssueItem(
                id=f"punct-{issue_counter}",
                category=ErrorCategory.PUNCTUATION,
                error_type="Missing Question Mark",
                start_idx=sent_end_char - 1,
                end_idx=sent_end_char,
                sentence_idx=sent_idx,
                original_text=".",
                replacement="?",
                alternative_replacements=[],
                short_message='Replace period with a question mark "?".',
                rule_explanation='This sentence has the grammatical structure of a question and requires a question mark at the end.',
                context_snippet=sent.text,
                severity=ErrorSeverity.ERROR
            ))
            issue_counter += 1

        # 5. Excessive punctuation (e.g. "???" or "!!!!")
        for match in re.finditer(r'([!?]){2,}', sent.text):
            issues.append(IssueItem(
                id=f"punct-{issue_counter}",
                category=ErrorCategory.PUNCTUATION,
                error_type="Excessive Punctuation",
                start_idx=sent.start_char + match.start(),
                end_idx=sent.start_char + match.end(),
                sentence_idx=sent_idx,
                original_text=match.group(0),
                replacement=match.group(1),
                alternative_replacements=[],
                short_message=f'Reduce repeated punctuation "{match.group(0)}" to a single "{match.group(1)}".',
                rule_explanation='Multiple consecutive exclamation or question marks are considered informal and should be reduced to a single mark.',
                context_snippet=sent.text,
                severity=ErrorSeverity.SUGGESTION
            ))
            issue_counter += 1

    return issues
