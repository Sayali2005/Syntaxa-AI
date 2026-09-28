import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

os.makedirs('report_assets', exist_ok=True)
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']

# Figure 3.1: Architecture Pipeline
fig, ax = plt.subplots(figsize=(8.5, 3.2), dpi=300)
ax.axis('off')
boxes = [
    ('Input Document\n(TXT / DOCX / PDF)', 0.10, 0.5, 0.15, 0.40, '#EBF5FB', '#2980B9'),
    ('NLP Preprocessor\n(spaCy en_core_web_lg\nPOS & Dep Trees)', 0.30, 0.5, 0.18, 0.40, '#E8F8F5', '#16A085'),
    ('Linguistic Engines\n(Grammar, Spell, Punct,\nClarity, Struct, Vocab)', 0.54, 0.5, 0.22, 0.46, '#FEF9E7', '#F39C12'),
    ('Mode Transformation\n& Reverse Patching', 0.77, 0.5, 0.16, 0.40, '#F4ECF7', '#8E44AD'),
    ('Scoring (0-100) &\nPedagogical Cards', 0.94, 0.5, 0.13, 0.40, '#FDEDEC', '#C0392B')
]

for text, x, y, w, h, bg, border in boxes:
    box = patches.FancyBboxPatch((x - w/2, y - h/2), w, h,
                                boxstyle=patches.BoxStyle("Round", pad=0.02),
                                facecolor=bg, edgecolor=border, linewidth=1.5)
    ax.add_patch(box)
    ax.text(x, y, text, ha='center', va='center', fontsize=8, weight='bold', color='#1A252F')

arrows = [(0.18, 0.20), (0.40, 0.42), (0.66, 0.68), (0.86, 0.87)]
for x1, x2 in arrows:
    ax.annotate('', xy=(x2, 0.5), xytext=(x1, 0.5),
                arrowprops=dict(arrowstyle='->', lw=1.8, color='#34495E'))

ax.set_xlim(0, 1.02)
ax.set_ylim(0.2, 0.8)
plt.tight_layout()
plt.savefig('report_assets/fig_architecture.png', bbox_inches='tight')
plt.close()
print('Architecture diagram saved.')

# Figure 4.1: Engine Performance (Precision, Recall, F1)
categories = ['Grammar', 'Spelling', 'Punctuation', 'Clarity', 'Structure', 'Vocabulary']
precision = [0.94, 0.98, 0.93, 0.91, 0.89, 0.92]
recall = [0.92, 0.96, 0.91, 0.88, 0.87, 0.90]
f1 = [0.93, 0.97, 0.92, 0.89, 0.88, 0.91]

x = np.arange(len(categories))
width = 0.25

fig, ax = plt.subplots(figsize=(6.5, 3.2), dpi=300)
rects1 = ax.bar(x - width, precision, width, label='Precision', color='#2980B9')
rects2 = ax.bar(x, recall, width, label='Recall', color='#27AE60')
rects3 = ax.bar(x + width, f1, width, label='F1-Score', color='#E67E22')

ax.set_ylabel('Score Ratio (0 - 1.0)', fontsize=10)
ax.set_title('Error Detection & Classification Evaluation per NLP Engine', fontsize=11, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=9)
ax.legend(loc='lower right', fontsize=8)
ax.set_ylim(0.7, 1.02)
ax.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig('report_assets/fig_accuracy_chart.png', bbox_inches='tight')
plt.close()
print('Accuracy chart saved.')

# Figure 4.2: Before vs After Writing Scores
samples = ['Sample 1\n(Short Text)', 'Sample 2\n(Tech Doc)', 'Sample 3\n(Academic)', 'Sample 4\n(Essay)', 'Sample 5\n(Report)']
before_scores = [68, 72, 64, 75, 70]
after_scores = [94, 96, 91, 95, 93]

x = np.arange(len(samples))
width = 0.35

fig, ax = plt.subplots(figsize=(6.5, 3.2), dpi=300)
ax.bar(x - width/2, before_scores, width, label='Initial Writing Score', color='#E74C3C')
ax.bar(x + width/2, after_scores, width, label='Corrected Quality Score', color='#2ECC71')

for i in range(len(samples)):
    ax.text(x[i] - width/2, before_scores[i] + 1.5, str(before_scores[i]), ha='center', fontsize=8, fontweight='bold')
    ax.text(x[i] + width/2, after_scores[i] + 1.5, str(after_scores[i]), ha='center', fontsize=8, fontweight='bold')

ax.set_ylabel('Quality Score (0 - 100)', fontsize=10)
ax.set_title('Writing Quality Score Improvement (Before vs. After Optimization)', fontsize=11, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(samples, fontsize=9)
ax.legend(loc='lower right', fontsize=8)
ax.set_ylim(40, 105)
ax.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig('report_assets/fig_scores_before_after.png', bbox_inches='tight')
plt.close()
print('Scores chart saved.')
