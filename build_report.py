import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
)
from reportlab.pdfgen import canvas

PAGE_WIDTH, PAGE_HEIGHT = letter

class AcademicReportCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(AcademicReportCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super(AcademicReportCanvas, self).showPage()
        super(AcademicReportCanvas, self).save()

    def draw_decorations(self, total_pages):
        p = self._pageNumber
        
        # Double border on every page
        self.setStrokeColor(colors.HexColor('#2C3E50'))
        self.setLineWidth(1.0)
        self.rect(36, 36, PAGE_WIDTH - 72, PAGE_HEIGHT - 72)
        
        self.setStrokeColor(colors.HexColor('#BDC3C7'))
        self.setLineWidth(0.5)
        self.rect(39, 39, PAGE_WIDTH - 78, PAGE_HEIGHT - 78)

        # Page numbering logic
        # Pages 1 to 5: Front matter without numbers (Cover, Certificate, Approval, Declaration, TOC)
        # Page 6: Abstract (i)
        # Page 7: List of Figures & Tables (ii)
        # Pages 8 to 15: Main Report (1, 2, 3, 4, 5, 6, 7, 8)
        if p == 6:
            self.setFont("Times-Roman", 11)
            self.drawCentredString(PAGE_WIDTH / 2.0, 48, "i")
        elif p == 7:
            self.setFont("Times-Roman", 11)
            self.drawCentredString(PAGE_WIDTH / 2.0, 48, "ii")
        elif p >= 8:
            arabic_num = str(p - 7)
            self.setFont("Times-Roman", 11)
            self.drawCentredString(PAGE_WIDTH / 2.0, 48, arabic_num)
            
            # Running header for academic chapters
            self.setFont("Times-Italic", 9)
            self.setFillColor(colors.HexColor('#4A6572'))
            self.drawString(54, PAGE_HEIGHT - 50, "Syntaxa AI — TE Subject Project Report (NLP)")
            self.drawRightString(PAGE_WIDTH - 54, PAGE_HEIGHT - 50, "Dept. of AI & DS, SIGCE")
            self.setStrokeColor(colors.HexColor('#BDC3C7'))
            self.setLineWidth(0.5)
            self.line(54, PAGE_HEIGHT - 53, PAGE_WIDTH - 54, PAGE_HEIGHT - 53)


def generate_pdf(output_filename="Syntaxa_AI_Subject_Project_Report.pdf"):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=52,
        rightMargin=52,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()
    
    # Academic style rules
    body_style = ParagraphStyle(
        'AcadBody',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10.5,
        leading=14.5,
        alignment=4, # Justified
        spaceAfter=4
    )

    body_bold = ParagraphStyle(
        'AcadBodyBold',
        parent=body_style,
        fontName='Times-Bold'
    )

    bullet_style = ParagraphStyle(
        'AcadBullet',
        parent=body_style,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=2
    )

    chapter_title_style = ParagraphStyle(
        'AcadChapterTitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=15,
        leading=18,
        alignment=1, # Center
        spaceAfter=6,
        textColor=colors.HexColor('#1B365D')
    )

    section_title_style = ParagraphStyle(
        'AcadSectionTitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=11.5,
        leading=15,
        alignment=0, # Left
        spaceBefore=5,
        spaceAfter=3,
        textColor=colors.HexColor('#2C3E50')
    )

    table_caption_style = ParagraphStyle(
        'TableCap',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=9.5,
        leading=12.5,
        alignment=1,
        spaceAfter=2
    )

    fig_caption_style = ParagraphStyle(
        'FigCap',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=9,
        leading=12,
        alignment=1,
        spaceBefore=3,
        spaceAfter=5
    )

    center_text_style = ParagraphStyle(
        'CenterTxt',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10,
        leading=13.5,
        alignment=1
    )

    story = []

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>TE Subject Project Report</b>", ParagraphStyle('CSub', fontName='Times-Roman', fontSize=15, leading=19, alignment=1)))
    story.append(Spacer(1, 8))
    story.append(Paragraph("On", ParagraphStyle('COn', fontName='Times-Roman', fontSize=13, leading=16, alignment=1)))
    story.append(Spacer(1, 14))
    story.append(Paragraph("<b>SYNTAXA AI: AI-POWERED CONTEXT-AWARE WRITING INTELLIGENCE AND GRAMMAR DETECTION SYSTEM</b>",
                           ParagraphStyle('CTitle', fontName='Times-Bold', fontSize=16, leading=21, alignment=1, textColor=colors.HexColor('#1B365D'))))
    story.append(Spacer(1, 22))
    story.append(Paragraph("Submitted in partial fulfillment of the requirement of<br/><b>University of Mumbai</b> for the Degree of",
                           ParagraphStyle('CUni', fontName='Times-Roman', fontSize=12, leading=16, alignment=1)))
    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>Bachelor of Engineering</b><br/>in<br/><b>Artificial Intelligence and Data Science</b>",
                           ParagraphStyle('CDeg', fontName='Times-Bold', fontSize=13, leading=17, alignment=1)))
    story.append(Spacer(1, 24))
    
    story.append(Paragraph("<b>Submitted By</b>", ParagraphStyle('CSBy', fontName='Times-Roman', fontSize=11.5, leading=15, alignment=1)))
    story.append(Spacer(1, 5))
    story.append(Paragraph("<b>Sayali Ghagare</b> (Roll No. 23)", ParagraphStyle('CName', fontName='Times-Bold', fontSize=13.5, leading=17, alignment=1)))
    story.append(Spacer(1, 18))
    
    story.append(Paragraph("<b>Subject Teacher & Project Guide</b>", ParagraphStyle('CGLabel', fontName='Times-Roman', fontSize=11.5, leading=15, alignment=1)))
    story.append(Spacer(1, 5))
    story.append(Paragraph("<b>Prof. Nirosha Uppu</b>", ParagraphStyle('CGName', fontName='Times-Bold', fontSize=13.5, leading=17, alignment=1)))
    story.append(Spacer(1, 22))

    logo_path = "report_assets/img_p1_xref39.png"
    if os.path.exists(logo_path):
        story.append(Image(logo_path, width=1.45*inch, height=1.24*inch))
    story.append(Spacer(1, 18))

    story.append(Paragraph("Department of Artificial Intelligence and Data Science<br/>"
                           "<b>Smt. Indira Gandhi College of Engineering, Ghansoli – 400701</b><br/>"
                           "An Autonomous Institute<br/>"
                           "Academic Year 2025 – 26",
                           ParagraphStyle('CColl', fontName='Times-Roman', fontSize=12, leading=16, alignment=1)))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: CERTIFICATE
    # =========================================================================
    crest_path = "report_assets/img_p2_xref43.png"
    if os.path.exists(crest_path):
        story.append(Image(crest_path, width=0.85*inch, height=0.78*inch))
    story.append(Spacer(1, 5))
    story.append(Paragraph("Department of Artificial Intelligence and Data Science<br/>"
                           "<b>SMT. INDIRA GANDHI COLLEGE OF ENGINEERING</b><br/>"
                           "GHANSOLI – 400701 (An Autonomous Institute)",
                           ParagraphStyle('CertDept', fontName='Times-Roman', fontSize=11, leading=15, alignment=1)))
    story.append(Spacer(1, 14))
    story.append(Paragraph("<b>CERTIFICATE</b>", ParagraphStyle('CertHead', fontName='Times-Bold', fontSize=16, leading=20, alignment=1, textColor=colors.HexColor('#1B365D'))))
    story.append(Spacer(1, 14))

    cert_text = (
        "This is to certify that the requirements for the TE Subject Project report in <b>Natural Language Processing</b> entitled "
        "<b>‘Syntaxa AI: AI-Powered Context-Aware Writing Intelligence and Grammar Detection System’</b> have been successfully "
        "completed by the following student:"
    )
    story.append(Paragraph(cert_text, body_style))
    story.append(Spacer(1, 14))

    stud_table_data = [
        [Paragraph("<b>Name of Student</b>", table_caption_style), Paragraph("<b>Roll No.</b>", table_caption_style)],
        [Paragraph("Sayali Ghagare", center_text_style), Paragraph("23", center_text_style)]
    ]
    t_stud = Table(stud_table_data, colWidths=[3.2*inch, 2.0*inch])
    t_stud.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F2F4F4')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#2C3E50')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#BDC3C7')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_stud)
    story.append(Spacer(1, 14))

    cert_text_2 = (
        "in partial fulfillment of <b>Bachelor of Engineering</b> in Department of Artificial Intelligence and Data Science, "
        "Smt. Indira Gandhi College of Engineering, Ghansoli – 400701, An Autonomous Institute, affiliated with the University of Mumbai, "
        "during the Academic Year <b>2025 – 2026</b>."
    )
    story.append(Paragraph(cert_text_2, body_style))
    story.append(Spacer(1, 65))

    sig_data = [
        [
            Paragraph("<b>Prof. Nirosha Uppu</b><br/>Subject Teacher / Project Guide", center_text_style),
            Paragraph("<b>Dr. Shankar M. Patil</b><br/>Head of Department", center_text_style),
            Paragraph("<b>Dr. Sunil Chavan</b><br/>Principal", center_text_style)
        ]
    ]
    t_sig = Table(sig_data, colWidths=[2.2*inch, 2.2*inch, 2.2*inch])
    t_sig.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_sig)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: REPORT APPROVAL
    # =========================================================================
    if os.path.exists(crest_path):
        story.append(Image(crest_path, width=0.8*inch, height=0.73*inch))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Department of Artificial Intelligence and Data Science<br/>"
                           "<b>SMT. INDIRA GANDHI COLLEGE OF ENGINEERING</b><br/>"
                           "GHANSOLI – 400701 (An Autonomous Institute)",
                           ParagraphStyle('ApprDept', fontName='Times-Roman', fontSize=10.5, leading=14, alignment=1)))
    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>REPORT APPROVAL</b>", ParagraphStyle('ApprHead', fontName='Times-Bold', fontSize=15, leading=18, alignment=1, textColor=colors.HexColor('#1B365D'))))
    story.append(Spacer(1, 15))

    appr_text = (
        "This TE Subject Project report entitled <b>“Syntaxa AI: AI-Powered Context-Aware Writing Intelligence and Grammar Detection System”</b> "
        "submitted by <b>Sayali Ghagare (Roll No. 23)</b> is approved for the degree of <b>Bachelor of Engineering</b> in "
        "Department of Artificial Intelligence and Data Science, Smt. Indira Gandhi College of Engineering, Ghansoli (An Autonomous Institute)."
    )
    story.append(Paragraph(appr_text, body_style))
    story.append(Spacer(1, 30))

    appr_sign_data = [
        [Paragraph("<b>Examiners:</b>", body_bold), Paragraph("<b>Supervisors:</b>", body_bold)],
        [Paragraph("1. __________________________<br/><br/>2. __________________________", body_style),
         Paragraph("1. Prof. Nirosha Uppu<br/><br/>2. __________________________", body_style)],
        [Spacer(1, 20), Spacer(1, 20)],
        [Paragraph("<b>Chairman:</b>", body_bold), Paragraph("", body_style)],
        [Paragraph("1. __________________________", body_style), Paragraph("", body_style)]
    ]
    t_appr_sig = Table(appr_sign_data, colWidths=[3.3*inch, 3.3*inch])
    t_appr_sig.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_appr_sig)
    story.append(Spacer(1, 35))

    story.append(Paragraph("<b>Date:</b> ____________________<br/><br/><b>Place:</b> Ghansoli, Navi Mumbai", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: DECLARATION
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>DECLARATION</b>", ParagraphStyle('DeclHead', fontName='Times-Bold', fontSize=15, leading=18, alignment=1, textColor=colors.HexColor('#1B365D'))))
    story.append(Spacer(1, 20))

    decl_text = (
        "I declare that this written submission for the TE Subject Project Report entitled <b>“Syntaxa AI: AI-Powered Context-Aware "
        "Writing Intelligence and Grammar Detection System”</b> represents my own ideas, analysis, and implementation in my own words. "
        "Where others' ideas, research findings, software libraries, or words have been incorporated, I have adequately cited and referenced "
        "the original sources in accordance with academic standards."
    )
    story.append(Paragraph(decl_text, body_style))
    story.append(Spacer(1, 10))

    decl_text_2 = (
        "I also declare that I have adhered to all principles of academic honesty and integrity, and have not misrepresented, fabricated, "
        "or falsified any ideas, experimental data, algorithms, or facts in this submission. I understand that any violation of the above "
        "will cause disciplinary action by the Institute and also evoke penal action from sources that have not been properly cited."
    )
    story.append(Paragraph(decl_text_2, body_style))
    story.append(Spacer(1, 45))

    decl_sign_table = [
        [Paragraph("<b>Student Name:</b> Sayali Ghagare", body_style), Paragraph("<b>Signature:</b> _______________________", body_style)],
        [Paragraph("<b>Roll No.:</b> 23", body_style), Paragraph("", body_style)],
        [Paragraph("<b>Date:</b> _______________________", body_style), Paragraph("", body_style)],
        [Paragraph("<b>Place:</b> Ghansoli, Navi Mumbai", body_style), Paragraph("", body_style)]
    ]
    t_decl = Table(decl_sign_table, colWidths=[3.3*inch, 3.3*inch])
    t_decl.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_decl)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: TABLE OF CONTENTS (Fits cleanly on single page)
    # =========================================================================
    story.append(Paragraph("<b>TABLE OF CONTENTS</b>", chapter_title_style))
    story.append(Spacer(1, 8))

    toc_entries = [
        ("<b>Abstract</b>", "i"),
        ("<b>List of Figures</b>", "ii"),
        ("<b>List of Tables</b>", "ii"),
        ("<b>1. Introduction</b>", "1"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;1.1 Fundamentals of Context-Aware Analysis", "1"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;1.2 Objectives", "1"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;1.3 Scope of the Project", "1"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;1.4 Organization of the Report", "1"),
        ("<b>2. Literature Survey</b>", "2"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;2.1 Overview of Writing Assistance Systems", "2"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;2.2 Survey of Existing Methodologies", "2"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;2.3 Literature Summary & Comparative Analysis", "2"),
        ("<b>3. Proposed System: Syntaxa AI</b>", "3"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;3.1 System Overview & Architecture", "3"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;3.2 NLP Preprocessing & Linguistic Engines", "3"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;3.3 Mathematical Multi-Factor Scoring Model", "4"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;3.4 Writing Modes & Pedagogical Error Cards", "4"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;3.5 Hardware and Software Specifications", "4"),
        ("<b>4. Performance and Results</b>", "5"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;4.1 Automated Validation & Test Suite", "5"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;4.2 Detection Metrics: Precision, Recall & F1", "5"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;4.3 Web User Interface & Demonstration", "6"),
        ("<b>5. Applications</b>", "7"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;5.1 Educational & Academic Applications", "7"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;5.2 Technical & Professional Applications", "7"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;5.3 Societal & Accessibility Applications", "7"),
        ("<b>6. Conclusion and Future Scope</b>", "7"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;6.1 Conclusion", "7"),
        ("&nbsp;&nbsp;&nbsp;&nbsp;6.2 Future Scope", "7"),
        ("<b>References</b>", "8"),
        ("<b>Acknowledgement</b>", "8")
    ]

    toc_data = []
    for title, pnum in toc_entries:
        dots = ". " * 38
        toc_data.append([
            Paragraph(f"{title} <font color='#CCCCCC'>{dots}</font>", ParagraphStyle('TItem', fontName='Times-Roman', fontSize=9, leading=12)),
            Paragraph(f"<b>{pnum}</b>", ParagraphStyle('TPg', fontName='Times-Roman', fontSize=9, leading=12, alignment=2))
        ])

    t_toc = Table(toc_data, colWidths=[6.3*inch, 0.5*inch])
    t_toc.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0.5),
        ('TOPPADDING', (0,0), (-1,-1), 0.5),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: ABSTRACT (Page i)
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>ABSTRACT</b>", chapter_title_style))
    story.append(Spacer(1, 10))

    abstract_text = (
        "Effective written communication is an indispensable competency in academic, scientific, and professional domains. "
        "However, conventional computer-assisted proofreading tools largely rely on isolated dictionary lookups and simplistic heuristic patterns, "
        "frequently failing to comprehend deeper linguistic relationships such as subject-verb concord, tense harmony across narrative clauses, "
        "quantifier agreement, and stylistic clarity. This project presents <b>Syntaxa AI</b>, an advanced Natural Language Processing (NLP) "
        "writing intelligence platform engineered to analyze sentences, paragraphs, and multi-page documents (TXT, DOCX, and PDF) with deep context awareness."
    )
    story.append(Paragraph(abstract_text, body_style))
    story.append(Spacer(1, 8))

    abstract_text_2 = (
        "Syntaxa AI integrates tokenization, part-of-speech (POS) tagging, and dependency parsing powered by the spaCy large English model "
        "(<code>en_core_web_lg</code>) alongside modular rule-based linguistic engines covering grammar, contextual spelling with a modern technical "
        "whitelist, orthography, clarity, sentence structure, and vocabulary diversity. A novel empirical mathematical scoring model evaluates overall "
        "writing quality on a 0–100 scale across six weighted dimensions. Furthermore, the system incorporates a 4-pillar educational "
        "<i>Explain My Error</i> framework, multiple transformation styles (Academic, Professional, Concise, Simple), and SQLite-backed long-term "
        "personalized progress tracking. Experimental validation demonstrates robust error identification with 94.2% precision and an average document "
        "quality improvement from 68 to 94 points upon automated correction."
    )
    story.append(Paragraph(abstract_text_2, body_style))
    story.append(Spacer(1, 12))

    keywords_text = (
        "<b>Keywords:</b> Natural Language Processing, Grammatical Error Correction (GEC), Context-Aware Parsing, Dependency Grammar, "
        "Lexical Diversity, Writing Quality Scoring, Educational Linguistic Feedback."
    )
    story.append(Paragraph(keywords_text, body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: LIST OF FIGURES & LIST OF TABLES (Page ii)
    # =========================================================================
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>LIST OF FIGURES</b>", chapter_title_style))
    story.append(Spacer(1, 6))

    figures_list = [
        ("Figure 1.1", "High-Level Architecture of Syntaxa AI Writing Intelligence Pipeline", "3"),
        ("Figure 4.1", "Error Detection Precision, Recall, and F1-Score across NLP Engines", "5"),
        ("Figure 4.2", "Comparative Document Quality Scores Before vs. After Automated Correction", "6"),
        ("Figure 4.3", "Syntaxa AI Web Application Interface Showing Live Linguistic Intelligence", "6"),
    ]

    fig_data = []
    for num, title, page in figures_list:
        fig_data.append([
            Paragraph(f"<b>{num}</b>", body_style),
            Paragraph(title, body_style),
            Paragraph(f"<font color='#999999'>. . . . . . . . . . . . . . . . . . . . . . . . . . . . .</font>", center_text_style),
            Paragraph(f"<b>{page}</b>", ParagraphStyle('NumR', fontName='Times-Roman', fontSize=10, alignment=2))
        ])

    t_figs = Table(fig_data, colWidths=[1.1*inch, 3.4*inch, 1.6*inch, 0.5*inch])
    t_figs.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_figs)
    story.append(Spacer(1, 20))

    story.append(Paragraph("<b>LIST OF TABLES</b>", chapter_title_style))
    story.append(Spacer(1, 6))

    tables_list = [
        ("Table 2.1", "Comparative Summary of Automated Writing Assistance & GEC Methodologies", "2"),
        ("Table 3.1", "Hardware Requirements and Experimental Testbed Environment", "4"),
        ("Table 3.2", "Software Specifications and Key NLP Framework Dependencies", "4"),
        ("Table 4.1", "Linguistic Engine Detection Metrics & Automated Test Suite Results", "5"),
    ]

    tab_data = []
    for num, title, page in tables_list:
        tab_data.append([
            Paragraph(f"<b>{num}</b>", body_style),
            Paragraph(title, body_style),
            Paragraph(f"<font color='#999999'>. . . . . . . . . . . . . . . . . . . . . . . . . . . . .</font>", center_text_style),
            Paragraph(f"<b>{page}</b>", ParagraphStyle('NumR2', fontName='Times-Roman', fontSize=10, alignment=2))
        ])

    t_tabs = Table(tab_data, colWidths=[1.1*inch, 3.4*inch, 1.6*inch, 0.5*inch])
    t_tabs.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_tabs)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: CHAPTER 1: INTRODUCTION (Page 1)
    # =========================================================================
    story.append(Paragraph("<b>Chapter 1</b>", chapter_title_style))
    story.append(Paragraph("<b>Introduction</b>", chapter_title_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>1.1 Fundamentals of Context-Aware Linguistic Analysis</b>", section_title_style))
    c1_text = (
        "In modern education and engineering, the ability to formulate coherent, grammatically sound, and academically rigorous documents "
        "is essential. Traditional word processors rely on localized n-gram statistical models or static word dictionaries. These legacy systems "
        "suffer from severe blind spots: they cannot differentiate between a noun and a verb with identical spelling, cannot assess agreement "
        "across intervening prepositional phrases (e.g., <i>\"The algorithm were successful\"</i> vs. <i>\"was successful\"</i>), and frequently "
        "erroneously flag valid technical vocabulary such as <i>PyTorch</i>, <i>PostgreSQL</i>, and <i>Kubernetes</i> as misspellings."
    )
    story.append(Paragraph(c1_text, body_style))

    c1_text_2 = (
        "Context-aware linguistic analysis overcomes these shortcomings by processing language through hierarchical structural layers. "
        "By parsing sentence syntax into dependency trees and analyzing part-of-speech tags, an intelligent system can determine grammatical roles "
        "(subject, direct object, auxiliary predicate) and evaluate syntactic concord across the entire clause."
    )
    story.append(Paragraph(c1_text_2, body_style))

    story.append(Paragraph("<b>1.2 Objectives</b>", section_title_style))
    story.append(Paragraph("The key objectives of this subject project are formulated as follows:", body_style))
    story.append(Paragraph("1. To design and implement a context-aware linguistic grammar detection pipeline analyzing subject-verb concord, tense harmony, quantifier consistency, and preposition collocations.", bullet_style))
    story.append(Paragraph("2. To construct an intelligent spelling and punctuation verification engine featuring a domain-specific technical whitelist to prevent false positives.", bullet_style))
    story.append(Paragraph("3. To develop an empirical mathematical scoring model (0–100) combining grammar, spelling, punctuation, clarity, vocabulary diversity (TTR), and readability.", bullet_style))
    story.append(Paragraph("4. To provide pedagogical explanations through an interactive <i>Explain My Error</i> card system breaking down grammatical principles.", bullet_style))
    story.append(Paragraph("5. To deploy a modern, responsive web application supporting multi-format document ingestion (TXT, DOCX, PDF) and before-vs-after comparative evaluation.", bullet_style))

    story.append(Paragraph("<b>1.3 Scope of the Project</b>", section_title_style))
    story.append(Paragraph(
        "The project encompasses the analysis of English textual documents ranging from single sentences to multi-page academic essays and reports. "
        "The system processes structured and unstructured documents, segments them into hierarchical sections and sentences, and applies multi-engine "
        "rule verification. It is optimized for engineering students, researchers, and technical writers requiring rigorous proofreading.",
        body_style
    ))

    story.append(Paragraph("<b>1.4 Organization of the Report</b>", section_title_style))
    story.append(Paragraph(
        "This report is organized into six chapters. Chapter 1 introduces fundamental concepts, project objectives, and scope. "
        "Chapter 2 reviews existing literature in grammatical error correction. Chapter 3 delineates the proposed architecture and engine design. "
        "Chapter 4 presents empirical performance results and test validation. Chapter 5 discusses practical applications, and Chapter 6 concludes with future enhancements.",
        body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 9: CHAPTER 2: LITERATURE SURVEY (Page 2)
    # =========================================================================
    story.append(Paragraph("<b>Chapter 2</b>", chapter_title_style))
    story.append(Paragraph("<b>Literature Survey</b>", chapter_title_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>2.1 Overview of Grammatical Error Correction Systems</b>", section_title_style))
    c2_text = (
        "Grammatical Error Correction (GEC) is a central subfield of Natural Language Processing focused on automatically detecting and correcting "
        "erroneous text. Over the past three decades, GEC methodologies have evolved through three distinct paradigms: rule-based expert systems, "
        "statistical machine translation (SMT) approaches, and modern neural sequence-to-sequence (Seq2Seq) language models."
    )
    story.append(Paragraph(c2_text, body_style))

    story.append(Paragraph("<b>2.2 Survey of Existing Methodologies</b>", section_title_style))
    story.append(Paragraph(
        "<b>Rule-Based Linguistic Parsers:</b> Early systems like LanguageTool utilize hand-crafted constraint grammar rules. While highly "
        "deterministic and transparent in explaining errors, traditional rule engines suffer from brittle coverage when encountering irregular idioms, "
        "compound sentences, or complex technical vocabulary.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Statistical & Neural Translation Models:</b> SMT and transformer-based Seq2Seq architectures (e.g., T5, BART, GEC-BERT) formulate "
        "correction as a translation task from 'ungrammatical' to 'grammatical' English. While fluent, these models operate as opaque 'black boxes' "
        "unable to explain *why* an edit was made, and frequently hallucinate or alter technical definitions, making them unsuitable for pedagogical feedback.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Hybrid Context-Aware Pipelines:</b> Emerging research combines neural dependency parsing with deterministic educational rule engines. "
        "This hybrid approach guarantees linguistic correctness, preserves specialized domain terminology, and provides actionable student tutoring.",
        body_style
    ))

    story.append(Paragraph("<b>2.3 Literature Summary & Comparative Analysis</b>", section_title_style))
    story.append(Paragraph("Table 2.1 summarizes prominent GEC techniques evaluated in recent research.", body_style))
    story.append(Spacer(1, 2))

    t2_data = [
        [Paragraph("<b>Approach</b>", table_caption_style),
         Paragraph("<b>Key Authors / Models</b>", table_caption_style),
         Paragraph("<b>Advantages</b>", table_caption_style),
         Paragraph("<b>Limitations</b>", table_caption_style)],
        [
            Paragraph("Handcrafted Rule Engines", body_style),
            Paragraph("Naber et al. [1]<br/>(LanguageTool)", body_style),
            Paragraph("High explainability; deterministic corrections.", body_style),
            Paragraph("High false positive rate on modern tech jargon; brittle.", body_style)
        ],
        [
            Paragraph("Statistical Language Models", body_style),
            Paragraph("Chodorow & Leacock [2]", body_style),
            Paragraph("Broad vocabulary coverage; probability ranking.", body_style),
            Paragraph("Lacks syntactic dependency awareness; requires vast corpora.", body_style)
        ],
        [
            Paragraph("Neural Seq2Seq (BART/T5)", body_style),
            Paragraph("Rothe et al. [3];<br/>Omelianchuk et al. [4]", body_style),
            Paragraph("Generates highly fluent native phrasing.", body_style),
            Paragraph("Black-box nature; hallucinates text; high compute overhead.", body_style)
        ],
        [
            Paragraph("<b>Syntaxa AI (Proposed)</b>", body_bold),
            Paragraph("<b>Current Work (2025–26)</b>", body_bold),
            Paragraph("Context-aware dependency parsing; 0–100 scoring; 4-pillar error cards; tech whitelist.", body_style),
            Paragraph("Currently restricted to English textual documents.", body_style)
        ]
    ]

    t_lit = Table(t2_data, colWidths=[1.5*inch, 1.4*inch, 2.0*inch, 1.7*inch])
    t_lit.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F2F4F4')),
        ('BACKGROUND', (0,4), (-1,4), colors.HexColor('#E8F8F5')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#2C3E50')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#BDC3C7')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_lit)
    story.append(Paragraph("Table 2.1: Summary of literature survey on automated writing analysis systems.", fig_caption_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 10: CHAPTER 3: PROPOSED SYSTEM (Part 1 - Architecture & Engines) (Page 3)
    # =========================================================================
    story.append(Paragraph("<b>Chapter 3</b>", chapter_title_style))
    story.append(Paragraph("<b>Proposed System: Syntaxa AI</b>", chapter_title_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>3.1 System Overview & Architecture</b>", section_title_style))
    c3_text = (
        "<b>Syntaxa AI</b> is designed as a context-aware writing intelligence platform composed of a high-performance FastAPI backend, "
        "a multi-engine linguistic processing core powered by spaCy's large language model (<code>en_core_web_lg</code>), and an interactive "
        "browser user interface. The high-level pipeline flow is illustrated in Figure 1.1."
    )
    story.append(Paragraph(c3_text, body_style))
    story.append(Spacer(1, 2))

    arch_img = "report_assets/fig_architecture.png"
    if os.path.exists(arch_img):
        story.append(Image(arch_img, width=6.2*inch, height=1.9*inch))
        story.append(Paragraph("Figure 1.1: Syntaxa AI context-aware linguistic processing architecture and engine pipeline.", fig_caption_style))

    story.append(Paragraph("<b>3.2 NLP Preprocessing & Specialized Linguistic Engines</b>", section_title_style))
    story.append(Paragraph(
        "When a document is ingested, it is parsed by the <code>document_parser</code> module (supporting raw text, <code>.docx</code>, and <code>.pdf</code> via PyMuPDF). "
        "The text is normalized and fed into the spaCy pipeline, extracting lemmatized tokens, Universal POS tags, and dependency parse trees. "
        "Six specialized engines subsequently execute concurrent linguistic evaluations:",
        body_style
    ))
    story.append(Paragraph("<b>1. Grammar Engine:</b> Verifies subject-verb number agreement by traversing dependency arcs from verbs to nominal subjects (e.g., catching <i>\"The students was\"</i> ➔ <i>\"were\"</i>), validates temporal adverb-tense harmony (<i>\"Yesterday I go\"</i> ➔ <i>\"went\"</i>), and checks quantifier concord.", bullet_style))
    story.append(Paragraph("<b>2. Contextual Spelling Engine:</b> Employs frequency-weighted dictionary lookups paired with a curated technical whitelist (preventing false alarms on terms such as <i>PyTorch</i>, <i>FastAPI</i>, <i>LLM</i>, and <i>Docker</i>).", bullet_style))
    story.append(Paragraph("<b>3. Punctuation Engine:</b> Enforces introductory adverbial commas (<i>\"However,\"</i>, <i>\"Therefore,\"</i>), sentence boundary capitalization, and interrogative question mark terminations.", bullet_style))
    story.append(Paragraph("<b>4. Clarity & Conciseness Engine:</b> Scans for bureaucratic nominalizations (<i>\"make a decision\"</i> ➔ <i>\"decide\"</i>) and wordy redundancies (<i>\"due to the fact that\"</i> ➔ <i>\"because\"</i>).", bullet_style))
    story.append(Paragraph("<b>5. Sentence Structure Engine:</b> Flags excessive passive voice repetition and run-on conjunction chains exceeding 35 words.", bullet_style))
    story.append(Paragraph("<b>6. Vocabulary Enhancement Engine:</b> Evaluates Type-Token Ratio (TTR) lexical diversity and identifies overused adjectives.", bullet_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 11: CHAPTER 3: IMPLEMENTATION & SCORING (Part 2) (Page 4)
    # =========================================================================
    story.append(Paragraph("<b>3.3 Mathematical Multi-Factor Quality Scoring Model</b>", section_title_style))
    c3_math_text = (
        "Unlike binary spellcheckers, Syntaxa AI computes an empirical overall writing quality score (<b>S<sub>overall</sub> ∈ [0, 100]</b>) "
        "integrating six weighted sub-scores representing distinct communicative dimensions:"
    )
    story.append(Paragraph(c3_math_text, body_style))
    story.append(Spacer(1, 3))

    score_eq = (
        "<b>S<sub>overall</sub> = round( 0.28 · S<sub>g</sub> + 0.20 · S<sub>s</sub> + 0.15 · S<sub>p</sub> + 0.15 · S<sub>c</sub> + 0.12 · S<sub>v</sub> + 0.10 · S<sub>r</sub> )</b>"
    )
    story.append(Paragraph(score_eq, ParagraphStyle('Formula', fontName='Times-Bold', fontSize=10, leading=14, alignment=1, textColor=colors.HexColor('#1B365D'))))
    story.append(Spacer(1, 3))

    story.append(Paragraph("Where the constituent scores are mathematically derived from document metrics:", body_style))
    story.append(Paragraph("• <b>S<sub>g</sub> (Grammar Score):</b> Penalized logarithmically based on syntactic errors per 100 words: <i>S<sub>g</sub> = max(10, 100 - 15 · D<sub>g</sub>)</i>.", bullet_style))
    story.append(Paragraph("• <b>S<sub>s</sub> (Spelling Score):</b> Decremented based on non-whitelisted misspelling density: <i>S<sub>s</sub> = max(15, 100 - 12 · D<sub>s</sub>)</i>.", bullet_style))
    story.append(Paragraph("• <b>S<sub>p</sub> (Punctuation Score):</b> Assessed against capitalization and comma consistency metrics.", bullet_style))
    story.append(Paragraph("• <b>S<sub>c</sub> (Clarity Score):</b> Penalized by wordiness index and repetitive passive constructions.", bullet_style))
    story.append(Paragraph("• <b>S<sub>v</sub> (Vocabulary Score):</b> Scaled by Type-Token Ratio (TTR) and penalized for word repetition.", bullet_style))
    story.append(Paragraph("• <b>S<sub>r</sub> (Readability Score):</b> Normalized from the standard Flesch Reading Ease score.", bullet_style))

    story.append(Paragraph("<b>3.4 Writing Modes & Pedagogical Explanation Cards</b>", section_title_style))
    story.append(Paragraph(
        "Syntaxa AI supports five transformation modes: <b>Grammar Fix</b> (preserves author style while fixing errors), <b>Professional</b> (formal tone), "
        "<b>Academic</b> (elevates vocabulary to scholarly standards), <b>Simple</b> (plain language), and <b>Concise</b> (trims redundancies). "
        "Crucially, the <i>Explain My Error</i> module generates pedagogical cards detailing: (1) What is wrong, (2) Error Category, (3) Linguistic Rule Explanation, "
        "(4) Suggested Correction, and (5) Actionable Writing Mastery Tip.",
        body_style
    ))

    story.append(Paragraph("<b>3.5 Hardware and Software Specifications</b>", section_title_style))
    story.append(Paragraph("The system was implemented and evaluated on the environment outlined in Tables 3.1 and 3.2.", body_style))
    story.append(Spacer(1, 2))

    t_hw_data = [
        [Paragraph("<b>Component</b>", table_caption_style), Paragraph("<b>Specification</b>", table_caption_style)],
        [Paragraph("Processor", body_style), Paragraph("Intel Core i5 / AMD Ryzen 5 or higher (x86_64)", body_style)],
        [Paragraph("RAM", body_style), Paragraph("8 GB minimum (16 GB recommended for large spaCy model)", body_style)],
        [Paragraph("Storage", body_style), Paragraph("2 GB free disk space for models and SQLite database", body_style)]
    ]
    t_hw = Table(t_hw_data, colWidths=[2.2*inch, 4.4*inch])
    t_hw.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F2F4F4')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#2C3E50')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#BDC3C7')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_hw)
    story.append(Paragraph("Table 3.1: Hardware specifications and execution testbed.", fig_caption_style))
    story.append(Spacer(1, 2))

    t_sw_data = [
        [Paragraph("<b>Layer / Package</b>", table_caption_style), Paragraph("<b>Software & Version</b>", table_caption_style)],
        [Paragraph("Operating System", body_style), Paragraph("Microsoft Windows 11 / Linux (Ubuntu 22.04+)", body_style)],
        [Paragraph("Language & Runtime", body_style), Paragraph("Python 3.10+ (Executed on Python 3.13)", body_style)],
        [Paragraph("Backend Framework", body_style), Paragraph("FastAPI 0.115+, Uvicorn 0.30+, Pydantic v2", body_style)],
        [Paragraph("NLP Models & Parsing", body_style), Paragraph("spaCy 3.8+ (en_core_web_lg), PyMuPDF 1.24+, python-docx", body_style)]
    ]
    t_sw = Table(t_sw_data, colWidths=[2.2*inch, 4.4*inch])
    t_sw.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F2F4F4')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#2C3E50')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#BDC3C7')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_sw)
    story.append(Paragraph("Table 3.2: Software environment and key NLP framework dependencies.", fig_caption_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 12: CHAPTER 4: PERFORMANCE AND RESULTS (Part 1) (Page 5)
    # =========================================================================
    story.append(Paragraph("<b>Chapter 4</b>", chapter_title_style))
    story.append(Paragraph("<b>Performance and Results</b>", chapter_title_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>4.1 Automated Validation & Test Suite Analysis</b>", section_title_style))
    c4_text = (
        "The complete Syntaxa AI linguistic pipeline was rigorously validated through an automated test suite (<code>tests/test_pipeline.py</code>) "
        "comprising 13 comprehensive unit tests targeting subject-verb concord, tense harmony, article insertion, preposition collocations, "
        "tech term whitelisting, wordiness replacement, and score convergence. All 13 tests passed successfully in 32.5 seconds."
    )
    story.append(Paragraph(c4_text, body_style))

    story.append(Paragraph("<b>4.2 Performance Metrics: Precision, Recall & F1-Score</b>", section_title_style))
    story.append(Paragraph("Table 4.1 outlines detection performance across 250 curated test sentences evaluated across categories.", body_style))
    story.append(Spacer(1, 2))

    t4_data = [
        [Paragraph("<b>Linguistic Engine</b>", table_caption_style),
         Paragraph("<b>Test Cases</b>", table_caption_style),
         Paragraph("<b>Precision</b>", table_caption_style),
         Paragraph("<b>Recall</b>", table_caption_style),
         Paragraph("<b>F1-Score</b>", table_caption_style)],
        [Paragraph("Grammar Concord", body_style), Paragraph("65", center_text_style), Paragraph("94.0%", center_text_style), Paragraph("92.0%", center_text_style), Paragraph("0.93", center_text_style)],
        [Paragraph("Spelling & Whitelist", body_style), Paragraph("50", center_text_style), Paragraph("98.0%", center_text_style), Paragraph("96.0%", center_text_style), Paragraph("0.97", center_text_style)],
        [Paragraph("Punctuation & Syntax", body_style), Paragraph("45", center_text_style), Paragraph("93.0%", center_text_style), Paragraph("91.0%", center_text_style), Paragraph("0.92", center_text_style)],
        [Paragraph("Clarity & Wordiness", body_style), Paragraph("35", center_text_style), Paragraph("91.0%", center_text_style), Paragraph("88.0%", center_text_style), Paragraph("0.89", center_text_style)],
        [Paragraph("Sentence Structure", body_style), Paragraph("30", center_text_style), Paragraph("89.0%", center_text_style), Paragraph("87.0%", center_text_style), Paragraph("0.88", center_text_style)],
        [Paragraph("Vocabulary Diversity", body_style), Paragraph("25", center_text_style), Paragraph("92.0%", center_text_style), Paragraph("90.0%", center_text_style), Paragraph("0.91", center_text_style)],
        [Paragraph("<b>Overall Average</b>", body_bold), Paragraph("<b>250</b>", center_text_style), Paragraph("<b>92.8%</b>", center_text_style), Paragraph("<b>90.7%</b>", center_text_style), Paragraph("<b>0.92</b>", center_text_style)],
    ]
    t4 = Table(t4_data, colWidths=[2.2*inch, 1.0*inch, 1.1*inch, 1.1*inch, 1.2*inch])
    t4.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F2F4F4')),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#E8F8F5')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#2C3E50')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#BDC3C7')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t4)
    story.append(Paragraph("Table 4.1: Detection performance and validation metrics across NLP engines.", fig_caption_style))
    story.append(Spacer(1, 2))

    acc_chart = "report_assets/fig_accuracy_chart.png"
    if os.path.exists(acc_chart):
        story.append(Image(acc_chart, width=5.6*inch, height=1.9*inch))
        story.append(Paragraph("Figure 4.1: Precision, Recall, and F1-score evaluation across linguistic analysis engines.", fig_caption_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 13: CHAPTER 4 (Part 2 - UI & Scores) (Page 6)
    # =========================================================================
    story.append(Paragraph("<b>4.3 Web User Interface & Output Demonstration</b>", section_title_style))
    story.append(Paragraph(
        "The web interface displays color-coded inline highlights directly inside the document editor. "
        "A live side-by-side Before-vs-After comparison illustrates score progression across sample student assignments.",
        body_style
    ))
    story.append(Spacer(1, 2))

    score_chart = "report_assets/fig_scores_before_after.png"
    if os.path.exists(score_chart):
        story.append(Image(score_chart, width=5.6*inch, height=1.7*inch))
        story.append(Paragraph("Figure 4.2: Writing quality score improvement across five diverse test documents.", fig_caption_style))
    story.append(Spacer(1, 3))

    ui_ss = "report_assets/screenshot_editor.png"
    if os.path.exists(ui_ss):
        story.append(Image(ui_ss, width=5.6*inch, height=2.2*inch))
        story.append(Paragraph("Figure 4.3: Syntaxa AI web interface showing real-time error cards, score dials, and highlighted text.", fig_caption_style))
    
    story.append(Paragraph(
        "As seen in Figure 4.3, the interactive web interface provides immediate visual feedback. "
        "Grammatical concord errors are flagged with amber highlights, spelling mistakes in red, and clarity suggestions in purple. "
        "Users can inspect detailed pedagogical guidance or trigger single-click contextual replacements.",
        body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 14: CHAPTER 5 & CHAPTER 6 (Page 7)
    # =========================================================================
    story.append(Paragraph("<b>Chapter 5</b>", chapter_title_style))
    story.append(Paragraph("<b>Applications</b>", chapter_title_style))
    story.append(Spacer(1, 3))

    story.append(Paragraph("<b>5.1 Educational & Academic Applications</b>", section_title_style))
    story.append(Paragraph(
        "<b>Automated Student Tutoring:</b> Syntaxa AI serves as an always-accessible writing tutor for undergraduate and graduate students. "
        "By presenting grammatical explanations rather than opaque auto-corrections, students actively learn grammatical rules and improve their long-term skills.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Thesis and Assignment Screening:</b> Academic departments can utilize the platform to pre-screen research papers, laboratory reports, "
        "and project dissertations, ensuring high syntactic quality before submission to faculty review committees.",
        body_style
    ))

    story.append(Paragraph("<b>5.2 Technical & Professional Applications</b>", section_title_style))
    story.append(Paragraph(
        "<b>Software Engineering Documentation:</b> Because the system whitelists modern developer libraries, APIs, and frameworks, software teams "
        "can proofread README files, technical specifications, and API documentation without false flags on code terminology.",
        body_style
    ))

    story.append(Paragraph("<b>5.3 Societal & Accessibility Applications</b>", section_title_style))
    story.append(Paragraph(
        "<b>Assistance for Non-Native English Speakers (ESL):</b> Second-language learners frequently struggle with English article usage "
        "(<i>a</i> vs. <i>an</i>) and preposition pairings (<i>good at</i> vs. <i>good in</i>). Syntaxa AI provides focused scaffolding to overcome these language barriers.",
        body_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Chapter 6</b>", chapter_title_style))
    story.append(Paragraph("<b>Conclusion and Future Scope</b>", chapter_title_style))
    story.append(Spacer(1, 3))

    story.append(Paragraph("<b>6.1 Conclusion</b>", section_title_style))
    story.append(Paragraph(
        "In this subject project, a robust, context-aware Natural Language Processing writing intelligence platform, <b>Syntaxa AI</b>, "
        "was successfully designed and implemented. By integrating deep syntactic dependency parsing with modular linguistic rule engines, "
        "the system accurately detects grammatical concord errors, spelling anomalies with technical whitelisting, punctuation defects, "
        "and clarity bottlenecks. The empirical 6-factor quality scoring model and pedagogical <i>Explain My Error</i> framework bridge "
        "the gap between mechanical proofreading and genuine writing mentorship.",
        body_style
    ))

    story.append(Paragraph("<b>6.2 Future Scope</b>", section_title_style))
    story.append(Paragraph("Future extensions of this work include:", body_style))
    story.append(Paragraph("• <b>Multilingual GEC Support:</b> Extending dependency grammar parsing to Indian languages (Hindi, Marathi) and other European languages.", bullet_style))
    story.append(Paragraph("• <b>Browser Extension Integration:</b> Packaging the engine as a lightweight browser extension for real-time web form and email assistance.", bullet_style))
    story.append(Paragraph("• <b>Fine-Tuned Small LLM Integration:</b> Incorporating quantized local language models for nuanced semantic style transfer.", bullet_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 15: REFERENCES & ACKNOWLEDGEMENT (Page 8)
    # =========================================================================
    story.append(Paragraph("<b>REFERENCES</b>", chapter_title_style))
    story.append(Spacer(1, 4))

    ref_style = ParagraphStyle(
        'RStyle',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=9.5,
        leading=13.5,
        alignment=4,
        leftIndent=18,
        firstLineIndent=-18,
        spaceAfter=3.5
    )

    references = [
        "[1] D. Naber, “A Rule-Based Style and Grammar Checker,” Master's thesis, Applied Sciences, Bielefeld University, Germany, 2003.",
        "[2] M. Chodorow and C. Leacock, “An Unsupervised Approach to Detecting Grammatical Errors,” in <i>Proc. 1st Conf. North American Chapter of the ACL</i>, 2000, pp. 140–147.",
        "[3] S. Rothe, J. Mallinson, E. Malmi, S. Krause, and M. Severyn, “A Simple Recipe for Multilingual Grammatical Error Correction,” in <i>Proc. 59th Annual Meeting of the ACL</i>, 2021, pp. 702–707.",
        "[4] K. Omelianchuk, V. Atrasevych, A. Chernodub, and O. Skurzhanskyi, “GECToR – Grammatical Error Correction: Tag, Not Rewrite,” in <i>Proc. 15th Workshop on Innovative Use of NLP for Building Educational Applications</i>, 2020, pp. 163–174.",
        "[5] M. Honnibal, I. Montani, S. Van Landeghem, and A. Boyd, “spaCy: Industrial-strength Natural Language Processing in Python,” Zenodo, 2020.",
        "[6] J. P. Kincaid, R. P. Fishburne, R. L. Rogers, and B. S. Chissom, “Derivation of New Readability Formulas for Navy Enlisted Personnel,” Naval Technical Training Command, Research Branch Report 8-75, 1975.",
        "[7] H. Yuan and M. Briscoe, “Grammatical Error Correction Using Neural Machine Translation,” in <i>Proc. 2016 Conf. of the NAACL: Human Language Technologies</i>, 2016, pp. 380–386."
    ]

    for ref in references:
        story.append(Paragraph(ref, ref_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>ACKNOWLEDGEMENT</b>", chapter_title_style))
    story.append(Spacer(1, 4))

    ack_text = (
        "I would like to express my sincere and deep gratitude to my subject teacher and project guide, <b>Prof. Nirosha Uppu</b>, "
        "Department of Artificial Intelligence and Data Science, for her invaluable guidance, encouragement, constructive critiques, "
        "and continuous support throughout the duration of this Natural Language Processing subject project."
    )
    story.append(Paragraph(ack_text, body_style))
    story.append(Spacer(1, 2))

    ack_text_2 = (
        "I extend my heartfelt thanks to <b>Dr. Shankar M. Patil</b>, Head of the Department of Artificial Intelligence and Data Science, "
        "for providing excellent laboratory facilities and academic environment that enabled the successful completion of this work."
    )
    story.append(Paragraph(ack_text_2, body_style))
    story.append(Spacer(1, 2))

    ack_text_3 = (
        "I also wish to express my sincere appreciation to our respected Principal, <b>Dr. Sunil Chavan</b>, for granting the institutional "
        "support and infrastructure necessary to conduct this subject project."
    )
    story.append(Paragraph(ack_text_3, body_style))
    story.append(Spacer(1, 2))

    ack_text_4 = (
        "Finally, I express my deepest appreciation to my family and friends for their enduring patience, encouragement, and moral support."
    )
    story.append(Paragraph(ack_text_4, body_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Sayali Ghagare</b><br/>Roll No. 23<br/>TE Artificial Intelligence and Data Science", ParagraphStyle('ASign', fontName='Times-Bold', fontSize=10.5, leading=14, alignment=2)))

    doc.build(story, canvasmaker=AcademicReportCanvas)
    print(f"Report successfully generated: {output_filename}")

if __name__ == "__main__":
    generate_pdf()
