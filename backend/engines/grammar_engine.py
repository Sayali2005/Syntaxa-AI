import re
from typing import List, Dict, Any, Optional
from backend.models.schemas import IssueItem, ErrorCategory, ErrorSeverity
import spacy

# Irregular past tense and 3rd person singular mapping
IRREGULAR_VERBS = {
    "go": {"past": "went", "3sg": "goes", "pp": "gone"},
    "do": {"past": "did", "3sg": "does", "pp": "done"},
    "have": {"past": "had", "3sg": "has", "pp": "had"},
    "be": {"past": "was/were", "3sg": "is", "pp": "been"},
    "see": {"past": "saw", "3sg": "sees", "pp": "seen"},
    "take": {"past": "took", "3sg": "takes", "pp": "taken"},
    "make": {"past": "made", "3sg": "makes", "pp": "made"},
    "get": {"past": "got", "3sg": "gets", "pp": "gotten"},
    "come": {"past": "came", "3sg": "comes", "pp": "come"},
    "write": {"past": "wrote", "3sg": "writes", "pp": "written"},
    "buy": {"past": "bought", "3sg": "buys", "pp": "bought"},
    "bring": {"past": "brought", "3sg": "brings", "pp": "brought"},
    "think": {"past": "thought", "3sg": "thinks", "pp": "thought"},
    "run": {"past": "ran", "3sg": "runs", "pp": "run"},
    "know": {"past": "knew", "3sg": "knows", "pp": "known"},
    "find": {"past": "found", "3sg": "finds", "pp": "found"},
    "give": {"past": "gave", "3sg": "gives", "pp": "given"},
    "tell": {"past": "told", "3sg": "tells", "pp": "told"},
    "become": {"past": "became", "3sg": "becomes", "pp": "become"},
    "leave": {"past": "left", "3sg": "leaves", "pp": "left"},
    "feel": {"past": "felt", "3sg": "feels", "pp": "felt"},
    "study": {"past": "studied", "3sg": "studies", "pp": "studied"},
    "develop": {"past": "developed", "3sg": "develops", "pp": "developed"},
    "test": {"past": "tested", "3sg": "tests", "pp": "tested"},
    "deploy": {"past": "deployed", "3sg": "deploys", "pp": "deployed"}
}

PAST_TIME_MARKERS = {
    "yesterday", "ago", "last night", "last week", "last month", "last year",
    "previously", "earlier", "formerly", "in the past"
}

PREPOSITION_COLLOCATIONS = [
    # (regex_pattern, incorrect_prep, correct_prep, explanation, error_type)
    (r'\b(good|bad|skilled|expert|great|terrible)\s+in\s+([a-zA-Z]+)\b', 'in', 'at', 
     'The adjective "{adj}" typically collocates with the preposition "at" when referring to ability or skill.',
     'Preposition Collocation'),
    (r'\b(interested)\s+(for|about)\b', 'for|about', 'in',
     'The adjective "interested" takes the preposition "in".',
     'Preposition Collocation'),
    (r'\b(depend|depends|depended|depending)\s+of\b', 'of', 'on',
     'The verb "depend" correctly pairs with the preposition "on" (or "upon"), not "of".',
     'Preposition Collocation'),
    (r'\b(congratulate|congratulated|congratulates)\s+(\w+)\s+for\b', 'for', 'on',
     'We congratulate someone "on" an achievement, not "for".',
     'Preposition Collocation'),
    (r'\b(responsible)\s+of\b', 'of', 'for',
     'The adjective "responsible" is followed by the preposition "for".',
     'Preposition Collocation'),
    (r'\b(comply|complies|complied)\s+to\b', 'to', 'with',
     'The verb "comply" requires the preposition "with".',
     'Preposition Collocation'),
    (r'\b(capable)\s+to\s+([a-zA-Z]+)\b', 'to', 'of',
     'The adjective "capable" is followed by "of" + gerund (e.g., "capable of doing"), not an infinitive "to".',
     'Preposition Collocation'),
    (r'\b(different)\s+(than|to)\b', 'than|to', 'from',
     'In formal and standard English, "different from" is preferred over "different than" or "different to".',
     'Preposition Collocation'),
    (r'\b(insist|insists|insisted)\s+to\b', 'to', 'on',
     'The verb "insist" takes "on" followed by a gerund or noun.',
     'Preposition Collocation')
]

COUNTABLE_SINGULAR_NOUNS = {
    "book", "car", "apple", "assignment", "project", "algorithm", "computer",
    "student", "teacher", "paper", "report", "system", "model", "problem",
    "error", "question", "sentence", "paragraph", "document",
    "machine", "test", "result", "program", "method"
}

def get_3sg_verb(lemma: str, orig_text: str) -> str:
    """Return 3rd person singular present form of a verb."""
    if lemma in IRREGULAR_VERBS and "3sg" in IRREGULAR_VERBS[lemma]:
        res = IRREGULAR_VERBS[lemma]["3sg"]
        return res.capitalize() if orig_text.istitle() else res
    if lemma.endswith(('s', 'sh', 'ch', 'x', 'z', 'o')):
        res = lemma + "es"
    elif lemma.endswith('y') and len(lemma) > 1 and lemma[-2] not in 'aeiou':
        res = lemma[:-1] + "ies"
    else:
        res = lemma + "s"
    return res.capitalize() if orig_text.istitle() else res

def get_past_verb(lemma: str, orig_text: str) -> str:
    """Return past tense form of a verb."""
    if lemma in IRREGULAR_VERBS and "past" in IRREGULAR_VERBS[lemma]:
        res = IRREGULAR_VERBS[lemma]["past"]
        return res.capitalize() if orig_text.istitle() else res
    if lemma.endswith('e'):
        res = lemma + "d"
    elif lemma.endswith('y') and len(lemma) > 1 and lemma[-2] not in 'aeiou':
        res = lemma[:-1] + "ied"
    else:
        res = lemma + "ed"
    return res.capitalize() if orig_text.istitle() else res

def get_plural_noun(lemma: str, orig_text: str) -> str:
    """Return plural form of a noun."""
    if lemma.endswith(('s', 'sh', 'ch', 'x', 'z')):
        res = lemma + "es"
    elif lemma.endswith('y') and len(lemma) > 1 and lemma[-2] not in 'aeiou':
        res = lemma[:-1] + "ies"
    else:
        res = lemma + "s"
    return res.capitalize() if orig_text.istitle() else res

def check_grammar(doc, raw_text: str) -> List[IssueItem]:
    """
    Comprehensive context-aware grammar detection across all sentences.
    Detects subject-verb agreement, verb tense, article usage, preposition collocations,
    quantifier-noun concord, and pronoun cases.
    """
    issues: List[IssueItem] = []
    issue_counter = 1

    for sent_idx, sent in enumerate(doc.sents):
        sent_text = sent.text
        sent_lower = sent_text.lower()
        
        # ----------------------------------------------------
        # 1. Temporal Adverb + Verb Tense Consistency
        # e.g., "Yesterday I go to college." -> "went"
        # ----------------------------------------------------
        has_past_marker = any(m in sent_lower for m in PAST_TIME_MARKERS)
        
        # ----------------------------------------------------
        # 2. Token-level syntactic checks
        # ----------------------------------------------------
        for token in sent:
            # A. Quantifier + Noun Concord
            # e.g., "Many student were present" -> "student" -> "students"
            if token.pos_ in ("NOUN", "PROPN") and token.tag_ == "NN":
                # Check left children or preceding token
                prev_token = doc[token.i - 1] if token.i > 0 else None
                if prev_token and prev_token.text.lower() in ("many", "several", "these", "those", "numerous", "various", "few"):
                    plural_form = get_plural_noun(token.text.lower(), token.text)
                    issues.append(IssueItem(
                        id=f"gram-{issue_counter}",
                        category=ErrorCategory.GRAMMAR,
                        error_type="Singular/Plural Agreement",
                        start_idx=token.idx,
                        end_idx=token.idx + len(token.text),
                        sentence_idx=sent_idx,
                        original_text=token.text,
                        replacement=plural_form,
                        alternative_replacements=[],
                        short_message=f'Change "{token.text}" to plural "{plural_form}" after "{prev_token.text}".',
                        rule_explanation=f'The quantifier "{prev_token.text}" must be followed by a plural countable noun. Use "{plural_form}" instead of "{token.text}".',
                        context_snippet=sent_text,
                        severity=ErrorSeverity.ERROR
                    ))
                    issue_counter += 1

            # B. Subject-Verb Agreement & Verb Tense
            if token.pos_ in ("VERB", "AUX"):
                # Find nominal subjects
                subjects = [c for c in token.children if c.dep_ in ("nsubj", "nsubjpass")]
                # If this token is an auxiliary (e.g. 'was' in 'was studying'), its subject attaches to the head verb!
                if not subjects and token.dep_ in ("aux", "auxpass") and token.head:
                    subjects = [c for c in token.head.children if c.dep_ in ("nsubj", "nsubjpass")]
                
                # Check past marker clash with present tense verb
                if has_past_marker and token.tag_ in ("VBP", "VBZ", "VB") and token.dep_ == "ROOT":
                    lemma = token.lemma_.lower()
                    past_verb = get_past_verb(lemma, token.text)
                    if past_verb.lower() != token.text.lower():
                        # Temporal adverb conflict
                        matched_marker = next(m for m in PAST_TIME_MARKERS if m in sent_lower)
                        issues.append(IssueItem(
                            id=f"gram-{issue_counter}",
                            category=ErrorCategory.GRAMMAR,
                            error_type="Verb Tense Inconsistency",
                            start_idx=token.idx,
                            end_idx=token.idx + len(token.text),
                            sentence_idx=sent_idx,
                            original_text=token.text,
                            replacement=past_verb,
                            alternative_replacements=[],
                            short_message=f'Use past tense "{past_verb}" to agree with "{matched_marker}".',
                            rule_explanation=f'The time marker "{matched_marker}" denotes an action completed in the past. The verb "{token.text}" should be in the past tense form ("{past_verb}").',
                            context_snippet=sent_text,
                            severity=ErrorSeverity.ERROR
                        ))
                        issue_counter += 1
                        continue  # Handled tense

                # Check Subject-Verb Agreement
                for subj in subjects:
                    subj_text = subj.text.lower()
                    subj_tag = subj.tag_
                    verb_text = token.text.lower()
                    
                    # Case 1: Plural subject + singular verb
                    # e.g., "The students was studying." -> "was" -> "were"
                    # "Many students was interested." -> "was" -> "were"
                    # Check if subject is plural noun or pronoun ('they', 'we')
                    is_subj_plural = (subj_tag in ("NNS", "NNPS") or 
                                      subj_text in ("they", "we", "these", "those") or
                                      any(c.dep_ == "conj" for c in subj.children))
                    
                    # Also if prev word to subject is 'many', treat intended subject as plural!
                    if not is_subj_plural and subj.i > 0 and doc[subj.i - 1].text.lower() in ("many", "several", "these", "those"):
                        is_subj_plural = True

                    if is_subj_plural:
                        if verb_text == "was":
                            repl = "were" if token.text.islower() else "Were"
                            issues.append(IssueItem(
                                id=f"gram-{issue_counter}",
                                category=ErrorCategory.GRAMMAR,
                                error_type="Subject-Verb Agreement",
                                start_idx=token.idx,
                                end_idx=token.idx + len(token.text),
                                sentence_idx=sent_idx,
                                original_text=token.text,
                                replacement=repl,
                                alternative_replacements=[],
                                short_message=f'Use plural verb "{repl}" with plural subject "{subj.text}".',
                                rule_explanation=f'The subject "{subj.text}" is plural, which requires the plural past verb "{repl}" instead of the singular "{token.text}".',
                                context_snippet=sent_text,
                                severity=ErrorSeverity.ERROR
                            ))
                            issue_counter += 1
                        elif verb_text == "is":
                            repl = "are" if token.text.islower() else "Are"
                            issues.append(IssueItem(
                                id=f"gram-{issue_counter}",
                                category=ErrorCategory.GRAMMAR,
                                error_type="Subject-Verb Agreement",
                                start_idx=token.idx,
                                end_idx=token.idx + len(token.text),
                                sentence_idx=sent_idx,
                                original_text=token.text,
                                replacement=repl,
                                alternative_replacements=[],
                                short_message=f'Use plural verb "{repl}" with plural subject "{subj.text}".',
                                rule_explanation=f'The subject "{subj.text}" is plural, requiring the plural verb "{repl}" rather than "{token.text}".',
                                context_snippet=sent_text,
                                severity=ErrorSeverity.ERROR
                            ))
                            issue_counter += 1
                        elif verb_text == "has":
                            repl = "have" if token.text.islower() else "Have"
                            issues.append(IssueItem(
                                id=f"gram-{issue_counter}",
                                category=ErrorCategory.GRAMMAR,
                                error_type="Subject-Verb Agreement",
                                start_idx=token.idx,
                                end_idx=token.idx + len(token.text),
                                sentence_idx=sent_idx,
                                original_text=token.text,
                                replacement=repl,
                                alternative_replacements=[],
                                short_message=f'Use plural verb "{repl}" with plural subject "{subj.text}".',
                                rule_explanation=f'The plural subject "{subj.text}" takes "{repl}" instead of 3rd-person singular "{token.text}".',
                                context_snippet=sent_text,
                                severity=ErrorSeverity.ERROR
                            ))
                            issue_counter += 1
                        elif token.tag_ == "VBZ":
                            # e.g., "The students goes" -> "go"
                            repl = token.lemma_ if token.text.islower() else token.lemma_.capitalize()
                            issues.append(IssueItem(
                                id=f"gram-{issue_counter}",
                                category=ErrorCategory.GRAMMAR,
                                error_type="Subject-Verb Agreement",
                                start_idx=token.idx,
                                end_idx=token.idx + len(token.text),
                                sentence_idx=sent_idx,
                                original_text=token.text,
                                replacement=repl,
                                alternative_replacements=[],
                                short_message=f'Use base plural verb "{repl}" with plural subject "{subj.text}".',
                                rule_explanation=f'Plural subjects require the base form "{repl}" rather than the singular verb ending "-s" / "{token.text}".',
                                context_snippet=sent_text,
                                severity=ErrorSeverity.ERROR
                            ))
                            issue_counter += 1

                    # Case 2: Singular 3rd-person subject + plural / base verb
                    # e.g., "She go to college." -> "goes"
                    # "The algorithm were successful." -> "were" -> "was"
                    # "He have" -> "has", "He do" -> "does"
                    has_plural_quantifier = (subj.i > 0 and doc[subj.i - 1].text.lower() in ("many", "several", "these", "those", "numerous", "various", "few", "two", "three"))
                    is_subj_3sg = (subj_tag in ("NN", "NNP") or subj_text in ("he", "she", "it", "this", "that"))
                    if is_subj_3sg and not has_plural_quantifier and not any(c.dep_ == "conj" for c in subj.children):
                        if verb_text == "were":
                            repl = "was" if token.text.islower() else "Was"
                            issues.append(IssueItem(
                                id=f"gram-{issue_counter}",
                                category=ErrorCategory.GRAMMAR,
                                error_type="Subject-Verb Agreement",
                                start_idx=token.idx,
                                end_idx=token.idx + len(token.text),
                                sentence_idx=sent_idx,
                                original_text=token.text,
                                replacement=repl,
                                alternative_replacements=[],
                                short_message=f'Use singular verb "{repl}" with singular subject "{subj.text}".',
                                rule_explanation=f'"{subj.text}" is a singular noun/pronoun, so the singular verb "{repl}" is required rather than the plural "{token.text}".',
                                context_snippet=sent_text,
                                severity=ErrorSeverity.ERROR
                            ))
                            issue_counter += 1
                        elif token.tag_ == "VBP" and subj_text != "i" and subj_text != "you":
                            # e.g., "She go" -> "She goes"
                            repl = get_3sg_verb(token.lemma_.lower(), token.text)
                            if repl.lower() != token.text.lower():
                                issues.append(IssueItem(
                                    id=f"gram-{issue_counter}",
                                    category=ErrorCategory.GRAMMAR,
                                    error_type="Subject-Verb Agreement",
                                    start_idx=token.idx,
                                    end_idx=token.idx + len(token.text),
                                    sentence_idx=sent_idx,
                                    original_text=token.text,
                                    replacement=repl,
                                    alternative_replacements=[],
                                    short_message=f'Use 3rd-person singular "{repl}" with subject "{subj.text}".',
                                    rule_explanation=f'Third-person singular subjects ("{subj.text}") take verbs ending in -s or -es ("{repl}") in the present tense.',
                                    context_snippet=sent_text,
                                    severity=ErrorSeverity.ERROR
                                ))
                                issue_counter += 1

            # C. Article Usage (Missing article before singular countable noun)
            # e.g., "I bought book." -> "bought a book" or "bought the book"
            if token.pos_ == "NOUN" and token.tag_ == "NN" and token.dep_ in ("dobj", "attr"):
                if token.text.lower() in COUNTABLE_SINGULAR_NOUNS:
                    # Check if token has a determiner or possessive modifier
                    has_det = any(c.dep_ in ("det", "poss") for c in token.children)
                    if not has_det:
                        first_letter = token.text.lower()[0]
                        art = "an" if first_letter in "aeiou" and not token.text.lower().startswith("uni") else "a"
                        repl = f"{art} {token.text}"
                        issues.append(IssueItem(
                            id=f"gram-{issue_counter}",
                            category=ErrorCategory.GRAMMAR,
                            error_type="Article Usage",
                            start_idx=token.idx,
                            end_idx=token.idx + len(token.text),
                            sentence_idx=sent_idx,
                            original_text=token.text,
                            replacement=repl,
                            alternative_replacements=[f"the {token.text}"],
                            short_message=f'Add an article before countable noun "{token.text}".',
                            rule_explanation=f'Singular countable nouns like "{token.text}" usually require a determiner such as "{art}" or "the".',
                            context_snippet=sent_text,
                            severity=ErrorSeverity.ERROR
                        ))
                        issue_counter += 1

            # D. Article Sound Mismatch (a vs an)
            # e.g., "a apple" -> "an apple", "an car" -> "a car"
            if token.text.lower() in ("a", "an"):
                next_token = doc[token.i + 1] if token.i + 1 < len(doc) else None
                if next_token and next_token.pos_ in ("NOUN", "ADJ", "ADV"):
                    target_word = next_token.text.lower()
                    first_char = target_word[0]
                    
                    # Exceptions: 'university', 'unique', 'euro' take 'a'; 'hour', 'honor' take 'an'
                    is_vowel_sound = (first_char in "aeiou")
                    if target_word.startswith(("uni", "use", "user", "one", "euro", "eul")):
                        is_vowel_sound = False
                    elif target_word.startswith(("hour", "honest", "honor")):
                        is_vowel_sound = True

                    if token.text.lower() == "a" and is_vowel_sound:
                        repl = "an" if token.text.islower() else "An"
                        issues.append(IssueItem(
                            id=f"gram-{issue_counter}",
                            category=ErrorCategory.GRAMMAR,
                            error_type="Article Usage (a/an)",
                            start_idx=token.idx,
                            end_idx=token.idx + len(token.text),
                            sentence_idx=sent_idx,
                            original_text=token.text,
                            replacement=repl,
                            alternative_replacements=[],
                            short_message=f'Use "{repl}" before vowel sound in "{next_token.text}".',
                            rule_explanation=f'The indefinite article "an" must be used before words beginning with a vowel sound ("{next_token.text}").',
                            context_snippet=sent_text,
                            severity=ErrorSeverity.ERROR
                        ))
                        issue_counter += 1
                    elif token.text.lower() == "an" and not is_vowel_sound:
                        repl = "a" if token.text.islower() else "A"
                        issues.append(IssueItem(
                            id=f"gram-{issue_counter}",
                            category=ErrorCategory.GRAMMAR,
                            error_type="Article Usage (a/an)",
                            start_idx=token.idx,
                            end_idx=token.idx + len(token.text),
                            sentence_idx=sent_idx,
                            original_text=token.text,
                            replacement=repl,
                            alternative_replacements=[],
                            short_message=f'Use "{repl}" before consonant sound in "{next_token.text}".',
                            rule_explanation=f'The indefinite article "a" must be used before words beginning with a consonant sound ("{next_token.text}").',
                            context_snippet=sent_text,
                            severity=ErrorSeverity.ERROR
                        ))
                        issue_counter += 1

        # ----------------------------------------------------
        # 3. Regex Preposition Collocation Checks
        # e.g., "He is good in mathematics." -> "good at"
        # ----------------------------------------------------
        for pattern, incorrect_prep, correct_prep, explanation_tmpl, error_type in PREPOSITION_COLLOCATIONS:
            for match in re.finditer(pattern, sent_text, re.IGNORECASE):
                full_matched = match.group(0)
                # Find exact position of incorrect preposition within the match
                prep_match = re.search(r'\b(' + incorrect_prep + r')\b', full_matched, re.IGNORECASE)
                if prep_match:
                    start_pos = sent.start_char + match.start() + prep_match.start()
                    end_pos = start_pos + len(prep_match.group(0))
                    orig_prep = prep_match.group(0)
                    adj_match = match.group(1) if match.groups() else ""
                    explanation = explanation_tmpl.replace("{adj}", adj_match)
                    
                    issues.append(IssueItem(
                        id=f"gram-{issue_counter}",
                        category=ErrorCategory.GRAMMAR,
                        error_type=error_type,
                        start_idx=start_pos,
                        end_idx=end_pos,
                        sentence_idx=sent_idx,
                        original_text=orig_prep,
                        replacement=correct_prep,
                        alternative_replacements=[],
                        short_message=f'Change "{orig_prep}" to "{correct_prep}".',
                        rule_explanation=explanation,
                        context_snippet=sent_text,
                        severity=ErrorSeverity.ERROR
                    ))
                    issue_counter += 1

    return issues
