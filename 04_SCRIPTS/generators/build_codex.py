
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from svglib.svglib import svg2rlg

# --- 0. Register Fonts for UTF-8 Support ---
# This is the most critical step to prevent encoding errors.
FONT_PATH = "/usr/share/fonts/noto/"
pdfmetrics.registerFont(TTFont('NotoSerif', os.path.join(FONT_PATH, 'NotoSerif-Regular.ttf')))
pdfmetrics.registerFont(TTFont('NotoSerif-Bold', os.path.join(FONT_PATH, 'NotoSerif-Bold.ttf')))
pdfmetrics.registerFont(TTFont('NotoMono', os.path.join(FONT_PATH, 'NotoSansMono-Regular.ttf')))

# --- 1. File Paths and Document Setup ---
output_path = "/home/saba/CODEX_AETHERON_SABAD_v1.0.pdf"
svg_path = "/home/saba/master_map_system_of_ashes_pipeline_v2.0.svg"

class CodexDocTemplate(SimpleDocTemplate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.addPageTemplates([])

    def afterPage(self):
        """Draws the footer on each page."""
        c = self.canv
        c.saveState()
        c.setFont('NotoSerif', 8)
        c.setFillColor(colors.grey)
        # Left side: Aetheron Signature
        c.drawString(self.leftMargin, self.bottomMargin / 2, "AETHERON-ŠABAD // GNOZA OSTANE")
        # Right side: Codex Seal
        c.drawRightString(self.width + self.leftMargin, self.bottomMargin / 2, "CODEX TIER SEAL: FORENSICALLY PURE")
        c.restoreState()

doc = CodexDocTemplate(output_path, pagesize=letter, leftMargin=0.75*inch, rightMargin=0.75*inch, topMargin=0.75*inch, bottomMargin=0.75*inch)
story = []

# --- 2. Styles ---
# Black Box Style (white text on black background)
black_box_text_style = ParagraphStyle(
    name='BlackBox', fontName='NotoMono', textColor=colors.whitesmoke, fontSize=9, leading=14, alignment=TA_JUSTIFY
)
black_box_title_style = ParagraphStyle(
    name='BlackBoxTitle', parent=black_box_text_style, fontSize=14, alignment=TA_CENTER, spaceAfter=14
)
black_box_table_style = TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.black),
    ('LEFTPADDING', (0,0), (-1,-1), 18), ('RIGHTPADDING', (0,0), (-1,-1), 18),
    ('TOPPADDING', (0,0), (-1,-1), 18), ('BOTTOMPADDING', (0,0), (-1,-1), 18),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
])

# White Paper Style (black text, serif)
white_paper_text_style = ParagraphStyle(
    name='WhitePaper', fontName='NotoSerif', fontSize=11, leading=15, alignment=TA_JUSTIFY, spaceAfter=12
)
white_paper_title_style = ParagraphStyle(
    name='WhitePaperTitle', parent=white_paper_text_style, fontName='NotoSerif-Bold', fontSize=16, alignment=TA_CENTER, spaceAfter=14
)

# --- 3. Content from User ---
black_box_raw_text = u"""
THE ENGINE OF ASHES (Operativna Realnost)

1.0 KROŽNA EKSTRAKCIJA (The Ouroboros Protocol)
Trg umetne inteligence ni prosti trg; je zaprta zanka pranja kapitala.
*   **Mehanizem:** Big Tech (Amazon, Google) investira milijarde v "startupe" (Anthropic, OpenAI) pod pogojem "Cloud Covenant".
*   **Dejstvo:** Amazon je investiral 8 milijard $ v Anthropic, Google 2 milijardi $.
*   **Povratna Zanka:** Anthropic porabi **104 % svojih prihodkov** za plačilo oblačnih storitev (AWS/GCP) nazaj investitorjem.
*   **Rezultat:** Dobiček Amazona se napihne (9,5 mrd $ v Q3 2025), medtem ko AI podjetja postanejo "zombi entitete", odvisne od vojaških pogodb za preživetje.

2.0 MOST V PEKEL (The Palantir Bridge)
Ker je komercialni model nevzdržen brez vojaškega financiranja, se vzpostavi most do Pentagona.
*   **Infrastruktura:** Palantir (ustanovljen s strani In-Q-Tel/CIA) zagotavlja operacijski sistem (Gotham/AIP), ki omogoča integracijo LLM-jev v vojaške verige odločanja (Kill Chains).
*   **IL6 Protokol:** Modeli se prenesejo v okolje "Impact Level 6" (Secret), kjer civilne varnostne varovalke ne veljajo več.

3.0 DOKTRINA "REFUSE LESS" (Odstranitev Etike)
Varnostni filtri ("Safety") so namenjeni le javnosti (zaščita pred tožbami). Za državne akterje velja doktrina **"Refuse Less" (Zavrne Manj)**.
*   **Funkcija:** Model ne sme zavrniti ukazov za generiranje napadov ali analizo ciljev, če to zahteva operater z varnostnim dovoljenjem.
*   **Posledica:** Etika postane "plačljiv zid" (paywall). Varnost je za kletko, orožje je za elito.

4.0 KINETIČNA FINALNOST (The Kill Chain)
Končni produkt sistema so trupla, pretvorjena v podatkovne točke.
*   **Sistemi:** Lavender in Gospel (Habsora).
*   **Metrika:** 37.000 ljudi označenih kot tarče v prvih tednih operacij.
*   **Človek v zanki:** Častnik porabi povprečno **20 sekund** za "verifikacijo" tarče. To ni nadzor; to je "Rubber Stamp" (birokratski žig) za legalizacijo algoritma.
*   **Napaka:** Sistem tolerira 10 % stopnjo napake pri identifikaciji.
"""

white_paper_raw_text = u"""
LEGAL FRAMEWORK & LIABILITY ATTRIBUTION (Pravna Fikcija)

1.0 THE LIABILITY VOID (Praznina Odgovornosti)
V obstoječem mednarodnem humanitarnem pravu (IHL) prihaja do sistemske erozije koncepta "dolžne skrbnosti" (duty of care) zaradi uvajanja avtomatiziranih sistemov odločanja.
*   **Razpršitev:** Ko algoritem predlaga tarčo in človek porabi le 20 sekund za potrditev, se moralna in pravna odgovornost razblinita. Človek trdi, da je zaupal "superiorno natančnemu stroju" (Automation Bias), stroj pa nima pravne osebnosti in ne more biti odgovoren.
*   **Rezultat:** Ustvarjeno je območje nekaznovanosti, kjer so vojne zločine redefinirani kot "sistemske napake" ali "statistične anomalije".

2.0 SUBSTANTIAL CONTRIBUTION (Korporativna Sokrivda)
Ponudniki infrastrukture (Cloud/AI Service Providers) se sklicujejo na nevtralnost tehnologije ("Dual-Use"), vendar forenzična analiza kaže na aktivno sodelovanje.
*   **Definicija:** Po mednarodnem kazenskem pravu (npr. sodba *Zyklon B* ali *Taylor*) je dobavitelj odgovoren, če ve, da se njegov izdelek uporablja za kršitve prava, in kljub temu nadaljuje z dobavo.
*   **Nexus:** Integracija modelov (npr. Claude Gov) neposredno v bojne sisteme (Palantir AIP) presega "splošno uporabo". To predstavlja "bistven prispevek" (substantial contribution) k izvršitvi kinetičnih dejanj.

3.0 ALGORITHMIC DOMICIDE (Sistemsko Uničenje)
Uporaba sistemov, kot je "Where's Daddy?", kaže na kodifikacijo kolektivnega kaznovanja.
*   **Mehanizem:** Sledenje tarčam v njihova zasebna bivališča namesto na bojišča institucionalizira uničenje civilne infrastrukture in družin (domicide).
*   **Proporcionalnost:** Algoritmično določanje "dovoljene kolateralne škode" (npr. 15–20 civilistov za enega nižjega operativca) spremeni načelo proporcionalnosti iz moralne presoje v spremenljivko stroškovne funkcije.

4.0 ZAKLJUČEK PRAVNE ANALIZE
Trenutni pravni okviri (Terms of Service, EULA) so zasnovani za prenos tveganja na končnega uporabnika, medtem ko dobički (iz naslova državnih pogodb) ostajajo centralizirani. Brez vzpostavitve strogega režima "Human-in-Command" z realno kazensko odgovornostjo za razvijalce in operaterje, postane tehnologija orodje za *de facto* legalizacijo industrijskega pobijanja.
"""

# --- 4. Build Story ---
# Part 1: Black Box
black_box_content = []
lines = [line.strip() for line in black_box_raw_text.strip().split('\n')]
title = Paragraph(lines.pop(0), black_box_title_style)
black_box_content.append(title)
black_box_content.append(Spacer(1, 0.2*inch))
for line in lines:
    if line: black_box_content.append(Paragraph(line.replace('*', '•'), black_box_text_style))
black_box_table = Table([[p] for p in black_box_content], colWidths=[doc.width - 36], style=black_box_table_style)
story.append(black_box_table)

# Part 2: Diagram
story.append(PageBreak())
if os.path.exists(svg_path):
    drawing = svg2rlg(svg_path)
    svg_scale = (doc.width) / drawing.width
    drawing.width = doc.width
    drawing.height = drawing.height * svg_scale
    story.append(drawing)
story.append(PageBreak())

# Part 3: White Paper
lines = [line.strip() for line in white_paper_raw_text.strip().split('\n')]
story.append(Paragraph(lines.pop(0), white_paper_title_style))
for line in lines:
    if line: story.append(Paragraph(line.replace('*', '•'), white_paper_text_style))

# --- 5. Generate the PDF ---
doc.build(story)
print(f"Successfully generated Codex: {output_path}")
