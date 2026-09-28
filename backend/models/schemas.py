from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class WritingMode(str, Enum):
    GRAMMAR_FIX = "grammar_fix"
    PROFESSIONAL = "professional"
    ACADEMIC = "academic"
    SIMPLE = "simple"
    CONCISE = "concise"

class ErrorCategory(str, Enum):
    GRAMMAR = "grammar"
    SPELLING = "spelling"
    PUNCTUATION = "punctuation"
    CLARITY = "clarity"
    VOCABULARY = "vocabulary"
    STRUCTURE = "structure"

class ErrorSeverity(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    SUGGESTION = "suggestion"

class IssueItem(BaseModel):
    id: str
    category: ErrorCategory
    error_type: str
    start_idx: int
    end_idx: int
    sentence_idx: int
    original_text: str
    replacement: str
    alternative_replacements: List[str] = []
    short_message: str
    rule_explanation: str
    context_snippet: str
    severity: ErrorSeverity = ErrorSeverity.ERROR

class ReadabilityMetrics(BaseModel):
    reading_ease: float
    grade_level: float
    reading_level_label: str
    target_audience: str
    coleman_liau: float
    avg_sentence_length: float
    avg_word_length: float
    complex_words_count: int
    complex_words_percentage: float

class QualityScore(BaseModel):
    overall: int
    grammar: int
    spelling: int
    punctuation: int
    clarity: int
    vocabulary: int
    readability: int

class DocumentStats(BaseModel):
    character_count: int
    word_count: int
    sentence_count: int
    paragraph_count: int
    section_count: int
    estimated_reading_time_min: float
    estimated_speaking_time_min: float

class LanguageInfo(BaseModel):
    detected_language: str
    confidence: float
    is_supported: bool

class AnalyzeRequest(BaseModel):
    text: str
    mode: WritingMode = WritingMode.GRAMMAR_FIX
    document_name: Optional[str] = "Untitled Document"

class AnalyzeResponse(BaseModel):
    document_name: str
    mode: WritingMode
    original_text: str
    language: LanguageInfo
    stats: DocumentStats
    scores: QualityScore
    readability: ReadabilityMetrics
    issues: List[IssueItem]
    corrected_text: str
    after_scores: QualityScore
    after_error_count: int
    vocabulary_analysis: Dict[str, Any]
    sentence_structure_analysis: Dict[str, Any]
    document_hierarchy: Dict[str, Any]

class HistoryEntry(BaseModel):
    id: str
    timestamp: str
    document_name: str
    mode: str
    word_count: int
    score_before: int
    score_after: int
    errors_before: int
    errors_after: int
    category_breakdown: Dict[str, int]
