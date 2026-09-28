import re
import io
from typing import List, Dict, Any, Optional

try:
    import docx
except ImportError:
    docx = None

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

try:
    import pypdf
except ImportError:
    pypdf = None

def parse_txt_bytes(content: bytes) -> str:
    """Parse text file with encoding fallback."""
    for enc in ("utf-8", "utf-8-sig", "latin-1", "cp1252"):
        try:
            return content.decode(enc)
        except UnicodeDecodeError:
            continue
    return content.decode("utf-8", errors="replace")

def parse_docx_bytes(content: bytes) -> str:
    """Extract formatted text from docx file bytes."""
    if not docx:
        raise ImportError("python-docx is not installed.")
    doc = docx.Document(io.BytesIO(content))
    paragraphs = []
    for p in doc.paragraphs:
        text = p.text.strip()
        if text:
            paragraphs.append(text)
    return "\n\n".join(paragraphs)

def parse_pdf_bytes(content: bytes) -> str:
    """Extract text from pdf file bytes using PyMuPDF (fitz) or pypdf fallback."""
    if fitz:
        try:
            doc = fitz.open(stream=content, filetype="pdf")
            pages_text = []
            for page in doc:
                text = page.get_text()
                if text.strip():
                    pages_text.append(text.strip())
            if pages_text:
                return "\n\n".join(pages_text)
        except Exception:
            pass

    if pypdf:
        reader = pypdf.PdfReader(io.BytesIO(content))
        pages_text = []
        for page in reader.pages:
            t = page.extract_text()
            if t and t.strip():
                pages_text.append(t.strip())
        return "\n\n".join(pages_text)

    raise ImportError("Neither PyMuPDF nor pypdf could extract text from PDF.")

def extract_text_from_upload(filename: str, content: bytes) -> str:
    """Dispatch file extraction based on file extension."""
    lower_name = filename.lower()
    if lower_name.endswith(".docx"):
        return parse_docx_bytes(content)
    elif lower_name.endswith(".pdf"):
        return parse_pdf_bytes(content)
    elif lower_name.endswith(".txt") or lower_name.endswith(".md"):
        return parse_txt_bytes(content)
    else:
        # Default try text decode
        return parse_txt_bytes(content)

def segment_document_hierarchy(raw_text: str, nlp_sentences: List[str] = None) -> Dict[str, Any]:
    """
    Divides document into:
    Document -> Sections -> Paragraphs -> Sentences -> Word Count
    """
    raw_paragraphs = [p.strip() for p in re.split(r'\n\s*\n', raw_text) if p.strip()]
    if not raw_paragraphs:
        raw_paragraphs = [raw_text.strip()] if raw_text.strip() else []

    sections = []
    current_section = {
        "title": "General",
        "paragraphs": []
    }

    # Regex to detect section headers (e.g., "1. Introduction", "# Summary", "Conclusion")
    header_regex = re.compile(r'^(#+\s+.+|[0-9]+(\.[0-9]+)*\s+[A-Z].+|[A-Z][A-Za-z0-9\s]{2,40}:?$)$')

    for p in raw_paragraphs:
        first_line = p.split('\n')[0].strip()
        if len(p.split('\n')) == 1 and len(first_line) < 60 and header_regex.match(first_line):
            if current_section["paragraphs"]:
                sections.append(current_section)
            current_section = {
                "title": first_line.lstrip('#').strip(),
                "paragraphs": []
            }
        else:
            # Segment into sentences roughly or from spacy
            sentences_in_p = [s.strip() for s in re.split(r'(?<=[.!?])\s+', p) if s.strip()]
            current_section["paragraphs"].append({
                "text": p,
                "sentences": sentences_in_p,
                "sentence_count": len(sentences_in_p),
                "word_count": len(re.findall(r'\b\w+\b', p))
            })

    if current_section["paragraphs"] or not sections:
        sections.append(current_section)

    return {
        "title": "Document",
        "section_count": len(sections),
        "total_paragraphs": len(raw_paragraphs),
        "sections": sections
    }
