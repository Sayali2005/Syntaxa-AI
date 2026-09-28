from typing import List, Dict, Any
from backend.models.schemas import IssueItem

def build_educational_explanation(issue: IssueItem) -> Dict[str, Any]:
    """
    Constructs an interactive 4-part learning explanation card for an issue.
    """
    return {
        "id": issue.id,
        "what_is_wrong": issue.original_text if issue.original_text else "[Missing text]",
        "error_type": issue.error_type,
        "category": issue.category.value,
        "why_it_is_wrong": issue.rule_explanation,
        "recommended_correction": issue.replacement,
        "alternative_options": issue.alternative_replacements,
        "sentence_context": issue.context_snippet,
        "pedagogical_tip": get_pedagogical_tip(issue.error_type)
    }

def get_pedagogical_tip(error_type: str) -> str:
    tips = {
        "Subject-Verb Agreement": "Tip: Identify the core subject first. Ignore intervening prepositional phrases like 'of the students' when matching singular vs plural verbs.",
        "Verb Tense Inconsistency": "Tip: Keep verb tenses consistent within the same time frame unless there is a clear time shift indicated by an adverb or conjunction.",
        "Article Usage": "Tip: Ask yourself: is this noun countable and singular? If yes, it virtually always needs an article ('a', 'an', or 'the').",
        "Preposition Collocation": "Tip: Prepositions often form fixed collocations with specific verbs and adjectives (e.g. 'good at', 'depend on'). Memorizing these pairs enhances natural fluency.",
        "Spelling Error": "Tip: Watch out for silent letters and irregular vowel pairings ('ie' vs 'ei').",
        "Wordiness & Redundancy": "Tip: Read your sentence aloud. If a shorter word conveys identical meaning, choose the shorter word."
    }
    return tips.get(error_type, "Tip: Practice reading sentences in active voice and revising drafts to develop strong grammatical intuition.")
