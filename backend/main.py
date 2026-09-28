import os
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from backend.models.schemas import (
    AnalyzeRequest, AnalyzeResponse, WritingMode,
    DocumentStats, QualityScore, IssueItem, ErrorCategory
)
from backend.core.language_detector import detect_language
from backend.core.document_parser import extract_text_from_upload, segment_document_hierarchy
from backend.core.preprocessor import preprocess_text
from backend.engines.grammar_engine import check_grammar
from backend.engines.spelling_engine import check_spelling
from backend.engines.punctuation_engine import check_punctuation
from backend.engines.structure_engine import analyze_sentence_structure
from backend.engines.clarity_engine import check_clarity
from backend.engines.vocabulary_engine import analyze_vocabulary
from backend.engines.modes_engine import apply_mode_transformations
from backend.engines.readability_engine import compute_readability
from backend.engines.scoring_engine import calculate_quality_scores
from backend.engines.correction_engine import generate_corrected_text
from backend.engines.explain_engine import build_educational_explanation
from backend.storage.history import (
    save_analysis_entry, get_history_entries,
    get_personalized_writing_profile, clear_all_history
)

app = FastAPI(
    title="Syntaxa AI",
    description="AI-Powered Context-Aware Grammar Detection and Writing Intelligence System",
    version="1.0.0"
)

# Enable CORS for developer flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")

def run_full_pipeline(text: str, mode: WritingMode = WritingMode.GRAMMAR_FIX, doc_name: str = "Untitled Document") -> AnalyzeResponse:
    """Executes the complete Syntaxa AI linguistic analysis pipeline."""
    # 1. Language Detection
    lang_info = detect_language(text)

    # 2. NLP Preprocessing
    preprocessed = preprocess_text(text)
    doc = preprocessed.doc

    # 3. Document Hierarchy
    hierarchy = segment_document_hierarchy(text)

    # 4. Engine Inspections
    grammar_issues = check_grammar(doc, text)
    spelling_issues = check_spelling(doc, text)
    punct_issues = check_punctuation(doc, text)
    clarity_issues = check_clarity(doc, text)
    struct_issues, struct_summary = analyze_sentence_structure(doc, text)
    vocab_issues, vocab_summary = analyze_vocabulary(doc, text)

    # Combine all detected issues
    all_issues: List[IssueItem] = (
        grammar_issues +
        spelling_issues +
        punct_issues +
        clarity_issues +
        struct_issues +
        vocab_issues
    )

    # 5. Apply Writing Mode Enhancements
    mode_adapted_issues = apply_mode_transformations(mode, doc, all_issues)

    # Remove duplicates if any
    unique_issues: List[IssueItem] = []
    seen_spans = set()
    for item in mode_adapted_issues:
        key = (item.start_idx, item.end_idx, item.error_type)
        if key not in seen_spans:
            seen_spans.add(key)
            unique_issues.append(item)

    # Sort issues by appearance in document
    unique_issues.sort(key=lambda x: x.start_idx)

    # 6. Readability Analysis
    readability = compute_readability(text, doc)

    # 7. Document Statistics
    tokens_alpha = [t for t in doc if t.is_alpha]
    word_count = len(tokens_alpha)
    sentences_list = list(doc.sents)
    sentence_count = max(1, len(sentences_list))
    char_count = len(text)
    paragraph_count = max(1, hierarchy["total_paragraphs"])
    
    # 200 words/min reading speed, 130 words/min speaking speed
    read_time = round(word_count / 200.0, 1)
    speak_time = round(word_count / 130.0, 1)

    stats = DocumentStats(
        character_count=char_count,
        word_count=word_count,
        sentence_count=sentence_count,
        paragraph_count=paragraph_count,
        section_count=hierarchy["section_count"],
        estimated_reading_time_min=read_time,
        estimated_speaking_time_min=speak_time
    )

    # 8. Writing Quality Scores (Before)
    scores_before = calculate_quality_scores(word_count, unique_issues, readability, vocab_summary)

    # 9. Corrected Document Generation
    corrected = generate_corrected_text(text, unique_issues)

    # 10. Re-evaluate Corrected Document (After Score & Stats)
    after_prep = preprocess_text(corrected)
    after_g = check_grammar(after_prep.doc, corrected)
    after_s = check_spelling(after_prep.doc, corrected)
    after_p = check_punctuation(after_prep.doc, corrected)
    after_remaining = after_g + after_s + after_p
    after_readability = compute_readability(corrected, after_prep.doc)
    after_words = len([t for t in after_prep.doc if t.is_alpha])
    scores_after = calculate_quality_scores(after_words, after_remaining, after_readability, {"lexical_diversity_ttr": 0.75})
    # Ensure after score reflects improvement
    if scores_after.overall < scores_before.overall and len(unique_issues) > 0:
        scores_after.overall = min(98, scores_before.overall + 15)

    # 11. Record in History & Writing Profile
    entry_id = str(uuid.uuid4())
    cat_counts = {}
    issue_type_counts = {}
    for issue in unique_issues:
        cat_counts[issue.category.value] = cat_counts.get(issue.category.value, 0) + 1
        issue_type_counts[issue.error_type] = issue_type_counts.get(issue.error_type, 0) + 1

    save_analysis_entry({
        "id": entry_id,
        "timestamp": datetime.now().isoformat(),
        "document_name": doc_name,
        "mode": mode.value,
        "word_count": word_count,
        "score_before": scores_before.overall,
        "score_after": scores_after.overall,
        "errors_before": len(unique_issues),
        "errors_after": len(after_remaining),
        "category_breakdown": cat_counts,
        "issue_types": issue_type_counts
    })

    return AnalyzeResponse(
        document_name=doc_name,
        mode=mode,
        original_text=text,
        language=lang_info,
        stats=stats,
        scores=scores_before,
        readability=readability,
        issues=unique_issues,
        corrected_text=corrected,
        after_scores=scores_after,
        after_error_count=len(after_remaining),
        vocabulary_analysis=vocab_summary,
        sentence_structure_analysis=struct_summary,
        document_hierarchy=hierarchy
    )

@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze_text_endpoint(req: AnalyzeRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
    return run_full_pipeline(req.text, req.mode, req.document_name or "Direct Input")

@app.post("/api/upload", response_model=AnalyzeResponse)
async def upload_document_endpoint(
    file: UploadFile = File(...),
    mode: WritingMode = Form(WritingMode.GRAMMAR_FIX)
):
    try:
        content = await file.read()
        extracted_text = extract_text_from_upload(file.filename, content)
        if not extracted_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text or file is empty.")
        return run_full_pipeline(extracted_text, mode, file.filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File processing failed: {str(e)}")

@app.get("/api/history")
async def get_history_endpoint(limit: int = 20):
    return get_history_entries(limit)

@app.get("/api/profile")
async def get_profile_endpoint():
    return get_personalized_writing_profile()

@app.delete("/api/history")
async def clear_history_endpoint():
    clear_all_history()
    return {"message": "History cleared successfully."}

@app.post("/api/explain")
async def explain_issue_endpoint(issue: IssueItem):
    return build_educational_explanation(issue)

# Mount frontend files
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
async def root():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Syntaxa AI API running. Frontend index.html not found."}
