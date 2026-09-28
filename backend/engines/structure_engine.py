import re
from typing import List, Dict, Any, Tuple
from backend.models.schemas import IssueItem, ErrorCategory, ErrorSeverity

def analyze_sentence_structure(doc, raw_text: str) -> Tuple[List[IssueItem], Dict[str, Any]]:
    """
    Detects structural issues:
    - Excessive passive construction
    - Repetitive passive coordination (e.g., "The project was developed by us and it was tested by us...")
    - Run-on sentences and overly long sentences (> 35 words)
    - Excessive conjunction chaining
    """
    issues: List[IssueItem] = []
    issue_counter = 1
    
    passive_count = 0
    total_sentences = len(list(doc.sents))
    sentence_lengths = []

    for sent_idx, sent in enumerate(doc.sents):
        sent_text = sent.text.strip()
        words = [t for t in sent if t.is_alpha]
        sentence_lengths.append(len(words))

        # 1. Detect classic coordinated passive pattern:
        # e.g., "The project was developed by us and it was tested by us and it was deployed by us."
        passive_by_us_match = re.search(
            r'\b(?:the|this)\s+([a-zA-Z]+)\s+was\s+(\w+)\s+by\s+us(?:\s+and\s+(?:it\s+was|was)\s+(\w+)\s+by\s+us)+\b',
            sent_text,
            re.IGNORECASE
        )
        if passive_by_us_match:
            # Extract all passive verbs in the sentence
            verbs_found = re.findall(r'\bwas\s+(\w+ed|\w+en|\w+t)\s+by\s+us\b', sent_text, re.IGNORECASE)
            noun_target = passive_by_us_match.group(1)
            if verbs_found:
                if len(verbs_found) == 1:
                    verbs_str = verbs_found[0]
                elif len(verbs_found) == 2:
                    verbs_str = f"{verbs_found[0]} and {verbs_found[1]}"
                else:
                    verbs_str = ", ".join(verbs_found[:-1]) + f", and {verbs_found[-1]}"
                
                suggestion = f"We {verbs_str} the {noun_target}."
                issues.append(IssueItem(
                    id=f"struct-{issue_counter}",
                    category=ErrorCategory.STRUCTURE,
                    error_type="Repetitive Passive Construction",
                    start_idx=sent.start_char,
                    end_idx=sent.end_char,
                    sentence_idx=sent_idx,
                    original_text=sent_text,
                    replacement=suggestion,
                    alternative_replacements=[],
                    short_message="Convert repetitive passive clauses into a concise active sentence.",
                    rule_explanation='Repeated passive constructions with the same agent ("by us") create redundant, heavy phrasing. Active voice ("We developed, tested, and deployed...") is significantly clearer and more impactful.',
                    context_snippet=sent_text,
                    severity=ErrorSeverity.WARNING
                ))
                issue_counter += 1
                passive_count += len(verbs_found)
                continue

        # 2. General Passive Voice Detection via spaCy dependency graph
        sent_passives = []
        for token in sent:
            if token.dep_ == "auxpass":
                parent_verb = token.head
                # Find agent 'by'
                agent = [c for c in parent_verb.children if c.dep_ == "agent" or (c.text.lower() == "by" and c.dep_ == "prep")]
                sent_passives.append((parent_verb, agent))

        if sent_passives:
            passive_count += len(sent_passives)
            # If multiple passives in a single sentence or heavy passive
            if len(sent_passives) >= 2:
                issues.append(IssueItem(
                    id=f"struct-{issue_counter}",
                    category=ErrorCategory.STRUCTURE,
                    error_type="Excessive Passive Voice",
                    start_idx=sent.start_char,
                    end_idx=sent.end_char,
                    sentence_idx=sent_idx,
                    original_text=sent_text,
                    replacement=sent_text,
                    alternative_replacements=[],
                    short_message="Multiple passive constructions detected in this sentence.",
                    rule_explanation='This sentence contains multiple passive verbs, which can obscure who is performing the action and weaken readability. Consider converting to active voice where suitable.',
                    context_snippet=sent_text,
                    severity=ErrorSeverity.SUGGESTION
                ))
                issue_counter += 1

        # 3. Overly Long / Run-on Sentence Detection
        if len(words) > 35:
            issues.append(IssueItem(
                id=f"struct-{issue_counter}",
                category=ErrorCategory.STRUCTURE,
                error_type="Long Sentence Structure",
                start_idx=sent.start_char,
                end_idx=sent.end_char,
                sentence_idx=sent_idx,
                original_text=sent_text,
                replacement=sent_text,
                alternative_replacements=[],
                short_message=f"Sentence is very long ({len(words)} words). Consider dividing it.",
                rule_explanation=f"At {len(words)} words, this sentence exceeds recommended readability thresholds (20-25 words). Splitting it into two or more sentences will improve comprehension.",
                context_snippet=sent_text,
                severity=ErrorSeverity.SUGGESTION
            ))
            issue_counter += 1

        # 4. Excessive Conjunction Chaining (e.g. 3 or more 'and's in a sentence)
        and_count = sum(1 for t in sent if t.text.lower() == "and")
        if and_count >= 3 and len(words) > 20:
            issues.append(IssueItem(
                id=f"struct-{issue_counter}",
                category=ErrorCategory.STRUCTURE,
                error_type="Conjunction Chaining",
                start_idx=sent.start_char,
                end_idx=sent.end_char,
                sentence_idx=sent_idx,
                original_text=sent_text,
                replacement=sent_text,
                alternative_replacements=[],
                short_message="Excessive use of conjunctions ('and') linking clauses.",
                rule_explanation='Chaining multiple independent ideas with repeated "and" creates a run-on feeling. Break this into distinct sentences or use bullet points.',
                context_snippet=sent_text,
                severity=ErrorSeverity.SUGGESTION
            ))
            issue_counter += 1

    summary_structure = {
        "total_passive_constructions": passive_count,
        "passive_percentage": round((passive_count / max(1, total_sentences)) * 100, 1),
        "avg_sentence_length_words": round(sum(sentence_lengths) / max(1, len(sentence_lengths)), 1) if sentence_lengths else 0,
        "longest_sentence_words": max(sentence_lengths) if sentence_lengths else 0
    }

    return issues, summary_structure
