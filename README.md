# ✨ Syntaxa AI — AI-Powered Context-Aware Writing Intelligence

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.122-009688.svg)](https://fastapi.tiangolo.com)
[![spaCy](https://img.shields.io/badge/spaCy-3.8.11-09a3d5.svg)](https://spacy.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

**Syntaxa AI** is an advanced NLP-based writing intelligence system that analyzes sentences, paragraphs, and complete multi-page documents to detect grammatical, spelling, punctuation, clarity, vocabulary, and sentence-structure issues.

Unlike traditional spell checkers that perform isolated dictionary lookups, **Syntaxa AI understands linguistic context**: it identifies what is wrong, categorizes the error, explains *why* it is wrong using linguistic rules, recommends contextually appropriate corrections, evaluates multi-dimensional writing scores (0–100), and tracks personalized writing improvement over time.

---

## 🌟 Key Capabilities & Features

### 1. Context-Aware Linguistic Grammar Detection
- **Subject-Verb Agreement**: Evaluates noun-verb number concord, compound subjects, and auxiliary verbs (`"She go to college"` ➔ `"She goes"`; `"The students was studying"` ➔ `"were"`; `"The algorithm were successful"` ➔ `"was"`).
- **Verb Tense & Temporal Coherence**: Identifies temporal adverbs and enforces tense harmony (`"Yesterday I go to college"` ➔ `"went"`).
- **Quantifier Concord**: Detects plural/singular noun mismatches after quantifiers (`"Many student were present"` ➔ `"students"`).
- **Article Usage**: Flags missing articles before countable singular nouns (`"I bought book"` ➔ `"a book"`) and phonetic vowel mismatches (`a` vs `an`).
- **Preposition Collocations**: Corrects non-standard preposition pairings (`"He is good in mathematics"` ➔ `"good at"`).

### 2. Contextual Spelling & Domain Whitelisting
- High-precision dictionary checking powered by `SpellChecker`.
- **Domain & Tech Whitelist**: Never flags valid technical terminology (`Python`, `TensorFlow`, `PostgreSQL`, `OpenAI`, `PyTorch`, `Docker`, `Kubernetes`, `FastAPI`, `NLP`, `LLM`, etc.).
- Preserves exact capitalization formatting and provides candidate suggestions.

### 3. Punctuation & Orthography Analysis
- Detects missing periods and interrogative question marks for inquiry sentences (`"Hello how are you"` ➔ `"Hello, how are you?"`).
- Introductory transition commas (`"However,"`, `"Therefore,"`, `"For example,"`).
- Sentence boundary capitalization and excessive punctuation normalization (`"???"` ➔ `"?"`).

### 4. Sentence Structure & Stylistic Optimization
- **Passive Repetition Reduction**: Detects repeated passive clauses (`"The project was developed by us and it was tested by us and it was deployed by us"` ➔ `"We developed, tested, and deployed the project."`).
- **Run-on Sentences & Conjunction Chaining**: Flags sentences exceeding 35 words or with excessive `and` chains.

### 5. Clarity & Conciseness Engine
- Identifies verbose bureaucratic phrasing:
  - `"due to the fact that"` ➔ `"because"`
  - `"in order to"` ➔ `"to"`
  - `"at the present time"` ➔ `"currently"`
  - `"has the ability to"` ➔ `"can"`
  - Nominalizations (`"make a decision"` ➔ `"decide"`, `"conduct an investigation into"` ➔ `"investigate"`).

### 6. Readability & Quantitative Metrics
- Flesch Reading Ease score (0–100).
- Flesch-Kincaid Grade Level & Coleman-Liau Index.
- Average sentence length, word length, and complex words percentage.
- Audience suitability classification (e.g. *"College-level readers"*, *"General audience"*).

### 7. Vocabulary Enhancement & Overuse Detection
- Identifies overused words (e.g., `"good"` used 12 times) and suggests academic/professional alternatives (`"effective"`, `"useful"`, `"successful"`, `"appropriate"`).
- Type-Token Ratio (TTR) lexical diversity metric.

### 8. Explain My Error Feature (4 Pedagogical Pillars)
For every single error, Syntaxa AI presents:
1. **What is wrong**: Exact token / phrase
2. **What type of error it is**: Specific rule category
3. **Why it is incorrect**: In-depth linguistic rule explanation
4. **What the correct form is**: Contextual drop-in replacement
5. **Actionable writing insight / tip**: For long-term mastery

### 9. Multiple Writing Modes
- **Grammar Fix**: Strict error correction while preserving original voice.
- **Professional**: Formal tone, expands informal contractions (`don't` ➔ `do not`).
- **Academic**: Elevates colloquial language to scholarly terminology.
- **Simple**: Converts dense prose to plain English.
- **Concise**: Aggressively trims tautologies, filler words, and redundancies.

### 10. Multi-Format Document Processing
- Direct text entry & copy-paste.
- **`.txt`** & **`.md`** plain text.
- **`.docx`** Microsoft Word documents via `python-docx`.
- **`.pdf`** Adobe PDF documents via `PyMuPDF` (`fitz`) and `pypdf`.
- Preserves sections, headings, and paragraph boundaries.

### 11. Personalized Writing Profile & Progress Tracking
- Stores historical analyses in SQLite (`data/syntaxa_history.db`).
- Visualizes recurring issues breakdown:
  - e.g. 31% Long sentences, 24% Subject-verb agreement, 19% Punctuation, 15% Articles, 11% Repeated vocabulary.
  - Chronological score progression chart across documents.
  - Diagnostic weakness recommendation.

---

## 🏛️ System Architecture

```
                    ┌──────────────────────────┐
                    │  Modern Web UI (HTML/CSS)│
                    │   Glassmorphism + SVG    │
                    └────────────┬─────────────┘
                                 │ HTTP / JSON
                                 ▼
                    ┌──────────────────────────┐
                    │      FastAPI Gateway     │
                    │   (Endpoints & Storage)  │
                    └────────────┬─────────────┘
                                 │
           ┌─────────────────────┼─────────────────────┐
           ▼                     ▼                     ▼
┌───────────────────┐  ┌───────────────────┐  ┌───────────────────┐
│  Document Parser  │  │ Language Detector │  │ NLP Preprocessor  │
│  (TXT/DOCX/PDF)   │  │ (English Concord) │  │ (spaCy core_lg)   │
└───────────────────┘  └───────────────────┘  └─────────┬─────────┘
                                                        │ Tokens, POS, Dep Graph
    ┌────────────────┬────────────────┬─────────────────┼────────────────┬────────────────┐
    ▼                ▼                ▼                 ▼                ▼                ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│Grammar Engine│ │Spell Engine  │ │Punct Engine  │ │Clarity Engine│ │Struct Engine │ │Vocab Engine  │
│(Subj-Verb,   │ │(Whitelist,   │ │(Commas,      │ │(Wordiness,   │ │(Passives,    │ │(TTR, Syns,   │
│ Tense, Prep) │ │ Homophones)  │ │ Questions)   │ │ Fillers)     │ │ Run-ons)     │ │ Overuse)     │
└───────┬──────┘ └──────┬───────┘ └──────┬───────┘ └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
        │               │                │                │                │                │
        └───────────────┴────────────────┼────────────────┴────────────────┴────────────────┘
                                         ▼
                             ┌───────────────────────┐
                             │  Mode Transformation  │
                             │  (Academic, Concise)  │
                             └───────────┬───────────┘
                                         ▼
                             ┌───────────────────────┐
                             │  Correction Engine    │
                             │  (Reverse Patching)   │
                             └───────────┬───────────┘
                                         ▼
                             ┌───────────────────────┐
                             │ Quality Scoring (0-100│
                             │ Readability (textstat)│
                             └───────────┬───────────┘
                                         ▼
                             ┌───────────────────────┐
                             │  SQLite Profile Store │
                             │  (Progress Tracking)  │
                             └───────────────────────┘
```

---

## 🚀 Quickstart Guide

### 1. Requirements
- Python 3.10+
- spaCy with `en_core_web_lg` or `en_core_web_sm`
- Modern web browser (Chrome, Edge, Firefox, Safari)

### 2. Installation
```bash
# Clone or navigate to the project directory
cd d:/Projects/NLLP

# Install dependencies
python -m pip install -r requirements.txt
```

### 3. Launching Syntaxa AI
```bash
# Start the web server and open the browser
python run.py
```
Or run directly with Uvicorn:
```bash
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

Once launched, visit:
- **Web Application**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive Swagger API Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧪 Running the Unit Tests

Execute the comprehensive test suite validating all grammatical, spelling, punctuation, clarity, and structural scenarios:
```bash
python tests/test_pipeline.py
```

Output:
```
.............
----------------------------------------------------------------------
Ran 13 tests in 16.604s

OK
```

---

## 📊 Mathematical Quality Scoring

The overall writing score ($S_{overall} \in [0, 100]$) is computed through an empirical multi-factor formula:

$$S_{overall} = \mathrm{round}\Big(0.28 \cdot S_g + 0.20 \cdot S_s + 0.15 \cdot S_p + 0.15 \cdot S_c + 0.12 \cdot S_v + 0.10 \cdot S_r\Big)$$

Where:
- $S_g$: **Grammar Score** (penalized by errors per 100 words)
- $S_s$: **Spelling Score** (penalized by spelling density per 100 words)
- $S_p$: **Punctuation Score** (penalized by missing commas, periods, capitalization)
- $S_c$: **Clarity Score** (penalized by wordiness, nominalizations, passive repetition)
- $S_v$: **Vocabulary Score** (rewarded by Lexical Diversity TTR, penalized by overused words)
- $S_r$: **Readability Score** (calculated from Flesch Reading Ease normalized curve)

---

## 📁 Repository Structure

```
d:/Projects/NLLP/
├── backend/
│   ├── core/
│   │   ├── document_parser.py     # TXT, DOCX, and PDF parsing with section hierarchy
│   │   ├── language_detector.py   # English language detection & confidence rating
│   │   └── preprocessor.py        # spaCy pipeline singleton, POS & dependency tagging
│   ├── engines/
│   │   ├── clarity_engine.py      # Wordiness, filler phrases, nominalizations
│   │   ├── correction_engine.py   # Reverse-ordered character patcher
│   │   ├── explain_engine.py      # Pedagogical breakdown & 4-pillar error cards
│   │   ├── grammar_engine.py      # Subject-verb, verb tenses, articles, collocations
│   │   ├── modes_engine.py        # Grammar Fix, Professional, Academic, Simple, Concise
│   │   ├── punctuation_engine.py  # Missing periods, commas, question marks, capitalization
│   │   ├── readability_engine.py  # Flesch Reading Ease, grade level, audience targeting
│   │   ├── scoring_engine.py      # Multi-factor mathematical 0-100 score model
│   │   ├── spelling_engine.py     # SpellChecker with technical AI/tech whitelist
│   │   ├── structure_engine.py    # Repetitive passive voice, run-ons, conjunction chains
│   │   └── vocabulary_engine.py   # Lexical diversity (TTR) & overused word synonyms
│   ├── models/
│   │   └── schemas.py             # Pydantic models for API requests/responses
│   ├── storage/
│   │   └── history.py             # SQLite writing profile & progress tracker
│   └── main.py                    # FastAPI routes, file upload handler, static server
├── frontend/
│   ├── css/
│   │   └── styles.css             # Glassmorphism, dark theme, micro-animations
│   ├── js/
│   │   └── app.js                 # Editor events, live highlight layer, diff, charts
│   └── index.html                 # Complete 5-tab web user interface
├── tests/
│   ├── sample_assignment.txt      # Rich assignment sample with all error types
│   └── test_pipeline.py           # 13 automated unit tests
├── requirements.txt               # Python package dependencies
├── run.py                         # One-click startup launcher
└── README.md                      # Comprehensive documentation
```

---

## 🎓 Example Scenario Walkthrough

1. **User loads or pastes a 2,000-word assignment** into the editor or uploads `assignment.pdf`.
2. **Text is normalized & segmented** into sections, paragraphs, sentences, and tokens.
3. **Linguistic analysis executes** across grammar, spelling, punctuation, structure, clarity, and vocabulary engines.
4. **User reviews interactive highlights**: Clicking *"The algorithm were successful"* displays:
   - **Error**: `were`
   - **Type**: `Subject-Verb Agreement`
   - **Explanation**: *"Algorithm" is singular, so the singular past verb "was" is required.*
   - **Correction**: `was`
5. **Mode Selection**: User switches to **Academic**, transforming informal words and elevating phrasing.
6. **Side-by-Side Diff**: User compares Before vs After:
   - Score: **71 ➔ 92**
   - Errors: **14 ➔ 1**
7. **Writing Profile**: System records the session, updating long-term diagnostic tracking and progress charts!
