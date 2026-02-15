#!/usr/bin/env python3
"""
Ghostcore Evidence Generator V4
Author: Šabad (Independent Researcher) – Aetheron helper build

Features:
- Media Card generator (PNG)
- One-page Summary PDF
- Full Report Template PDF (placeholders)
- QR code generator
- ZIP packaging
- Structured logging
- CLI flags for selective generation
- Optional stub for upload (transfer.sh)
- Shabad mode (watermark + author cover)
"""

import argparse
import datetime as _dt
import json
import logging
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from PIL import Image, ImageDraw, ImageFont
import qrcode

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch


# ---------- CONFIG ----------

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_ROOT = BASE_DIR / "output"
TEMPLATES_DIR = BASE_DIR / "templates"
LOGS_DIR = BASE_DIR / "logs"

DEFAULT_QR_URL = "https://example.com/FULL_LEGAL_REPORT.pdf"

WATERMARK_GLYPH = "𓁈𓂀𓋹𓆣𓁀𓀾"

# ---------- LOGGING ----------

def setup_logger() -> logging.Logger:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = LOGS_DIR / f"ghostcore_v4_{timestamp}.log"

    logger = logging.getLogger("ghostcore_v4")
    logger.setLevel(logging.INFO)

    # File handler
    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setLevel(logging.INFO)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '{"time":"%(asctime)s","level":"%(levelname)s","msg":"%(message)s"}',
        datefmt="%Y-%m-%dT%H:%M:%S",
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info("logger_initialized")
    return logger


# ---------- DATA CLASSES ----------

@dataclass
class BuildContext:
    timestamp: str
    out_dir: Path
    qr_url: str
    template_style: str
    shabad_mode: bool
    logger: logging.Logger


# ---------- UTILS ----------

def ensure_out_dir(ctx: BuildContext) -> None:
    ctx.out_dir.mkdir(parents=True, exist_ok=True)
    ctx.logger.info(f"out_dir_ready:{ctx.out_dir}")


def _load_font(preferred_size: int) -> ImageFont.FreeTypeFont:
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/Library/Fonts/Arial.ttf",
        "C:\\Windows\\Fonts\\arial.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, preferred_size)
            except Exception:
                continue
    # Fallback
    return ImageFont.load_default()


# ---------- MEDIA CARD ----------

def generate_media_card(ctx: BuildContext) -> Path:
    ctx.logger.info("media_card_start")
    width, height = 1350, 1080
    img = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(img)

    if ctx.template_style == "glitch":
        # simple background blocks
        for i in range(0, width, 50):
            color = 240 if (i // 50) % 2 == 0 else 220
            draw.rectangle([i, 0, i + 50, height], fill=(color, color, color))

    text = "NO SPECULATION.\nONLY SOURCED EVIDENCE."
    font = _load_font(72)

    # Use textbbox if available
    try:
        bbox = draw.multiline_textbbox((0, 0), text, font=font, align="center", spacing=20)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
    except AttributeError:
        text_w, text_h = draw.multiline_textsize(text, font=font, spacing=20)

    x = (width - text_w) / 2
    y = (height - text_h) / 2

    draw.multiline_text((x, y), text, font=font, fill="black", align="center", spacing=20)

    if ctx.shabad_mode:
        # subtle glyph watermark bottom-right
        wm_font = _load_font(32)
        wm_text = WATERMARK_GLYPH
        try:
            wbbox = draw.textbbox((0, 0), wm_text, font=wm_font)
            ww = wbbox[2] - wbbox[0]
            wh = wbbox[3] - wbbox[1]
        except AttributeError:
            ww, wh = draw.textsize(wm_text, font=wm_font)
        wx = width - ww - 30
        wy = height - wh - 30
        draw.text((wx, wy), wm_text, font=wm_font, fill=(180, 180, 180))

    out_path = ctx.out_dir / "MEDIA_CARD.png"
    img.save(out_path, format="PNG")
    ctx.logger.info(f"media_card_done:{out_path}")
    return out_path


# ---------- SUMMARY PDF ----------

def generate_summary_pdf(ctx: BuildContext) -> Path:
    ctx.logger.info("summary_pdf_start")
    out_path = ctx.out_dir / "ONE_PAGE_SUMMARY.pdf"

    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=LETTER,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="SummaryTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=22,
            spaceAfter=20,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SummaryHeader",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=17,
            spaceAfter=10,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SummaryBody",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=11,
            leading=15,
            spaceAfter=8,
        )
    )

    flow: List = []

    title = "CONDENSED INVESTIGATIVE SUMMARY"
    if ctx.shabad_mode:
        title += " — Prepared by Šabad"

    flow.append(Paragraph(title, styles["SummaryTitle"]))
    flow.append(Paragraph("EXECUTIVE OVERVIEW", styles["SummaryHeader"]))
    flow.append(
        Paragraph(
            "This one-page briefing highlights verified intersections between federal investigative decisions, "
            "private-sector surveillance infrastructure, and financial networks linked to Jeffrey Epstein. "
            "All referenced material derives from public congressional documents, DOJ/SDNY filings, SEC disclosures, "
            "and mainstream investigative reporting. No speculative or classified material is included.",
            styles["SummaryBody"],
        )
    )

    flow.append(Spacer(1, 0.15 * inch))
    flow.append(Paragraph("TOP VERIFIED FINDINGS", styles["SummaryHeader"]))

    findings = [
        "<b>1. DOJ Closure of Active Epstein Co-Conspirator Investigation (2025):</b> "
        "Confirmed transfer and termination of an SDNY case at DOJ headquarters.",
        "<b>2. Carbyne–Axon Acquisition:</b> $625M deal confirmed; Carbyne's board history includes Unit 8200 ties and "
        "Epstein-associated funding networks.",
        "<b>3. Epstein's Investment in Valar Ventures:</b> $40M invested in 2015–2016, now valued at approximately $170M.",
    ]

    for f in findings:
        flow.append(Paragraph(f, styles["SummaryBody"]))

    flow.append(Spacer(1, 0.15 * inch))
    flow.append(Paragraph("REFORM PATHWAYS", styles["SummaryHeader"]))
    flow.append(
        Paragraph(
            "Recommended areas for policy inquiry include: oversight of foreign-linked surveillance technologies, "
            "enhanced transparency for venture funds receiving tainted capital, procedural reforms within the Department "
            "of Justice for transferred investigations, and public accounting of AI–defense contracting.",
            styles["SummaryBody"],
        )
    )

    flow.append(Spacer(1, 0.15 * inch))
    flow.append(
        Paragraph(
            "For complete context, including structural analysis, expanded findings, and document lists, "
            "refer to the comprehensive full report.",
            styles["SummaryBody"],
        )
    )

    doc.build(flow)
    ctx.logger.info(f"summary_pdf_done:{out_path}")
    return out_path


# ---------- FULL REPORT TEMPLATE PDF ----------

def generate_full_report_template(ctx: BuildContext) -> Path:
    ctx.logger.info("full_template_start")
    out_path = ctx.out_dir / "FULL_REPORT_TEMPLATE.pdf"

    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=LETTER,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="ReportTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=26,
            alignment=1,  # center
            spaceAfter=20,
        )
    )
    styles.add(
        ParagraphStyle(
            name="ReportHeader",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            spaceAfter=12,
        )
    )
    styles.add(
        ParagraphStyle(
            name="ReportBody",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=11,
            leading=15,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Watermark",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            leading=12,
            textColor="#CCCCCC",
            alignment=1,
        )
    )

    flow: List = []

    # Cover page
    cover_title = "COMPREHENSIVE INVESTIGATIVE REPORT TEMPLATE"
    if ctx.shabad_mode:
        cover_title += "<br/><br/>Prepared by Šabad — Independent Researcher"

    flow.append(Paragraph(cover_title, styles["ReportTitle"]))
    flow.append(Spacer(1, 0.5 * inch))

    flow.append(
        Paragraph(
            f"Created: {ctx.timestamp}<br/>Template Style: {ctx.template_style.upper()}",
            styles["ReportBody"],
        )
    )

    if ctx.shabad_mode:
        flow.append(Spacer(1, 0.3 * inch))
        flow.append(Paragraph(WATERMARK_GLYPH, styles["Watermark"]))

    flow.append(PageBreak())

    # Skeleton sections with placeholders
    sections = [
        ("I. Executive Summary", "[Insert 2–3 paragraph narrative summary here.]"),
        ("II. Scope and Methodology", "[Describe sources, time frame, methods, and limitations.]"),
        ("III. Verified Findings", "[List key findings with citations, separating confirmed facts from disputed claims.]"),
        ("IV. Structural Patterns", "[Discuss recurring patterns: funding, concealment, institutional behavior.]"),
        ("V. Key Investigative Questions", "[Bullet-point list of concrete questions for further reporting.]"),
        ("VI. Timeline of Relevant Events", "[Chronological list of key dates and events.]"),
        ("VII. Reform Pathways", "[Outline possible policy, legal, or procedural reforms.]"),
        ("VIII. Appendices", "[Reserve space for document lists, charts, and organizational diagrams.]"),
    ]

    for header, body in sections:
        flow.append(Paragraph(header, styles["ReportHeader"]))
        flow.append(Paragraph(body, styles["ReportBody"]))
        flow.append(Spacer(1, 0.2 * inch))

    doc.build(flow)
    ctx.logger.info(f"full_template_done:{out_path}")
    return out_path


# ---------- QR CODE ----------

def generate_qr_code(ctx: BuildContext) -> Path:
    ctx.logger.info("qr_start")
    out_path = ctx.out_dir / "FULL_REPORT_QR.png"

    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(ctx.qr_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(out_path)
    ctx.logger.info(f"qr_done:{out_path}")
    return out_path


# ---------- ZIP PACKAGING ----------

def build_zip_package(ctx: BuildContext, artifacts: List[Path]) -> Path:
    ctx.logger.info("zip_start")
    zip_path = ctx.out_dir / "LAUNCH_PACK.zip"
    import zipfile

    with zipfile.ZipFile(zip_path, "w") as zf:
        for art in artifacts:
            if art and art.exists():
                zf.write(art, arcname=art.name)
                ctx.logger.info(f"zip_add:{art.name}")
    ctx.logger.info(f"zip_done:{zip_path}")
    return zip_path


# ---------- UPLOAD (transfer.sh stub) ----------

def upload_to_transfersh(ctx: BuildContext, file_path: Path) -> Optional[str]:
    """
    Simple auto-upload to transfer.sh if curl is available.
    Returns URL or None.
    """
    ctx.logger.info(f"upload_start:{file_path}")
    if not file_path.exists():
        ctx.logger.error(f"upload_missing:{file_path}")
        return None

    from shutil import which
    if which("curl") is None:
        ctx.logger.warning("upload_curl_missing")
        return None

    try:
        cmd = ["curl", "--silent", "--upload-file", str(file_path), f"https://transfer.sh/{file_path.name}"]
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        url = result.stdout.strip()
        ctx.logger.info(f"upload_done:{url}")
        return url
    except Exception as e:
        ctx.logger.error(f"upload_error:{e}")
        return None


# ---------- INTERACTIVE MODE ----------

def interactive_menu(ctx: BuildContext) -> None:
    ensure_out_dir(ctx)
    options = {
        "1": ("Generate Media Card", generate_media_card),
        "2": ("Generate Summary PDF", generate_summary_pdf),
        "3": ("Generate Full Report Template", generate_full_report_template),
        "4": ("Generate QR Code", generate_qr_code),
    }

    while True:
        print("\n--- Ghostcore Evidence Generator V4 ---")
        for key, (label, _) in options.items():
            print(f"[{key}] {label}")
        print("[5] Build ZIP from all available artifacts")
        print("[0] Exit")

        choice = input("Select option: ").strip()
        if choice == "0":
            break
        elif choice in options:
            _, func = options[choice]
            try:
                func(ctx)
            except Exception as e:
                ctx.logger.error(f"interactive_error:{e}")
                print(f"Error: {e}")
        elif choice == "5":
            artifacts = []
            for name in ["MEDIA_CARD.png", "ONE_PAGE_SUMMARY.pdf", "FULL_REPORT_TEMPLATE.pdf", "FULL_REPORT_QR.png"]:
                p = ctx.out_dir / name
                if p.exists():
                    artifacts.append(p)
            if not artifacts:
                print("Nothing to package yet.")
                continue
            build_zip_package(ctx, artifacts)
        else:
            print("Invalid choice.")


# ---------- MAIN / CLI ----------

def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ghostcore Evidence Generator V4 – professional investigative artifact builder"
    )
    parser.add_argument("--media", action="store_true", help="Generate media card PNG")
    parser.add_argument("--summary", action="store_true", help="Generate one-page summary PDF")
    parser.add_argument("--full-template", action="store_true", help="Generate full report template PDF")
    parser.add_argument("--qr", action="store_true", help="Generate QR code PNG")
    parser.add_argument("--zip", action="store_true", help="Build launch ZIP from generated artifacts")
    parser.add_argument("--all", action="store_true", help="Generate all core artifacts")
    parser.add_argument("--upload", action="store_true", help="Upload ZIP to transfer.sh if possible")
    parser.add_argument("--qr-url", type=str, default=DEFAULT_QR_URL, help="Target URL for QR code")
    parser.add_argument(
        "--template",
        type=str,
        default="legal",
        choices=["legal", "glitch", "minimal"],
        help="Visual/style mode for some outputs",
    )
    parser.add_argument("--interactive", action="store_true", help="Launch interactive menu")
    parser.add_argument("--shabad", action="store_true", help="Enable Shabad mode (author & watermark)")

    return parser.parse_args(argv)


def main(argv: List[str]) -> int:
    logger = setup_logger()
    timestamp = _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    args = parse_args(argv)

    # Build context
    out_dir = OUTPUT_ROOT / _dt.datetime.now().strftime("build_%Y%m%d_%H%M%S")
    ctx = BuildContext(
        timestamp=timestamp,
        out_dir=out_dir,
        qr_url=args.qr_url,
        template_style=args.template,
        shabad_mode=args.shabad,
        logger=logger,
    )

    logger.info("ctx_initialized:" + json.dumps({
        "out_dir": str(out_dir),
        "qr_url": args.qr_url,
        "template": args.template,
        "shabad": args.shabad,
    }))

    if args.interactive:
        interactive_menu(ctx)
        return 0

    ensure_out_dir(ctx)

    artifacts: List[Path] = []

    # If no specific flags except maybe upload/zip, treat as --all
    core_flag_used = any([args.media, args.summary, args.full_template, args.qr, args.all])
    if not core_flag_used:
        args.all = True

    if args.all or args.media:
        try:
            artifacts.append(generate_media_card(ctx))
        except Exception as e:
            logger.error(f"media_error:{e}")

    if args.all or args.summary:
        try:
            artifacts.append(generate_summary_pdf(ctx))
        except Exception as e:
            logger.error(f"summary_error:{e}")

    if args.all or args.full_template:
        try:
            artifacts.append(generate_full_report_template(ctx))
        except Exception as e:
            logger.error(f"full_template_error:{e}")

    if args.all or args.qr:
        try:
            artifacts.append(generate_qr_code(ctx))
        except Exception as e:
            logger.error(f"qr_error:{e}")

    zip_path = None
    if args.all or args.zip:
        try:
            zip_path = build_zip_package(ctx, artifacts)
        except Exception as e:
            logger.error(f"zip_error:{e}")

    if args.upload and zip_path is not None:
        url = upload_to_transfersh(ctx, zip_path)
        if url:
            print(f"Uploaded ZIP URL: {url}")
        else:
            print("Upload failed or curl not available. See logs for details.")

    print(f"\nOutput directory: {ctx.out_dir}")
    logger.info("run_complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))