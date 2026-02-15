#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GHOSTCORE EVIDENCE GENERATOR — VERSION 3.0

V2 + FULL REPORT TEMPLATE + ZIP + optional upload na transfer.sh

Features:
- Media Card (PNG)
- One-page Summary (PDF)
- QR Code (PNG)
- Full Report Template PDF (z placeholderji)
- ZIP Launch Pack
- Optional upload via transfer.sh (curl required)
"""

import argparse
import os
import zipfile
import subprocess
from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from PIL import Image, ImageDraw, ImageFont
import qrcode


# ---------- LOG HELPERS ----------

def log(msg, level="INFO"):
    print(f"[{level}] {msg}")


# ---------- MEDIA CARD ----------

def generate_media_card(path="media_card.png"):
    log("Generiram Media Card...")

    width, height = 1350, 1080
    img = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(img)

    text = "NO SPECULATION.\nONLY SOURCED EVIDENCE."
    font_size = 80

    # Robust font loading
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # pogost Linux
        "Arial Bold.ttf",                                       # Windows
        "Arial.ttf",
        "/Library/Fonts/Arial.ttf"                              # macOS
    ]
    font = None
    for f in font_paths:
        try:
            font = ImageFont.truetype(f, font_size)
            break
        except Exception:
            continue

    if font is None:
        log("Font not found — using default (fallback).", "WARN")
        font = ImageFont.load_default()

    # Center text
    try:
        bbox = draw.textbbox((0, 0), text, font=font, align="center")
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
    except AttributeError:
        # older Pillow
        tw, th = draw.textsize(text, font=font)

    x = (width - tw) / 2
    y = (height - th) / 2

    draw.multiline_text(
        (x, y),
        text,
        font=font,
        fill="black",
        align="center",
        spacing=20
    )

    img.save(path)
    log(f"Media Card shranjen → {path}")


# ---------- ONE-PAGE SUMMARY PDF ----------

def generate_summary(path="one_page_summary.pdf"):
    log("Generiram Summary PDF...")

    doc = SimpleDocTemplate(
        path,
        pagesize=LETTER,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='SummaryTitle',
        parent=styles['Title'],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        spaceAfter=20,
    ))
    styles.add(ParagraphStyle(
        name='SummaryHeader',
        parent=styles['Heading1'],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        spaceAfter=10,
    ))
    styles.add(ParagraphStyle(
        name='SummaryBody',
        parent=styles['BodyText'],
        fontName="Helvetica",
        fontSize=11,
        leading=15,
        spaceAfter=6,
    ))

    flow = []

    # Title
    flow.append(Paragraph("CONDENSED INVESTIGATIVE SUMMARY", styles['SummaryTitle']))
    flow.append(Spacer(1, 0.15 * inch))

    # Exec overview
    flow.append(Paragraph("EXECUTIVE SUMMARY", styles['SummaryHeader']))
    flow.append(Paragraph(
        "This one-page briefing highlights verified intersections between federal investigative decisions, "
        "private-sector surveillance infrastructure, and financial networks linked to Jeffrey Epstein. "
        "All referenced material derives from public congressional documents, DOJ/SDNY filings, "
        "SEC disclosures, and mainstream investigative reporting.",
        styles['SummaryBody']
    ))

    flow.append(Spacer(1, 0.15 * inch))

    # Top findings
    flow.append(Paragraph("TOP FINDINGS (VERIFIED)", styles['SummaryHeader']))
    findings = [
        "DOJ closure of active Epstein co-conspirator investigation (2025).",
        "Carbyne-Axon acquisition ($625M) with Unit 8200 lineage and Epstein-linked funding.",
        "Epstein's $40M investment in Valar Ventures (2015–2016), now valued at ~$170M.",
        "Structural patterns: institutional concealment, government–industry convergence, funding asymmetry.",
    ]
    for f in findings:
        flow.append(Paragraph("• " + f, styles['SummaryBody']))

    flow.append(Spacer(1, 0.15 * inch))

    # Reform
    flow.append(Paragraph("REFORM PATHWAYS", styles['SummaryHeader']))
    flow.append(Paragraph(
        "Recommended areas include oversight of foreign-linked surveillance technology, transparency requirements for "
        "venture funds receiving tainted capital, DOJ procedural reforms, and public accounting of AI-defense contracting.",
        styles['SummaryBody']
    ))

    doc.build(flow)
    log(f"Summary PDF shranjen → {path}")


# ---------- QR CODE ----------

def generate_qr(path="full_report_qr.png",
                url="https://ghostcore-archive.net/report/full_download"):
    log(f"Generiram QR kodo za URL: {url}")

    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(path)

    log(f"QR koda shranjena → {path}")


# ---------- FULL REPORT TEMPLATE PDF (V3 CORE) ----------

def generate_full_report_template(output_dir=".", version_tag=None):
    """
    Ustvari PROFESSIONAL FULL TEMPLATE PDF z naslovnico in placeholderji.
    """
    log("Generiram FULL REPORT TEMPLATE PDF...")

    if version_tag is None:
        version_tag = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"FULL_REPORT_TEMPLATE_{version_tag}.pdf"
    path = os.path.join(output_dir, filename)

    doc = SimpleDocTemplate(
        path,
        pagesize=LETTER,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name='CoverTitle',
        parent=styles['Title'],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=30,
        alignment=1,  # center
        spaceAfter=20,
    ))

    styles.add(ParagraphStyle(
        name='CoverSub',
        parent=styles['BodyText'],
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        alignment=1,
        spaceAfter=10,
    ))

    styles.add(ParagraphStyle(
        name='SectionHeader',
        parent=styles['Heading1'],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=20,
        spaceBefore=12,
        spaceAfter=8,
    ))

    styles.add(ParagraphStyle(
        name='SubHeader',
        parent=styles['Heading2'],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        spaceBefore=8,
        spaceAfter=4,
    ))

    styles.add(ParagraphStyle(
        name='Body',
        parent=styles['BodyText'],
        fontName="Helvetica",
        fontSize=11,
        leading=15,
        spaceAfter=6,
    ))

    styles.add(ParagraphStyle(
        name='Placeholder',
        parent=styles['BodyText'],
        fontName="Helvetica-Oblique",
        fontSize=11,
        leading=15,
        textColor="gray",
        spaceAfter=8,
    ))

    flow = []

    # ----- COVER PAGE -----
    flow.append(Spacer(1, 2 * inch))
    flow.append(Paragraph("INVESTIGATIVE REPORT – WORKING TEMPLATE", styles['CoverTitle']))
    flow.append(Spacer(1, 0.5 * inch))

    flow.append(Paragraph("[[ INSERT REPORT TITLE HERE ]]", styles['CoverSub']))
    flow.append(Spacer(1, 0.3 * inch))

    flow.append(Paragraph("Author: [[ Šabad / Independent Researcher ]]", styles['CoverSub']))
    flow.append(Paragraph("Date: [[ YYYY-MM-DD ]]", styles['CoverSub']))
    flow.append(Paragraph("Version: [[ v1.0 / Draft ]]", styles['CoverSub']))

    flow.append(Spacer(1, 1 * inch))
    flow.append(Paragraph(
        "This template is designed for legal- and newsroom-grade investigative reporting. "
        "Replace all placeholder markers with your own content.",
        styles['Body']
    ))
    flow.append(PageBreak())

    # ----- SECTION I: EXECUTIVE SUMMARY -----
    flow.append(Paragraph("I. EXECUTIVE SUMMARY", styles['SectionHeader']))
    flow.append(Paragraph(
        "[[ INSERT: 1–3 paragraphs summarizing the investigation, major findings, and why it matters. ]]",
        styles['Placeholder']
    ))

    flow.append(PageBreak())

    # ----- SECTION II: SCOPE AND METHODOLOGY -----
    flow.append(Paragraph("II. SCOPE AND METHODOLOGY", styles['SectionHeader']))
    flow.append(Paragraph(
        "[[ Describe sources used: court filings, congressional documents, FOIA material, corporate records, "
        "interviews, data analysis methods. Clarify what is included and what is out of scope. ]]",
        styles['Placeholder']
    ))

    flow.append(PageBreak())

    # ----- SECTION III: VERIFIED FINDINGS -----
    flow.append(Paragraph("III. VERIFIED FINDINGS", styles['SectionHeader']))

    for i in range(1, 5):
        flow.append(Paragraph(f"Finding {i} – [[ Short Title ]]", styles['SubHeader']))
        flow.append(Paragraph(
            "[[ Insert factual description, time frame, entities involved, and citations to documents. "
            "Avoid speculation. ]]",
            styles['Placeholder']
        ))

    flow.append(PageBreak())

    # ----- SECTION IV: STRUCTURAL PATTERNS -----
    flow.append(Paragraph("IV. STRUCTURAL PATTERNS", styles['SectionHeader']))

    patterns = [
        "Funding Asymmetry",
        "Institutional Concealment",
        "Government–Industry Convergence",
        "Externalized Harm / Delayed Disclosure"
    ]
    for p in patterns:
        flow.append(Paragraph(p, styles['SubHeader']))
        flow.append(Paragraph(
            f"[[ Explain how {p} appears in your evidence. Use concrete examples from documents or contracts. ]]",
            styles['Placeholder']
        ))

    flow.append(PageBreak())

    # ----- SECTION V: TIMELINE OF EVENTS -----
    flow.append(Paragraph("V. TIMELINE OF RELEVANT EVENTS", styles['SectionHeader']))
    flow.append(Paragraph(
        "[[ Build a chronological list of key events (e.g., 1973–1974, 2002–2017, 2015–2016, 2019–2025) "
        "with one line per event and citation references. ]]",
        styles['Placeholder']
    ))

    flow.append(PageBreak())

    # ----- SECTION VI: EVIDENCE AND SOURCES -----
    flow.append(Paragraph("VI. EVIDENCE AND SOURCE MATRIX", styles['SectionHeader']))
    flow.append(Paragraph(
        "[[ List your primary sources by type: court dockets, congressional letters, SEC filings, "
        "press releases, investigative articles. Optionally create a table elsewhere. ]]",
        styles['Placeholder']
    ))

    flow.append(PageBreak())

    # ----- SECTION VII: REFORM PATHWAYS -----
    flow.append(Paragraph("VII. REFORM PATHWAYS AND POLICY QUESTIONS", styles['SectionHeader']))
    flow.append(Paragraph(
        "[[ Identify possible reforms, oversight mechanisms, or open questions for lawmakers, regulators, "
        "or institutions. Frame them as questions and concrete proposals, not slogans. ]]",
        styles['Placeholder']
    ))

    flow.append(PageBreak())

    # ----- SECTION VIII: APPENDICES -----
    flow.append(Paragraph("VIII. APPENDICES (OPTIONAL)", styles['SectionHeader']))
    flow.append(Paragraph("Appendix A – Document Index", styles['SubHeader']))
    flow.append(Paragraph("[[ Insert list of documents with IDs, dates, and short descriptions. ]]", styles['Placeholder']))

    flow.append(Paragraph("Appendix B – Organizational Charts", styles['SubHeader']))
    flow.append(Paragraph("[[ Insert or reference diagrams showing company/government relationships. ]]", styles['Placeholder']))

    flow.append(Paragraph("Appendix C – Methodological Notes & Limitations", styles['SubHeader']))
    flow.append(Paragraph("[[ Describe limitations, uncertainties, and non-verified areas honestly. ]]", styles['Placeholder']))

    # Build PDF
    doc.build(flow)
    log(f"FULL REPORT TEMPLATE shranjen → {path}")
    return path


# ---------- ZIP PACK ----------

def generate_zip(zip_path="launch_pack.zip", files=None):
    if files is None:
        files = []

    log("Pakiram ZIP paket...")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for f in files:
            if os.path.exists(f):
                zipf.write(f, arcname=os.path.basename(f))
                log(f"Dodan v ZIP → {f}")
            else:
                log(f"Preskočen (ne obstaja) → {f}", "WARN")

    log(f"ZIP paket shranjen → {zip_path}")
    return zip_path


# ---------- OPTIONAL UPLOAD NA transfer.sh ----------

def upload_to_transfersh(path):
    """
    Upload file via transfer.sh using curl.
    Returns URL or None.
    """
    log(f"Pošiljam na transfer.sh → {path}")

    if not os.path.exists(path):
        log("Datoteka ne obstaja, upload preklican.", "ERROR")
        return None

    filename = os.path.basename(path)
    url = f"https://transfer.sh/{filename}"

    try:
        result = subprocess.run(
            ["curl", "--silent", "--upload-file", path, url],
            capture_output=True,
            text=True,
            check=True
        )
        link = result.stdout.strip()
        if link:
            log(f"Upload uspešen. URL → {link}")
            return link
        else:
            log("Nepričakovan prazen odgovor iz transfer.sh", "WARN")
            return None
    except FileNotFoundError:
        log("curl ni nameščen. Namesti ga ali preskoči --upload.", "ERROR")
        return None
    except subprocess.CalledProcessError as e:
        log(f"Napaka pri uploadu: {e}", "ERROR")
        return None


# ---------- CLI / MAIN ----------

def main():
    parser = argparse.ArgumentParser(description="Ghostcore Evidence Generator v3.0")
    parser.add_argument("--media", action="store_true", help="Generate Media Card PNG")
    parser.add_argument("--summary", action="store_true", help="Generate one-page Summary PDF")
    parser.add_argument("--qr", action="store_true", help="Generate QR code PNG")
    parser.add_argument("--template", action="store_true", help="Generate Full Report Template PDF")
    parser.add_argument("--all", action="store_true", help="Generate all assets (media, summary, qr, template)")
    parser.add_argument("--zip", action="store_true", help="Create ZIP Launch Pack from generated files")
    parser.add_argument("--upload", action="store_true", help="Upload ZIP Launch Pack to transfer.sh (requires curl)")
    parser.add_argument("--qr-url", type=str, default="https://ghostcore-archive.net/report/full_download",
                        help="Override QR target URL")
    args = parser.parse_args()

    files = []

    # Generate pieces
    if args.media or args.all:
        generate_media_card()
        files.append("media_card.png")

    if args.summary or args.all:
        generate_summary()
        files.append("one_page_summary.pdf")

    if args.qr or args.all:
        generate_qr(url=args.qr_url)
        files.append("full_report_qr.png")

    template_path = None
    if args.template or args.all:
        template_path = generate_full_report_template()
        files.append(template_path)

    zip_path = None
    if args.zip:
        zip_path = generate_zip(files=files)

    if args.upload:
        # če ni posebej generiran ZIP, ga generiraj zdaj
        if zip_path is None:
            zip_path = generate_zip(files=files)
        upload_to_transfersh(zip_path)

    log("Končano.")


if __name__ == "__main__":
    main()