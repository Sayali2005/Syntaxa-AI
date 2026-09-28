from typing import List, Tuple
from backend.models.schemas import IssueItem

def generate_corrected_text(raw_text: str, issues: List[IssueItem]) -> str:
    """
    Applies non-overlapping suggested replacements in reverse character order,
    producing a clean, grammatically sound corrected document.
    """
    if not issues:
        return raw_text

    # Filter out empty or unchanged replacements and sort by start_idx descending
    valid_issues = [
        i for i in issues 
        if i.replacement is not None and (i.original_text != i.replacement or (i.original_text == "" and i.replacement != ""))
    ]
    # Sort descending so earlier character positions are unaffected
    valid_issues.sort(key=lambda x: (x.start_idx, x.end_idx), reverse=True)

    text_chars = list(raw_text)
    last_applied_start = len(raw_text) + 1

    for issue in valid_issues:
        start = issue.start_idx
        end = issue.end_idx

        # Prevent overlapping edits
        if end > last_applied_start:
            continue

        if 0 <= start <= end <= len(text_chars):
            text_chars[start:end] = list(issue.replacement)
            last_applied_start = start

    return "".join(text_chars)
