import sys
import os
import unittest

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.main import run_full_pipeline
from backend.models.schemas import WritingMode, ErrorCategory

class TestSyntaxaAIPipeline(unittest.TestCase):

    def test_subject_verb_agreement_she_go(self):
        text = "She go to college."
        res = run_full_pipeline(text, WritingMode.GRAMMAR_FIX)
        types = [i.error_type for i in res.issues]
        repls = [i.replacement for i in res.issues]
        self.assertIn("Subject-Verb Agreement", types)
        self.assertIn("goes", repls)
        self.assertIn("She goes to college.", res.corrected_text)

    def test_subject_verb_agreement_plural_was(self):
        text = "The students was studying."
        res = run_full_pipeline(text, WritingMode.GRAMMAR_FIX)
        repls = [i.replacement for i in res.issues]
        self.assertIn("were", repls)
        self.assertIn("The students were studying.", res.corrected_text)

    def test_subject_verb_agreement_singular_were(self):
        text = "The algorithm were successful."
        res = run_full_pipeline(text, WritingMode.GRAMMAR_FIX)
        repls = [i.replacement for i in res.issues]
        self.assertIn("was", repls)
        self.assertIn("The algorithm was successful.", res.corrected_text)

    def test_verb_tense_yesterday_go(self):
        text = "Yesterday I go to college."
        res = run_full_pipeline(text, WritingMode.GRAMMAR_FIX)
        types = [i.error_type for i in res.issues]
        repls = [i.replacement for i in res.issues]
        self.assertIn("Verb Tense Inconsistency", types)
        self.assertIn("went", repls)
        self.assertIn("Yesterday I went to college.", res.corrected_text)

    def test_article_usage(self):
        text = "I bought book."
        res = run_full_pipeline(text, WritingMode.GRAMMAR_FIX)
        types = [i.error_type for i in res.issues]
        self.assertIn("Article Usage", types)
        self.assertTrue(any("book" in i.replacement for i in res.issues))

    def test_preposition_collocation_good_in(self):
        text = "He is good in mathematics."
        res = run_full_pipeline(text, WritingMode.GRAMMAR_FIX)
        preps = [i.replacement for i in res.issues if i.error_type == "Preposition Collocation"]
        self.assertIn("at", preps)
        self.assertIn("He is good at mathematics.", res.corrected_text)

    def test_singular_plural_many_student(self):
        text = "Many student were present."
        res = run_full_pipeline(text, WritingMode.GRAMMAR_FIX)
        repls = [i.replacement for i in res.issues]
        self.assertIn("students", repls)
        self.assertIn("Many students were present.", res.corrected_text)

    def test_spelling_recieved_and_tech_whitelist(self):
        text = "I recieved the assignment using Python, TensorFlow, PostgreSQL, and OpenAI."
        res = run_full_pipeline(text, WritingMode.GRAMMAR_FIX)
        spell_issues = [i for i in res.issues if i.category == ErrorCategory.SPELLING]
        spell_words = [i.original_text.lower() for i in spell_issues]
        self.assertIn("recieved", spell_words)
        # Whitelisted technical terms must not be flagged
        for tech in ["python", "tensorflow", "postgresql", "openai"]:
            self.assertNotIn(tech, spell_words)
        self.assertIn("received", [i.replacement.lower() for i in spell_issues])

    def test_punctuation_hello_how_are_you(self):
        text = "Hello how are you"
        res = run_full_pipeline(text, WritingMode.GRAMMAR_FIX)
        types = [i.error_type for i in res.issues]
        self.assertTrue(any("Comma" in t or "Punctuation" in t or "Question" in t for t in types))
        self.assertTrue(res.corrected_text.endswith("?"))

    def test_clarity_due_to_the_fact_that(self):
        text = "Due to the fact that the system was not functioning properly, the project implementation was delayed."
        res = run_full_pipeline(text, WritingMode.GRAMMAR_FIX)
        repls = [i.replacement.lower() for i in res.issues]
        self.assertIn("because", repls)
        self.assertTrue(res.corrected_text.startswith("Because"))

    def test_repetitive_passive_structure(self):
        text = "The project was developed by us and it was tested by us and it was deployed by us."
        res = run_full_pipeline(text, WritingMode.GRAMMAR_FIX)
        struct_issues = [i for i in res.issues if i.category == ErrorCategory.STRUCTURE]
        self.assertTrue(len(struct_issues) > 0)
        self.assertIn("We developed, tested, and deployed the project.", [i.replacement for i in struct_issues])

    def test_vocabulary_repeated_words(self):
        text = "This is a good method. It gives good performance and good accuracy for good models."
        res = run_full_pipeline(text, WritingMode.GRAMMAR_FIX)
        repeated = res.vocabulary_analysis.get("repeated_words", [])
        words = [r["word"] for r in repeated]
        self.assertIn("good", words)

    def test_scores_and_before_after(self):
        text = "Yesterday I go to college. Many student was interested in the topic."
        res = run_full_pipeline(text, WritingMode.GRAMMAR_FIX)
        self.assertGreater(res.scores.overall, 0)
        self.assertGreaterEqual(res.after_scores.overall, res.scores.overall)
        self.assertIn("went", res.corrected_text)
        self.assertIn("students were", res.corrected_text)

if __name__ == "__main__":
    unittest.main()
