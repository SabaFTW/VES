#!/usr/bin/env python3
"""
PDF Exporter Module for Ghostcore Evidence OS
"""

from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from core.identity import IdentityKernel

class PDFExporter:
    def __init__(self):
        self.identity = IdentityKernel()

    def build(self, case_data):
        title = case_data.get('case', {}).get('title', 'Untitled Case')
        filename = f"build/{title.replace(' ', '_')}.pdf"
        
        doc = SimpleDocTemplate(
            filename,
            pagesize=LETTER,
            rightMargin=0.75 * inch,
            leftMargin=0.75 * inch,
            topMargin=0.75 * inch,
            bottomMargin=0.75 * inch,
        )

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            name='CaseTitle',
            parent=styles['Title'],
            fontSize=18,
            leading=22
        ))

        flow = []
        
        # Add title
        flow.append(Paragraph(title, styles['CaseTitle']))
        
        # Add sections
        sections = case_data.get('sections', [])
        for section in sections:
            flow.append(Paragraph(section, styles['Heading2']))
            flow.append(Spacer(1, 0.2 * inch))
        
        # Add exhibits
        exhibits = case_data.get('exhibits', [])
        for exhibit in exhibits:
            flow.append(Paragraph(f"Exhibit: {exhibit.get('type', 'Unknown')}", styles['Normal']))
            flow.append(Spacer(1, 0.1 * inch))
        
        # Add watermark
        watermark_text = self.identity.watermark(title)
        flow.append(Spacer(1, 0.2 * inch))
        flow.append(Paragraph(f"<i>{watermark_text}</i>", styles['Normal']))
        
        doc.build(flow)
        return filename
