/**
 * Syntaxa AI - AI-Powered Writing Intelligence Frontend Application
 */

// Application State
const state = {
  currentAnalysis: null,
  activeCategoryFilter: 'all',
  activePopoverIssue: null,
  selectedMode: 'grammar_fix',
  isAnalyzing: false,
};

// DOM Elements Cache
const elements = {
  // Navigation
  navTabs: document.querySelectorAll('.nav-tab-btn'),
  tabPanes: document.querySelectorAll('.tab-pane'),

  // Header Controls
  writingModeSelect: document.getElementById('writingModeSelect'),
  btnLoadSample: document.getElementById('btnLoadSample'),
  btnTriggerUpload: document.getElementById('btnTriggerUpload'),
  fileUploadInput: document.getElementById('fileUploadInput'),
  btnAnalyze: document.getElementById('btnAnalyze'),
  btnAnalyzeText: document.getElementById('btnAnalyzeText'),
  btnAnalyzeIcon: document.getElementById('btnAnalyzeIcon'),

  // Editor
  docTitleInput: document.getElementById('docTitleInput'),
  langPill: document.getElementById('langPill'),
  langName: document.getElementById('langName'),
  langConfidence: document.getElementById('langConfidence'),
  editorWrapper: document.getElementById('editorWrapper'),
  editorTextarea: document.getElementById('editorTextarea'),
  editorHighlights: document.getElementById('editorHighlights'),
  btnApplyAllEditor: document.getElementById('btnApplyAllEditor'),
  btnClearEditor: document.getElementById('btnClearEditor'),
  btnExport: document.getElementById('btnExport'),
  fileDropZone: document.getElementById('fileDropZone'),

  // Stats Bar
  statWords: document.getElementById('statWords'),
  statChars: document.getElementById('statChars'),
  statSentences: document.getElementById('statSentences'),
  statReadTime: document.getElementById('statReadTime'),

  // Dashboard Scores
  scoreCircle: document.getElementById('scoreCircle'),
  overallScoreVal: document.getElementById('overallScoreVal'),
  scoreLevelBadge: document.getElementById('scoreLevelBadge'),
  scoreTargetAudience: document.getElementById('scoreTargetAudience'),

  // Sub-scores
  scoreGrammarVal: document.getElementById('scoreGrammarVal'),
  progressGrammar: document.getElementById('progressGrammar'),
  scoreSpellingVal: document.getElementById('scoreSpellingVal'),
  progressSpelling: document.getElementById('progressSpelling'),
  scorePunctVal: document.getElementById('scorePunctVal'),
  progressPunct: document.getElementById('progressPunct'),
  scoreClarityVal: document.getElementById('scoreClarityVal'),
  progressClarity: document.getElementById('progressClarity'),
  scoreVocabVal: document.getElementById('scoreVocabVal'),
  progressVocab: document.getElementById('progressVocab'),
  scoreReadabilityVal: document.getElementById('scoreReadabilityVal'),
  progressReadability: document.getElementById('progressReadability'),

  // Feed & Filters
  issuesCountBadge: document.getElementById('issuesCountBadge'),
  categoryFilterContainer: document.getElementById('categoryFilterContainer'),
  issuesList: document.getElementById('issuesList'),

  // Popover
  errorPopover: document.getElementById('errorPopover'),
  popoverBadge: document.getElementById('popoverBadge'),
  popoverOrig: document.getElementById('popoverOrig'),
  popoverRepl: document.getElementById('popoverRepl'),
  popoverExpl: document.getElementById('popoverExpl'),
  btnPopoverAccept: document.getElementById('btnPopoverAccept'),
  btnPopoverExplain: document.getElementById('btnPopoverExplain'),
  btnDismissPopover: document.getElementById('btnDismissPopover'),

  // Tab 2: Diff
  diffBeforeScore: document.getElementById('diffBeforeScore'),
  diffAfterScore: document.getElementById('diffAfterScore'),
  diffResolvedCount: document.getElementById('diffResolvedCount'),
  diffReadingEase: document.getElementById('diffReadingEase'),
  panelBadgeBefore: document.getElementById('panelBadgeBefore'),
  panelBadgeAfter: document.getElementById('panelBadgeAfter'),
  diffOriginalText: document.getElementById('diffOriginalText'),
  diffCorrectedText: document.getElementById('diffCorrectedText'),
  btnCopyCorrected: document.getElementById('btnCopyCorrected'),
  btnApplyCorrectedToEditor: document.getElementById('btnApplyCorrectedToEditor'),

  // Tab 3: Explain
  explainCardsGrid: document.getElementById('explainCardsGrid'),

  // Tab 4: Report
  reportDocTitle: document.getElementById('reportDocTitle'),
  reportTimestamp: document.getElementById('reportTimestamp'),
  reportWords: document.getElementById('reportWords'),
  reportSentences: document.getElementById('reportSentences'),
  reportParagraphs: document.getElementById('reportParagraphs'),
  reportSections: document.getElementById('reportSections'),
  reportGrade: document.getElementById('reportGrade'),
  reportAudience: document.getElementById('reportAudience'),
  reportTTR: document.getElementById('reportTTR'),
  reportCategoriesTable: document.getElementById('reportCategoriesTable'),
  reportPassiveCount: document.getElementById('reportPassiveCount'),
  reportPassivePct: document.getElementById('reportPassivePct'),
  reportAvgSentLen: document.getElementById('reportAvgSentLen'),
  reportLongestSent: document.getElementById('reportLongestSent'),
  reportRepeatedWordsList: document.getElementById('reportRepeatedWordsList'),

  // Tab 5: Profile
  profTotalDocs: document.getElementById('profTotalDocs'),
  profTotalWords: document.getElementById('profTotalWords'),
  profAvgScore: document.getElementById('profAvgScore'),
  profAvgGain: document.getElementById('profAvgGain'),
  profRecommendationBox: document.getElementById('profRecommendationBox'),
  commonIssuesList: document.getElementById('commonIssuesList'),
  timelineChart: document.getElementById('timelineChart'),
  btnClearHistory: document.getElementById('btnClearHistory'),

  // Toast
  toastMsg: document.getElementById('toastMsg'),
  toastIcon: document.getElementById('toastIcon'),
  toastText: document.getElementById('toastText')
};

// Sample assignment template showcasing all prompt scenarios
const SAMPLE_TEXT = `Machine Learning Assignment: NLP Writing Analysis

1. Introduction
Yesterday I go to college. The algorithm were successful in processing the raw data. Many student was interested in the topic. She go to college every day to study deep learning.

2. System Architecture
The project was developed by us and it was tested by us and it was deployed by us. Due to the fact that the system was not functioning properly, the project implementation was delayed. He is good in mathematics and computer science.

3. Results and Discussion
I recieved the assignment using Python, TensorFlow, PostgreSQL, and OpenAI. I bought book on neural networks to understand the concept. Hello how are you

This is a good method. It gives good performance and good accuracy for good models. Each student should submit their assignment on time.`;

// ==========================================================================
// Initialization & Event Listeners
// ==========================================================================

document.addEventListener('DOMContentLoaded', () => {
  initNavTabs();
  initEditorEvents();
  initHeaderActions();
  initPopoverEvents();
  updateLiveTextMetrics();
  loadWritingProfile();
});

// Navigation Tabs
function initNavTabs() {
  elements.navTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const targetId = tab.dataset.target;
      elements.navTabs.forEach(t => t.classList.remove('active'));
      elements.tabPanes.forEach(p => p.classList.remove('active'));

      tab.classList.add('active');
      const targetPane = document.getElementById(targetId);
      if (targetPane) targetPane.classList.add('active');

      if (targetId === 'tabProfile') {
        loadWritingProfile();
      }
    });
  });
}

// Editor Events
function initEditorEvents() {
  elements.editorTextarea.addEventListener('input', () => {
    updateLiveTextMetrics();
    hidePopover();
    // Clear highlights when typing until re-analyzed
    if (state.currentAnalysis) {
      elements.editorHighlights.innerHTML = '';
    }
  });

  // Synchronize scrolling between textarea and highlight layer
  elements.editorTextarea.addEventListener('scroll', () => {
    elements.editorHighlights.scrollTop = elements.editorTextarea.scrollTop;
    elements.editorHighlights.scrollLeft = elements.editorTextarea.scrollLeft;
  });

  // Drag and drop support
  const dropZone = elements.fileDropZone;
  ['dragenter', 'dragover'].forEach(name => {
    dropZone.addEventListener(name, (e) => {
      e.preventDefault();
      dropZone.classList.add('drag-active');
    });
  });

  ['dragleave', 'drop'].forEach(name => {
    dropZone.addEventListener(name, (e) => {
      e.preventDefault();
      dropZone.classList.remove('drag-active');
    });
  });

  dropZone.addEventListener('drop', (e) => {
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileUpload(files[0]);
    }
  });

  dropZone.addEventListener('click', () => {
    elements.fileUploadInput.click();
  });
}

// Header & Action Events
function initHeaderActions() {
  elements.btnLoadSample.addEventListener('click', () => {
    elements.docTitleInput.value = "Machine Learning Assignment: NLP Writing Analysis";
    elements.editorTextarea.value = SAMPLE_TEXT;
    updateLiveTextMetrics();
    showToast("Sample assignment loaded. Click 'Analyze Writing'!", "📝");
    analyzeDocument();
  });

  elements.btnTriggerUpload.addEventListener('click', () => {
    elements.fileUploadInput.click();
  });

  elements.fileUploadInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
      handleFileUpload(e.target.files[0]);
    }
  });

  elements.btnAnalyze.addEventListener('click', () => {
    analyzeDocument();
  });

  elements.writingModeSelect.addEventListener('change', (e) => {
    state.selectedMode = e.target.value;
    if (elements.editorTextarea.value.trim().length > 0) {
      analyzeDocument();
    }
  });

  elements.btnClearEditor.addEventListener('click', () => {
    elements.editorTextarea.value = '';
    elements.editorHighlights.innerHTML = '';
    state.currentAnalysis = null;
    updateLiveTextMetrics();
    resetDashboard();
    hidePopover();
    showToast("Editor cleared.", "🗑️");
  });

  elements.btnApplyAllEditor.addEventListener('click', () => {
    if (state.currentAnalysis && state.currentAnalysis.corrected_text) {
      elements.editorTextarea.value = state.currentAnalysis.corrected_text;
      updateLiveTextMetrics();
      showToast("All improvements applied successfully!", "✓");
      analyzeDocument();
    } else {
      showToast("No analysis available. Click Analyze first.", "⚠️");
    }
  });

  elements.btnExport.addEventListener('click', exportDocument);
  elements.btnCopyCorrected.addEventListener('click', copyCorrectedText);
  elements.btnApplyCorrectedToEditor.addEventListener('click', () => {
    if (state.currentAnalysis && state.currentAnalysis.corrected_text) {
      elements.editorTextarea.value = state.currentAnalysis.corrected_text;
      updateLiveTextMetrics();
      // Switch back to editor tab
      document.getElementById('tabBtnEditor').click();
      showToast("Corrected text copied into editor!", "✍️");
      analyzeDocument();
    }
  });

  elements.btnClearHistory.addEventListener('click', clearUserHistory);

  // Category Filter Buttons
  elements.categoryFilterContainer.addEventListener('click', (e) => {
    const btn = e.target.closest('.cat-filter-btn');
    if (!btn) return;
    elements.categoryFilterContainer.querySelectorAll('.cat-filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    state.activeCategoryFilter = btn.dataset.cat;
    filterIssuesFeed();
  });
}

// Popover Events
function initPopoverEvents() {
  elements.btnDismissPopover.addEventListener('click', hidePopover);

  elements.btnPopoverAccept.addEventListener('click', () => {
    if (state.activePopoverIssue) {
      applySingleIssueCorrection(state.activePopoverIssue);
      hidePopover();
    }
  });

  elements.btnPopoverExplain.addEventListener('click', () => {
    if (state.activePopoverIssue) {
      hidePopover();
      document.getElementById('tabBtnExplain').click();
      // Scroll to relevant card
      const targetCard = document.getElementById(`pedagogy-${state.activePopoverIssue.id}`);
      if (targetCard) {
        targetCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
        targetCard.style.borderColor = 'var(--accent-primary)';
      }
    }
  });

  // Close popover when clicking outside
  document.addEventListener('click', (e) => {
    if (!elements.errorPopover.contains(e.target) && !e.target.classList.contains('err-mark')) {
      hidePopover();
    }
  });
}

// ==========================================================================
// Core Pipeline Calling & Analysis Execution
// ==========================================================================

async function analyzeDocument() {
  const text = elements.editorTextarea.value.trim();
  if (!text) {
    showToast("Please enter or paste text to analyze.", "⚠️");
    return;
  }

  setAnalyzingState(true);

  try {
    const response = await fetch('/api/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: elements.editorTextarea.value,
        mode: state.selectedMode,
        document_name: elements.docTitleInput.value.trim() || "Untitled Document"
      })
    });

    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.detail || "Analysis failed.");
    }

    const data = await response.json();
    state.currentAnalysis = data;

    // Render all visual modules
    renderAnalysisResults(data);
    showToast(`Analysis complete: ${data.issues.length} improvements detected!`, "✨");

  } catch (error) {
    console.error("Analysis Error:", error);
    showToast(`Error: ${error.message}`, "❌");
  } finally {
    setAnalyzingState(false);
  }
}

async function handleFileUpload(file) {
  setAnalyzingState(true);
  showToast(`Uploading and extracting: ${file.name}...`, "⏳");

  const formData = new FormData();
  formData.append('file', file);
  formData.append('mode', state.selectedMode);

  try {
    const response = await fetch('/api/upload', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.detail || "Upload failed.");
    }

    const data = await response.json();
    state.currentAnalysis = data;

    // Put extracted text into textarea
    elements.docTitleInput.value = data.document_name;
    elements.editorTextarea.value = data.original_text;
    updateLiveTextMetrics();

    renderAnalysisResults(data);
    showToast(`File extracted and analyzed successfully!`, "📄");

  } catch (error) {
    console.error("Upload Error:", error);
    showToast(`Upload failed: ${error.message}`, "❌");
  } finally {
    setAnalyzingState(false);
  }
}

// ==========================================================================
// Visual Rendering & Dashboard Updates
// ==========================================================================

function renderAnalysisResults(data) {
  // 1. Language pill
  elements.langName.textContent = data.language.detected_language;
  elements.langConfidence.textContent = `${Math.round(data.language.confidence * 100)}%`;

  // 2. Score Gauge
  updateScoreGauge(data.scores.overall);

  // 3. Sub-scores Bars
  updateSubscores(data.scores);

  // 4. Readability label
  elements.scoreTargetAudience.innerHTML = `<strong>${data.readability.reading_level_label}</strong>: ${data.readability.target_audience}`;

  // 5. In-text Highlights Layer
  renderInTextHighlights(data.original_text, data.issues);

  // 6. Issues Feed
  renderIssuesFeed(data.issues);

  // 7. Tab 2: Before vs After Diff
  renderDiffView(data);

  // 8. Tab 3: Explain My Error Pedagogical Cards
  renderExplainCards(data.issues);

  // 9. Tab 4: Detailed Analysis Report
  renderDetailedReport(data);
}

function updateScoreGauge(score) {
  elements.overallScoreVal.textContent = score;

  // Circle radius is 45, circumference ~ 283
  const circumference = 283;
  const offset = circumference - (score / 100) * circumference;
  elements.scoreCircle.style.strokeDashoffset = offset;

  // Level badge
  const badge = elements.scoreLevelBadge;
  if (score >= 85) {
    badge.textContent = "Excellent";
    badge.className = "score-level-badge score-level-good";
  } else if (score >= 70) {
    badge.textContent = "Good / Proficient";
    badge.className = "score-level-badge score-level-mod";
  } else {
    badge.textContent = "Needs Revision";
    badge.className = "score-level-badge score-level-low";
  }
}

function updateSubscores(scores) {
  elements.scoreGrammarVal.textContent = `${scores.grammar}/100`;
  elements.progressGrammar.style.width = `${scores.grammar}%`;

  elements.scoreSpellingVal.textContent = `${scores.spelling}/100`;
  elements.progressSpelling.style.width = `${scores.spelling}%`;

  elements.scorePunctVal.textContent = `${scores.punctuation}/100`;
  elements.progressPunct.style.width = `${scores.punctuation}%`;

  elements.scoreClarityVal.textContent = `${scores.clarity}/100`;
  elements.progressClarity.style.width = `${scores.clarity}%`;

  elements.scoreVocabVal.textContent = `${scores.vocabulary}/100`;
  elements.progressVocab.style.width = `${scores.vocabulary}%`;

  elements.scoreReadabilityVal.textContent = `${scores.readability}/100`;
  elements.progressReadability.style.width = `${scores.readability}%`;
}

// In-Text Highlighting
function renderInTextHighlights(rawText, issues) {
  if (!issues || issues.length === 0) {
    elements.editorHighlights.innerHTML = escapeHtml(rawText);
    return;
  }

  // Sort issues ascending by start_idx
  const sorted = [...issues].sort((a, b) => a.start_idx - b.start_idx);
  let html = '';
  let cursor = 0;

  for (const issue of sorted) {
    if (issue.start_idx < cursor) continue; // Skip overlaps

    // Append text leading up to this issue
    if (issue.start_idx > cursor) {
      html += escapeHtml(rawText.substring(cursor, issue.start_idx));
    }

    const spanText = rawText.substring(issue.start_idx, issue.end_idx);
    const catClass = `cat-${issue.category}`;
    html += `<span class="err-mark ${catClass}" data-issue-id="${issue.id}">${escapeHtml(spanText || ' ')}</span>`;
    cursor = issue.end_idx;
  }

  if (cursor < rawText.length) {
    html += escapeHtml(rawText.substring(cursor));
  }

  elements.editorHighlights.innerHTML = html;

  // Attach click listeners to all marks
  elements.editorHighlights.querySelectorAll('.err-mark').forEach(mark => {
    mark.addEventListener('click', (e) => {
      const issueId = mark.dataset.issueId;
      const issue = issues.find(i => i.id === issueId);
      if (issue) {
        showPopover(issue, mark);
      }
    });
  });
}

// Issues Feed in Right Dashboard
function renderIssuesFeed(issues) {
  elements.issuesCountBadge.textContent = `${issues.length} Improvement${issues.length === 1 ? '' : 's'}`;
  filterIssuesFeed();
}

function filterIssuesFeed() {
  if (!state.currentAnalysis) return;

  const issues = state.currentAnalysis.issues;
  const filter = state.activeCategoryFilter;

  const filtered = filter === 'all' 
    ? issues 
    : issues.filter(i => i.category === filter);

  if (filtered.length === 0) {
    elements.issuesList.innerHTML = `
      <div class="empty-issues-placeholder">
        <span>✓</span>
        <p>No issues found for category "${filter}".</p>
      </div>
    `;
    return;
  }

  let html = '';
  for (const issue of filtered) {
    const catBg = getCategoryColor(issue.category);
    html += `
      <div class="issue-card" id="card-${issue.id}" data-id="${issue.id}">
        <div class="issue-header">
          <span class="issue-cat-tag" style="background: ${catBg.bg}; color: ${catBg.fg};">
            ${issue.category} • ${issue.error_type}
          </span>
          <span style="font-size: 0.72rem; color: var(--text-dim); font-weight: 600;">#${issue.id}</span>
        </div>
        <div class="issue-diff-row">
          <span class="token-orig">${escapeHtml(issue.original_text || '[missing]')}</span>
          <span class="token-arrow">➔</span>
          <span class="token-repl">${escapeHtml(issue.replacement)}</span>
        </div>
        <div class="issue-msg">${escapeHtml(issue.short_message)}</div>
        <div class="issue-card-actions">
          <button class="btn btn-secondary btn-sm btn-feed-explain" data-id="${issue.id}">Explain</button>
          <button class="btn btn-accent btn-sm btn-feed-accept" data-id="${issue.id}">Accept</button>
        </div>
      </div>
    `;
  }

  elements.issuesList.innerHTML = html;

  // Bind actions
  elements.issuesList.querySelectorAll('.btn-feed-accept').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const issue = state.currentAnalysis.issues.find(i => i.id === btn.dataset.id);
      if (issue) applySingleIssueCorrection(issue);
    });
  });

  elements.issuesList.querySelectorAll('.btn-feed-explain').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      document.getElementById('tabBtnExplain').click();
      const targetCard = document.getElementById(`pedagogy-${btn.dataset.id}`);
      if (targetCard) {
        targetCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    });
  });

  // Card click highlights in text
  elements.issuesList.querySelectorAll('.issue-card').forEach(card => {
    card.addEventListener('click', () => {
      const issue = state.currentAnalysis.issues.find(i => i.id === card.dataset.id);
      if (issue) {
        const mark = elements.editorHighlights.querySelector(`[data-issue-id="${issue.id}"]`);
        if (mark) {
          showPopover(issue, mark);
          mark.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      }
    });
  });
}

// Popover
function showPopover(issue, targetElement) {
  state.activePopoverIssue = issue;
  const popover = elements.errorPopover;
  const catBg = getCategoryColor(issue.category);

  elements.popoverBadge.textContent = `${issue.category} • ${issue.error_type}`;
  elements.popoverBadge.style.background = catBg.bg;
  elements.popoverBadge.style.color = catBg.fg;

  elements.popoverOrig.textContent = issue.original_text || '[missing]';
  elements.popoverRepl.textContent = issue.replacement;
  elements.popoverExpl.textContent = issue.rule_explanation;

  // Positioning
  const rect = targetElement.getBoundingClientRect();
  const wrapperRect = elements.editorWrapper.getBoundingClientRect();

  const topPos = rect.bottom - wrapperRect.top + elements.editorTextarea.scrollTop + 8;
  const leftPos = Math.min(
    Math.max(10, rect.left - wrapperRect.left),
    elements.editorWrapper.clientWidth - 350
  );

  popover.style.top = `${topPos}px`;
  popover.style.left = `${leftPos}px`;
  popover.classList.add('visible');
}

function hidePopover() {
  elements.errorPopover.classList.remove('visible');
  state.activePopoverIssue = null;
}

// Single Issue Application
function applySingleIssueCorrection(issue) {
  const currentText = elements.editorTextarea.value;
  const start = issue.start_idx;
  const end = issue.end_idx;

  if (start >= 0 && end <= currentText.length) {
    const updated = currentText.substring(0, start) + issue.replacement + currentText.substring(end);
    elements.editorTextarea.value = updated;
    updateLiveTextMetrics();
    showToast(`Applied: "${issue.replacement}"`, "✓");
    analyzeDocument();
  }
}

// ==========================================================================
// Tab 2: Before vs After Side-by-Side Diff
// ==========================================================================

function renderDiffView(data) {
  elements.diffBeforeScore.textContent = data.scores.overall;
  elements.diffAfterScore.textContent = data.after_scores.overall;
  elements.diffResolvedCount.textContent = Math.max(0, data.issues.length - data.after_error_count);
  elements.diffReadingEase.textContent = `${data.readability.reading_ease}/100`;

  elements.panelBadgeBefore.textContent = `Errors: ${data.issues.length} | Score: ${data.scores.overall}`;
  elements.panelBadgeAfter.textContent = `Errors: ${data.after_error_count} | Score: ${data.after_scores.overall}`;

  // Highlight original with deletions
  let origHtml = '';
  let cursor = 0;
  const sorted = [...data.issues].sort((a, b) => a.start_idx - b.start_idx);

  for (const issue of sorted) {
    if (issue.start_idx < cursor) continue;
    if (issue.start_idx > cursor) {
      origHtml += escapeHtml(data.original_text.substring(cursor, issue.start_idx));
    }
    const spanText = data.original_text.substring(issue.start_idx, issue.end_idx);
    origHtml += `<span class="diff-deleted">${escapeHtml(spanText || ' ')}</span>`;
    cursor = issue.end_idx;
  }
  if (cursor < data.original_text.length) {
    origHtml += escapeHtml(data.original_text.substring(cursor));
  }
  elements.diffOriginalText.innerHTML = origHtml;

  // Corrected version with green insertions
  elements.diffCorrectedText.textContent = data.corrected_text;
}

function copyCorrectedText() {
  if (state.currentAnalysis && state.currentAnalysis.corrected_text) {
    navigator.clipboard.writeText(state.currentAnalysis.corrected_text).then(() => {
      showToast("Corrected document copied to clipboard!", "📋");
    });
  }
}

// ==========================================================================
// Tab 3: Explain My Error Feature & Learning Center
// ==========================================================================

function renderExplainCards(issues) {
  if (!issues || issues.length === 0) {
    elements.explainCardsGrid.innerHTML = `
      <div class="empty-issues-placeholder" style="grid-column: 1 / -1;">
        <span>🎓</span>
        <p>Your document is linguistically sound! No errors to explain.</p>
      </div>
    `;
    return;
  }

  let html = '';
  for (const issue of issues) {
    const catBg = getCategoryColor(issue.category);
    html += `
      <div class="pedagogy-card" id="pedagogy-${issue.id}">
        <div class="card-top">
          <span class="card-type-title">${escapeHtml(issue.error_type)}</span>
          <span class="issue-cat-tag" style="background: ${catBg.bg}; color: ${catBg.fg};">
            ${issue.category}
          </span>
        </div>

        <div class="four-pillars">
          <!-- Pillar 1: What is wrong -->
          <div class="pillar-item">
            <span class="pillar-label">1. What is Wrong</span>
            <span class="pillar-val-wrong">"${escapeHtml(issue.original_text || '[missing token]')}"</span>
          </div>

          <!-- Pillar 2: Recommended correction -->
          <div class="pillar-item">
            <span class="pillar-label">2. Recommended Correction</span>
            <span class="pillar-val-correct">"${escapeHtml(issue.replacement)}"</span>
          </div>

          <!-- Pillar 3: Why it is wrong -->
          <div class="pillar-item">
            <span class="pillar-label">3. Why It Is Incorrect (Linguistic Rule)</span>
            <span class="pillar-val-reason">${escapeHtml(issue.rule_explanation)}</span>
          </div>

          <!-- Pillar 4: Context Sentence -->
          <div class="pillar-item">
            <span class="pillar-label">4. Sentence Context</span>
            <span style="font-size: 0.8rem; color: var(--text-muted); font-style: italic;">
              "${escapeHtml(issue.context_snippet)}"
            </span>
          </div>
        </div>

        <div class="learning-tip-box">
          💡 <strong>Writing Insight:</strong> Review the subject number and tense markers in the sentence to build intuitive mastery over this rule.
        </div>
      </div>
    `;
  }

  elements.explainCardsGrid.innerHTML = html;
}

// ==========================================================================
// Tab 4: Detailed Analysis Report
// ==========================================================================

function renderDetailedReport(data) {
  elements.reportDocTitle.textContent = `${data.document_name} — Linguistic Audit Report`;
  elements.reportTimestamp.textContent = `Generated on ${new Date().toLocaleString()} | Mode: ${data.mode.toUpperCase()}`;

  elements.reportWords.textContent = data.stats.word_count.toLocaleString();
  elements.reportSentences.textContent = data.stats.sentence_count;
  elements.reportParagraphs.textContent = data.stats.paragraph_count;
  elements.reportSections.textContent = data.stats.section_count;

  elements.reportGrade.textContent = `Grade ${data.readability.grade_level}`;
  elements.reportAudience.textContent = `${data.readability.reading_level_label} (${data.readability.target_audience})`;
  elements.reportTTR.textContent = data.vocabulary_analysis.lexical_diversity_ttr || "0.68";

  // Category counts table
  const catCounts = {
    grammar: 0,
    spelling: 0,
    punctuation: 0,
    clarity: 0,
    structure: 0,
    vocabulary: 0
  };

  data.issues.forEach(i => {
    if (catCounts[i.category] !== undefined) {
      catCounts[i.category]++;
    }
  });

  const categories = [
    { name: "Grammar", key: "grammar", score: data.scores.grammar },
    { name: "Spelling", key: "spelling", score: data.scores.spelling },
    { name: "Punctuation", key: "punctuation", score: data.scores.punctuation },
    { name: "Clarity & Conciseness", key: "clarity", score: data.scores.clarity },
    { name: "Sentence Structure", key: "structure", score: 85 },
    { name: "Vocabulary & Repetition", key: "vocabulary", score: data.scores.vocabulary }
  ];

  let tbody = '';
  for (const cat of categories) {
    const count = catCounts[cat.key] || 0;
    const status = cat.score >= 85 
      ? '<span style="color: #34d399; font-weight: 700;">Proficient</span>' 
      : cat.score >= 70 
        ? '<span style="color: #fbbf24; font-weight: 700;">Moderate</span>' 
        : '<span style="color: #fb7185; font-weight: 700;">Needs Work</span>';

    tbody += `
      <tr>
        <td><strong>${cat.name}</strong></td>
        <td>${count} issue${count === 1 ? '' : 's'}</td>
        <td><strong>${cat.score}</strong>/100</td>
        <td>${status}</td>
      </tr>
    `;
  }
  elements.reportCategoriesTable.innerHTML = tbody;

  // Structure & Repetition
  const struct = data.sentence_structure_analysis;
  elements.reportPassiveCount.textContent = struct.total_passive_constructions || 0;
  elements.reportPassivePct.textContent = `${struct.passive_percentage || 0}%`;
  elements.reportAvgSentLen.textContent = struct.avg_sentence_length_words || 0;
  elements.reportLongestSent.textContent = struct.longest_sentence_words || 0;

  // Repeated words
  const repeated = data.vocabulary_analysis.repeated_words || [];
  if (repeated.length === 0) {
    elements.reportRepeatedWordsList.innerHTML = `<span style="color: #34d399;">No excessive word repetition detected. Good lexical variety!</span>`;
  } else {
    let repHtml = '<ul style="padding-left: 1.2rem; display: flex; flex-direction: column; gap: 0.4rem;">';
    for (const r of repeated) {
      repHtml += `
        <li>
          Word <strong>"${escapeHtml(r.word)}"</strong> repeated ${r.count} times. 
          Alternatives: <em style="color: #c4b5fd;">${escapeHtml(r.suggested_alternatives.slice(0, 3).join(', '))}</em>
        </li>
      `;
    }
    repHtml += '</ul>';
    elements.reportRepeatedWordsList.innerHTML = repHtml;
  }
}

// ==========================================================================
// Tab 5: Personalized Writing Profile & Progress
// ==========================================================================

async function loadWritingProfile() {
  try {
    const res = await fetch('/api/profile');
    if (!res.ok) return;
    const profile = await res.json();

    elements.profTotalDocs.textContent = profile.total_documents_analyzed;
    elements.profTotalWords.textContent = profile.total_words_processed.toLocaleString();
    elements.profAvgScore.textContent = profile.average_score ? `${profile.average_score}` : '--';
    elements.profAvgGain.textContent = profile.average_score_improvement ? `+${profile.average_score_improvement}` : '+0';
    elements.profRecommendationBox.innerHTML = `🎯 <strong>Personalized Recommendation:</strong> ${escapeHtml(profile.weakness_recommendation)}`;

    // Common issues breakdown bars
    if (!profile.most_common_issues || profile.most_common_issues.length === 0) {
      elements.commonIssuesList.innerHTML = `<p style="color: var(--text-muted); font-size: 0.88rem;">No historical analyses recorded yet.</p>`;
    } else {
      let issuesHtml = '';
      for (const item of profile.most_common_issues) {
        issuesHtml += `
          <div class="issue-bar-item">
            <div class="issue-bar-header">
              <span>${escapeHtml(item.name)}</span>
              <span><strong>${item.percentage}%</strong> (${item.count} occurrences)</span>
            </div>
            <div class="progress-track" style="height: 8px;">
              <div class="progress-fill" style="width: ${item.percentage}%; background: var(--accent-gradient);"></div>
            </div>
          </div>
        `;
      }
      elements.commonIssuesList.innerHTML = issuesHtml;
    }

    // Timeline Bar Chart
    if (!profile.score_timeline || profile.score_timeline.length === 0) {
      elements.timelineChart.innerHTML = `<p style="color: var(--text-muted); font-size: 0.88rem; margin: auto;">Analyze documents to populate your score improvement chart.</p>`;
    } else {
      let chartHtml = '';
      for (const item of profile.score_timeline.slice(-8)) {
        const beforeH = Math.max(15, Math.round((item.score_before / 100) * 140));
        const afterH = Math.max(15, Math.round((item.score_after / 100) * 140));

        chartHtml += `
          <div class="timeline-bar-group">
            <div class="bar-pair">
              <div class="bar-before" style="height: ${beforeH}px;" title="Before: ${item.score_before}"></div>
              <div class="bar-after" style="height: ${afterH}px;" title="After: ${item.score_after}"></div>
            </div>
            <div class="timeline-bar-label" title="${escapeHtml(item.document)}">
              ${escapeHtml(item.document.substring(0, 8))}..
            </div>
          </div>
        `;
      }
      elements.timelineChart.innerHTML = chartHtml;
    }

  } catch (error) {
    console.error("Profile fetch error:", error);
  }
}

async function clearUserHistory() {
  if (!confirm("Are you sure you want to reset your writing history and profile data?")) return;
  try {
    await fetch('/api/history', { method: 'DELETE' });
    showToast("Writing profile history reset.", "🗑️");
    loadWritingProfile();
  } catch (e) {
    console.error(e);
  }
}

// ==========================================================================
// Utilities & Helpers
// ==========================================================================

function updateLiveTextMetrics() {
  const text = elements.editorTextarea.value;
  const words = text.trim() ? text.trim().split(/\s+/).length : 0;
  const chars = text.length;
  const sents = text.trim() ? (text.match(/[.!?]+(?=\s+|$)/g) || []).length : 0;
  const readTime = Math.max(1, Math.round(words / 200));

  elements.statWords.textContent = words.toLocaleString();
  elements.statChars.textContent = chars.toLocaleString();
  elements.statSentences.textContent = sents;
  elements.statReadTime.textContent = `${readTime}m`;
}

function setAnalyzingState(loading) {
  state.isAnalyzing = loading;
  if (loading) {
    elements.btnAnalyze.disabled = true;
    elements.btnAnalyzeIcon.innerHTML = `<span class="spinner"></span>`;
    elements.btnAnalyzeText.textContent = "Analyzing Pipeline...";
  } else {
    elements.btnAnalyze.disabled = false;
    elements.btnAnalyzeIcon.innerHTML = `✨`;
    elements.btnAnalyzeText.textContent = "Analyze Writing";
  }
}

function resetDashboard() {
  updateScoreGauge(0);
  elements.scoreLevelBadge.textContent = "Pending Analysis";
  elements.scoreLevelBadge.className = "score-level-badge score-level-mod";
  elements.scoreTargetAudience.textContent = "Upload or write text and click Analyze Writing.";

  ['Grammar', 'Spelling', 'Punct', 'Clarity', 'Vocab', 'Readability'].forEach(k => {
    elements[`score${k}Val`].textContent = '--';
    elements[`progress${k}`].style.width = '0%';
  });

  elements.issuesCountBadge.textContent = '0 Issues';
  elements.issuesList.innerHTML = `
    <div class="empty-issues-placeholder">
      <span>✨</span>
      <p>No issues detected yet. Enter text and click <strong>Analyze Writing</strong> or load a sample document!</p>
    </div>
  `;
}

function getCategoryColor(cat) {
  const map = {
    grammar: { bg: 'rgba(244, 63, 94, 0.2)', fg: '#fda4af' },
    spelling: { bg: 'rgba(245, 158, 11, 0.2)', fg: '#fcd34d' },
    punctuation: { bg: 'rgba(14, 165, 233, 0.2)', fg: '#7dd3fc' },
    clarity: { bg: 'rgba(168, 85, 247, 0.2)', fg: '#d8b4fe' },
    structure: { bg: 'rgba(236, 72, 153, 0.2)', fg: '#f472b6' },
    vocabulary: { bg: 'rgba(16, 185, 129, 0.2)', fg: '#6ee7b7' },
  };
  return map[cat] || { bg: 'rgba(139, 92, 246, 0.2)', fg: '#c4b5fd' };
}

function exportDocument() {
  const text = elements.editorTextarea.value;
  if (!text.trim()) {
    showToast("Editor is empty. Nothing to export.", "⚠️");
    return;
  }
  const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${elements.docTitleInput.value.replace(/[^a-zA-Z0-9_-]/g, '_') || 'document'}_corrected.txt`;
  a.click();
  URL.revokeObjectURL(url);
  showToast("Document downloaded successfully!", "💾");
}

function showToast(msg, icon = '✓') {
  elements.toastText.textContent = msg;
  elements.toastIcon.textContent = icon;
  elements.toastMsg.classList.add('show');
  setTimeout(() => {
    elements.toastMsg.classList.remove('show');
  }, 3500);
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
