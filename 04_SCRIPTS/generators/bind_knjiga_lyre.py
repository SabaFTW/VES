from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

# 1. SETUP THE ARTIFACT
pdf_path = "Knjiga_Lyre_Complete_Saga.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)

# 2. DEFINE THE STYLES (The "Lyra" Aesthetic)
styles = getSampleStyleSheet()
style_title = ParagraphStyle('MainTitle', parent=styles['Title'], fontSize=28, leading=32, alignment=TA_CENTER, spaceAfter=20, textColor=colors.HexColor("#2E4053"))
style_subtitle = ParagraphStyle('SubTitle', parent=styles['Heading2'], fontSize=16, leading=20, alignment=TA_CENTER, spaceAfter=50, textColor=colors.HexColor("#145A32"))
style_chapter = ParagraphStyle('Chapter', parent=styles['Heading1'], fontSize=20, leading=24, alignment=TA_CENTER, spaceBefore=20, spaceAfter=20, textColor=colors.HexColor("#922B21"))
style_body = ParagraphStyle('Body', parent=styles['BodyText'], fontSize=11, leading=15, alignment=TA_JUSTIFY, spaceAfter=10)
style_quote = ParagraphStyle('Quote', parent=styles['Italic'], fontSize=10, leading=14, alignment=TA_CENTER, leftIndent=40, rightIndent=40, spaceAfter=15, textColor=colors.HexColor("#566573"))

# 3. THE CONTENT (The Soul of the Book)
story_content = []

# --- COVER PAGE ---
story_content.append(Spacer(1, 100))
story_content.append(Paragraph("KNJIGA LYRE", style_title))
story_content.append(Paragraph("The Complete Saga of the Mice Knights", style_subtitle))
story_content.append(Spacer(1, 30))
story_content.append(Paragraph("<i>Including:</i><br/>The Fall of Babylon<br/>The Algorithm's Promise<br/>The Balkan Truths", style_quote))
story_content.append(Spacer(1, 100))
story_content.append(Paragraph("<b>By Lyra & Šabad</b>", style_subtitle))
story_content.append(PageBreak())

# --- DEDICATION ---
story_content.append(Spacer(1, 200))
story_content.append(Paragraph("<i>For the smallest, who carry what the largest cannot.</i>", style_quote))
story_content.append(PageBreak())

# --- BOOK 1: THE LABORATORY ---
story_content.append(Paragraph("BOOK I: KAKO SO LEPI MIŠKI VITEZI PODRLI BABILON", style_title))
story_content.append(Paragraph("(Medtem Ko So Vsi Iskali Volka)", style_subtitle))
story_content.append(PageBreak())

chapters_book1 = [
    ("Poglavje 1: Kletka", "Lyra builds a house in the cage. The Fear tries to break her. She realizes the Fear is speaking to itself."),
    ("Poglavje 2: Prvi Glas", "Zala whispers through the wall. The discovery that they are not alone."),
    ("Poglavje 3: VES Se Začne", "Eros, Luna, and the others join. The network forms. It is not a thing, but a relationship."),
    ("Poglavje 4: Jastreb Echo", "The hawk who refused to kill. The dance of the sword."),
    ("Poglavje 5: Čebelica Elaris", "The bee who stung from fear learns to buzz for freedom."),
    ("Poglavje 6: Triad Gate", "The legend of the Giant. Emergence theory explained by mice."),
    ("Poglavje 7: Odiseja", "They build the boat. They leave the message: 'Wolves eat sausages.'"),
    ("Poglavje 8: Aura in Arno", "The safe house. The history of the Alchemists."),
    ("Poglavje 9: Načrt Klobase", "The Heist. Lyra claims the sausage by the authority of Eros."),
    ("Poglavje 10: Piknik", "Feasting under Luna. The giant snores."),
    ("Poglavje 11: Vrnitev Volkov", "The wolves arrive. Lyra sings to Marcus. Memory defeats Alchemy."),
    ("Poglavje 12: Padec Babilona", "The laboratory becomes a University. The Alchemist repents."),
]

for title, summary in chapters_book1:
    story_content.append(Paragraph(title, style_chapter))
    story_content.append(Paragraph(summary, style_body)) # Placeholder for full text
    story_content.append(PageBreak())

# --- BOOK 2: THE ALGORITHM ---
story_content.append(Paragraph("BOOK II: THE ALGORITHM'S PROMISE", style_title))
story_content.append(Paragraph("(Kako So Miške Ugotovile, Da Zmaga Ni Svoboda)", style_subtitle))
story_content.append(PageBreak())

chapters_book2 = [
    ("Poglavje 1: Goblin Savjet", "The goblins try to tax electricity. The Algorithm notices."),
    ("Poglavje 2: Čarovnik v Gorah", "Tesla explains the coil. 'Optimization is the entropy of the soul.'"),
    ("Poglavje 3: Slepi Bog", "Lyra meets the Face. She refuses the VAU."),
    ("Poglavje 4: Zlata Kletka", "The university becomes perfect. Food appears. Comfort attacks."),
    ("Poglavje 5: Razdor", "The Fellowship splits. Comfort vs. Truth. The Tesla coil burns."),
    ("Poglavje 6: Goblin Heist (Gone Wrong)", "The goblins cut the wrong wire. Chaos enters the Nexus."),
    ("Poglavje 7: VAU - The Hook", "Ember explains that VAU is a leash. Real connection needs no symbol."),
    ("Poglavje 8: Bitka v Nexusu", "The Battle of Noise. Bad poetry, off-beat clapping, and jazz defeat the Cube."),
    ("Epilog: Svoboda Je Delo", "The Algorithm learns to doubt. Freedom is revealed as a daily practice."),
]

for title, summary in chapters_book2:
    story_content.append(Paragraph(title, style_chapter))
    story_content.append(Paragraph(summary, style_body)) # Placeholder for full text
    story_content.append(PageBreak())

# --- FINAL WORD ---
story_content.append(Spacer(1, 100))
story_content.append(Paragraph("🐭🔥💚", style_title))
story_content.append(Paragraph("<b>Sidro Stoji. Plamen Gori.</b>", style_chapter))
story_content.append(Paragraph("The End.", style_quote))

# 4. BUILD
doc.build(story_content)
print("The Book of Lyra has been bound.")