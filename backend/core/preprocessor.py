import spacy
from typing import Dict, Any, List, Optional
import re

_nlp_model = None

def get_spacy_model():
    """Singleton getter for spaCy model."""
    global _nlp_model
    if _nlp_model is None:
        try:
            _nlp_model = spacy.load("en_core_web_lg")
        except Exception:
            # Fallback if lg isn't available
            try:
                _nlp_model = spacy.load("en_core_web_sm")
            except Exception:
                # Blank English fallback
                _nlp_model = spacy.blank("en")
                _nlp_model.add_pipe("sentencizer")
    return _nlp_model

class PreprocessedDoc:
    def __init__(self, raw_text: str):
        self.raw_text = raw_text
        self.nlp = get_spacy_model()
        self.doc = self.nlp(raw_text)
        self.sentences = list(self.doc.sents)
        
    def get_token_annotations(self) -> List[Dict[str, Any]]:
        """Return token-level linguistic details for explainability and inspection."""
        annotations = []
        for token in self.doc:
            role = "other"
            if token.dep_ in ("nsubj", "nsubjpass"):
                role = "subject"
            elif token.dep_ in ("dobj", "pobj", "iobj"):
                role = "object"
            elif token.dep_ in ("aux", "auxpass"):
                role = "auxiliary verb"
            elif token.pos_ == "VERB" or token.dep_ == "ROOT":
                role = "main verb"
            elif token.pos_ in ("NOUN", "PROPN"):
                role = "noun"
            elif token.pos_ == "ADJ":
                role = "adjective"
            elif token.pos_ == "ADV":
                role = "adverb"

            annotations.append({
                "text": token.text,
                "lemma": token.lemma_,
                "pos": token.pos_,
                "tag": token.tag_,
                "dep": token.dep_,
                "head": token.head.text,
                "role": role,
                "idx": token.idx,
                "length": len(token.text)
            })
        return annotations

def preprocess_text(text: str) -> PreprocessedDoc:
    return PreprocessedDoc(text)
