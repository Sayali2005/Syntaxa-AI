import re
from typing import List, Set, Dict, Any
from spellchecker import SpellChecker
from backend.models.schemas import IssueItem, ErrorCategory, ErrorSeverity

# Dedicated whitelist for computer science, AI, NLP, modern tech, and academic terms
TECHNICAL_WHITELIST = {
    # Programming & Tech
    "python", "tensorflow", "pytorch", "postgresql", "mysql", "mongodb", "sqlite",
    "openai", "spacy", "nltk", "scikit", "keras", "pandas", "numpy", "matplotlib",
    "docker", "kubernetes", "devops", "github", "gitlab", "bitbucket", "linux", "ubuntu",
    "fastapi", "django", "flask", "nodejs", "react", "vue", "angular", "typescript",
    "javascript", "html", "css", "json", "yaml", "xml", "csv", "sql", "nosql", "rest",
    "graphql", "api", "apis", "sdk", "sdks", "llm", "llms", "nlp", "bert", "gpt",
    "transformer", "transformers", "gpu", "cuda", "cpu", "tpu", "dataset", "datasets",
    "hyperparameter", "hyperparameters", "tokenization", "lemmatization", "embeddings",
    "tokenizer", "tokenizers", "vectorization", "backpropagation", "lossless",
    "frontend", "backend", "fullstack", "microservices", "serverless", "middleware",
    "scalability", "auth", "oauth", "jwt", "syntaxa", "ai"
}

# Common contextual confused words / homophones
CONFUSED_WORDS = {
    "their": "there",
    "there": "their",
    "they're": "their",
    "its": "it's",
    "it's": "its",
    "affect": "effect",
    "effect": "affect",
    "loose": "lose",
    "lose": "loose",
    "accept": "except",
    "except": "accept",
    "than": "then",
    "then": "than"
}

_spell_checker = None

def get_spell_checker():
    global _spell_checker
    if _spell_checker is None:
        _spell_checker = SpellChecker()
        # Add tech terms to custom dictionary
        _spell_checker.word_frequency.load_words(list(TECHNICAL_WHITELIST))
    return _spell_checker

def check_spelling(doc, raw_text: str) -> List[IssueItem]:
    """
    Detect spelling mistakes while whitelisting technical and domain vocabulary.
    Provides smart candidate suggestions and detailed explanations.
    """
    spell = get_spell_checker()
    issues: List[IssueItem] = []
    issue_counter = 1

    for sent_idx, sent in enumerate(doc.sents):
        sent_text = sent.text
        for token in sent:
            # Skip punctuation, symbols, URLs, numbers, email addresses
            if not token.is_alpha or token.is_punct or token.is_space:
                continue

            word = token.text
            word_lower = word.lower()

            # Skip single-letter words (except 'a', 'i') or whitelisted terms
            if len(word) == 1 and word_lower in ("a", "i"):
                continue
            if len(word) == 1:
                continue

            if word_lower in TECHNICAL_WHITELIST:
                continue

            # Skip proper nouns recognized with high confidence by spaCy unless clearly misspelled
            if token.pos_ == "PROPN" and word[0].isupper() and len(word) > 2:
                # Check if it's a known proper noun or tech term
                if word_lower in spell.word_frequency or word_lower in TECHNICAL_WHITELIST:
                    continue

            # Check if word is unknown to dictionary
            if word_lower not in spell:
                correction = spell.correction(word_lower)
                if correction and correction.lower() != word_lower:
                    # Preserve capitalization
                    if word.isupper():
                        formatted_corr = correction.upper()
                    elif word.istitle():
                        formatted_corr = correction.capitalize()
                    else:
                        formatted_corr = correction

                    # Get additional candidate suggestions
                    candidates = list(spell.candidates(word_lower) or [])
                    alt_replacements = [
                        (c.capitalize() if word.istitle() else c)
                        for c in candidates if c.lower() != word_lower and c.lower() != correction.lower()
                    ][:3]

                    issues.append(IssueItem(
                        id=f"spell-{issue_counter}",
                        category=ErrorCategory.SPELLING,
                        error_type="Spelling Error",
                        start_idx=token.idx,
                        end_idx=token.idx + len(token.text),
                        sentence_idx=sent_idx,
                        original_text=token.text,
                        replacement=formatted_corr,
                        alternative_replacements=alt_replacements,
                        short_message=f'Misspelled word "{token.text}". Did you mean "{formatted_corr}"?',
                        rule_explanation=f'"{token.text}" is not recognized in the standard English vocabulary or technical dictionary. The most likely intended spelling is "{formatted_corr}".',
                        context_snippet=sent_text,
                        severity=ErrorSeverity.ERROR
                    ))
                    issue_counter += 1

    return issues
