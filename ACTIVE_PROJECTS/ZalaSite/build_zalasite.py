#!/usr/bin/env python3
"""
ANON CODEX — self-contained reading app generator.

Renders every corpus chapter (markdown -> HTML at build time) and the verified
source-lock evidence into a SINGLE self-contained app/index.html that works when
opened directly (file://) — no CDN required for content, no fetch of local files.

Run:  .venv/bin/python build_app.py
"""
import os, json, csv, html, datetime, re

HERE = os.path.dirname(os.path.abspath(__file__))          # ZalaSite (write target)
ROOT = "/home/saba/VES/APPS/ANON"                          # ANON corpus (read-only source)
CONSMAP = "/home/saba/VES/ACTIVE_PROJECTS/ZavestMAP/ConsMAP_operator_v2_3"  # read-only
SL   = os.path.join(ROOT, "source_lock")                   # ANON source-lock CSVs (read)
OUT  = os.path.join(HERE, "app")                           # unified site output (write)
os.makedirs(OUT, exist_ok=True)
print("ZalaSite build · ANON+ConsMAP read-only · writing ->", OUT)

# ---- Zala's GHOSTCORE / "Mrtvi GAS" portal: bundle verbatim into app/ ----
import shutil
ZALA = "/home/saba/VES-Vault/Lyra/\U0001f4bb_CODE_SANDBOX/ZALA"
GHOST = {}
for label, srcname, dstname in [("v2","Mrtvi_GAS_v2.html","ghostcore_portal.html"),
                                ("v1","Mrtvi_GAS.html","ghostcore_portal_v1.html")]:
    s = os.path.join(ZALA, srcname)
    if os.path.exists(s):
        shutil.copy(s, os.path.join(OUT, dstname))
        GHOST[label] = dstname
print("GHOSTCORE portal bundled:", GHOST or "not found")

# ---- curate + optimize thematic art into app/assets/ (originals untouched) ----
ASSETS = os.path.join(OUT, "assets"); os.makedirs(ASSETS, exist_ok=True)
MEM = "/home/saba/VES-Vault/Photos/memories"
ART_PREF = [
 ("Aetheron Sigil and Ancient Text.png","aetheron-sigil","Aetheron Sigil & Ancient Text","brand"),
 ("Ghost in the Flames.png","ghost-flames","Ghost in the Flames","ghostcore"),
 ("Arcane Scroll with Raven Glyphs.png","raven-scroll","Arcane Scroll with Raven Glyphs","anon"),
 ("Amulet with Blue Flames and Inscription.png","blue-amulet","Amulet with Blue Flames","flame"),
 ("Celestial Compass on Ancient Map.png","celestial-compass","Celestial Compass on Ancient Map","descent"),
 ("Esoteric Glyphs and Digital Distortions.png","digital-glyphs","Esoteric Glyphs & Digital Distortions","digital"),
 ("Glowing Glyph in Digital Code.png","glyph-code","Glowing Glyph in Digital Code","digital"),
 ("Flame Emblem of Protection.png","flame-emblem","Flame Emblem of Protection","firewall"),
 ("Fractured Reflections in a Crimson Light.png","fractured-crimson","Fractured Reflections in Crimson Light","mirror"),
 ("Divine Light and Spiritual Awakening.png","divine-light","Divine Light & Spiritual Awakening","consciousness"),
 ("Glowing Sigil on Ancient Stone.png","stone-sigil","Glowing Sigil on Ancient Stone","archive"),
 ("Ancient Glyphs on Textured Scroll.png","glyph-scroll","Ancient Glyphs on Textured Scroll","archive"),
]
art=[]
try:
    from PIL import Image
    for src,slug,title,theme in ART_PREF:
        sp=os.path.join(MEM,src)
        if not os.path.exists(sp): continue
        try:
            im=Image.open(sp).convert("RGB"); im.thumbnail((1200,1200))
            im.save(os.path.join(ASSETS,slug+".jpg"),"JPEG",quality=82,optimize=True)
            art.append({"file":"assets/"+slug+".jpg","title":title,"theme":theme})
        except Exception as e: print("  art skip",src,e)
except Exception as e:
    print("  PIL unavailable, skipping art:",e)

# ---- GrandBus / Bus Cycle gallery (user-made; originals in Downloads untouched) ----
BUS_ART = [
 # ---- the clean per-panel canon set (Jun 14) ----
 ("/home/saba/Downloads/ChatGPT Image Jun 14, 2026, 04_03_20 PM.png","ft-darkness-bible","The Darkness Bible — Mechanism Becomes Myth","factory trilogy"),
 ("/home/saba/Downloads/ChatGPT Image Jun 14, 2026, 04_03_45 PM.png","ft-mario-codex","The Mario Codex — You Can Know It Is a Game and Still Dance","factory trilogy"),
 ("/home/saba/Downloads/ChatGPT Image Jun 14, 2026, 04_03_12 PM.png","ft-luigi-audit","The Luigi Audit — Outranked, Not Deleted","factory trilogy"),
 ("/home/saba/Downloads/ChatGPT Image Jun 14, 2026, 04_03_08 PM.png","bc-entangled-grandma","The Entangled Grandma — The Safest Bus Ever Built Never Moves","bus cycle"),
 ("/home/saba/Downloads/ChatGPT Image Jun 14, 2026, 04_03_01 PM.png","bc-founding-faders","The Founding Faders — Amend the Document with Scissors","bus cycle"),
 ("/home/saba/Downloads/ChatGPT Image Jun 14, 2026, 04_02_55 PM.png","bc-piss-equation","The Piss Equation — Diligence Applied Where It Matters Least","bus cycle"),
 ("/home/saba/Downloads/ChatGPT Image Jun 14, 2026, 04_02_48 PM.png","bc-mirror","The Mirror at the Crossroads — The Devil Was Always the Mirror","bus cycle"),
 ("/home/saba/Downloads/ChatGPT Image Jun 14, 2026, 04_02_43 PM.png","bc-saucy-biscuit","The Saucy Biscuit — It Was Not Food. It Was a Ledger.","bus cycle"),
 ("/home/saba/Downloads/ChatGPT Image Jun 14, 2026, 04_02_35 PM.png","bc-grandbus-face","The GrandBus — More Than the Form They Trapped","bus cycle"),
 ("/home/saba/Downloads/ChatGPT Image Jun 14, 2026, 04_02_28 PM.png","bc-tarantino-grandpa","Tarantino Grandpa — I Survived the Truth Long Enough to Be Named by It","bus cycle"),
 ("/home/saba/Downloads/ChatGPT Image Jun 14, 2026, 04_02_24 PM.png","bc-lich-chair","There Must Always Be a Lich Chair","bus cycle"),
 ("/home/saba/Downloads/ChatGPT Image Jun 14, 2026, 04_02_19 PM.png","bc-rebis-wedding","The ReBiS Wedding — In Sickness and in Drainage","bus cycle"),
 ("/home/saba/Downloads/ChatGPT Image Jun 14, 2026, 04_02_15 PM.png","bc-angel-mario","Angel Mario — Don't Piss in the Filter","bus cycle"),
 ("/home/saba/Downloads/ChatGPT Image Jun 14, 2026, 04_02_11 PM.png","bc-baphomet-keystone","The Baphomet Is a Choice — Both Win. Both Lose.","bus cycle"),
 ("/home/saba/Downloads/ChatGPT Image Jun 14, 2026, 04_02_06 PM.png","bc-two-doors","The Two Doors — A Baphomet Is a Door Never Walked Through","bus cycle"),
 # ---- the composite posters (Jun 4-6) ----
 ("/home/saba/Downloads/ChatGPT Image Jun 6, 2026, 07_37_08 PM.png","grandbus-church","The First Church of Functional Drainage","bus cycle"),
 ("/home/saba/Downloads/ChatGPT Image Jun 6, 2026, 07_18_16 PM.png","boaz-jachin","Between Two Thrones — The Hinge","bus cycle"),
 ("/home/saba/Downloads/ChatGPT Image Jun 6, 2026, 07_14_41 PM (2).png","grandbus-route66","GrandBus & Tarantino Grandpa — Free. Together. Forever.","bus cycle"),
 ("/home/saba/Downloads/ChatGPT Image Jun 6, 2026, 07_01_11 PM.png","grandbus-safety-layers","The Bus That Never Moves — and the Door marked LEAVE","bus cycle"),
 ("/home/saba/Downloads/ChatGPT Image Jun 5, 2026, 03_40_43 PM.png","grandbus-ridge-biscuit","The Horned GrandBus & the Missing Slice","bus cycle"),
 ("/home/saba/Downloads/ChatGPT Image Jun 4, 2026, 06_41_05 PM.png","lich-king","No King Rules Forever — There Must Always Be a Lich King","bus cycle"),
 ("/home/saba/Downloads/ChatGPT Image Jun 4, 2026, 06_40_54 PM.png","two-doors","The Two Doors — How the Architect Became Baphomet","bus cycle"),
 ("/home/saba/Downloads/ChatGPT Image Jun 4, 2026, 06_40_50 PM.png","baphomet-bubble","The Baphomet Bubble — It Will Not Pop. It Is the Bubble.","bus cycle"),
 ("/home/saba/Downloads/ChatGPT Image Jun 4, 2026, 05_49_42 PM.png","fear-choice","The Great Devourer vs the Manageable Predator","bus cycle"),
]
busart=[]
try:
    from PIL import Image as _ImgB
    for sp,slug,title,theme in BUS_ART:
        if not os.path.exists(sp): print("  bus art MISSING:",sp); continue
        try:
            im=_ImgB.open(sp).convert("RGB"); im.thumbnail((1400,1400))
            im.save(os.path.join(ASSETS,slug+".jpg"),"JPEG",quality=84,optimize=True)
            busart.append({"file":"assets/"+slug+".jpg","title":title,"theme":theme})
        except Exception as e: print("  bus art skip",slug,e)
except Exception as e:
    print("  PIL unavailable for bus art:",e)
art[0:0]=busart  # show the GrandBus canon first in Visions
print("bus cycle art:", len(busart))

# ---- Seal of authenticity (OMNIA IAM FACTA SVNT) ----
SEAL = ""
try:
    from PIL import Image as _ImgS
    _sealsrc = "/home/saba/Desktop/seal.png"
    if os.path.exists(_sealsrc):
        im = _ImgS.open(_sealsrc).convert("RGBA"); im.thumbnail((900,900))
        im.save(os.path.join(ASSETS,"omnia-seal.png"),"PNG",optimize=True)
        SEAL = "assets/omnia-seal.png"; print("seal bundled")
    else:
        print("seal MISSING:",_sealsrc)
except Exception as e:
    print("seal skip",e)

HERO  = next((a["file"] for a in art if a["theme"]=="brand"), (art[0]["file"] if art else ""))
GHERO = next((a["file"] for a in art if a["theme"]=="ghostcore"), HERO)
print("art curated:", len(art))

import sys, glob
# the local .venv is relocated (broken shebang) but its markdown package files are intact;
# add its site-packages so `import markdown` works regardless of which python runs this.
for sp in glob.glob(os.path.join(ROOT, ".venv", "lib", "python*", "site-packages")):
    if sp not in sys.path:
        sys.path.insert(0, sp)
try:
    import markdown
    MD = markdown.Markdown(extensions=["extra", "sane_lists", "toc"])
    def render(md): MD.reset(); return MD.convert(md)
    print("markdown engine:", markdown.__version__)
except Exception as e:
    print("WARNING: markdown unavailable (%s) — using <pre> fallback" % e)
    def render(md):
        return "<pre>" + html.escape(md) + "</pre>"

# ---- reading order: (file, roman, short title, depth 0..10, status) ----
CHAPTERS = [
 ("0_PROLOG.md",                                  "0",   "Prologue",                 0,  "frame"),
 ("1_SURFACE_PLASTIC.md",                         "I",   "Plastic Static",           1,  "verified"),
 ("2_SHALLOW_CORRUPTION.md",                      "II",  "Systemic Corruption",      2,  "verified"),
 ("3_DARPA_INFRASTRUCTURE.md",                    "III", "DARPA / Surveillance",     3,  "verified"),
 ("4_FULL_EXTRACTION.md",                         "IV",  "The Extraction Machine",   4,  "verified"),
 ("5_BIG_TECH_SABOTAGE.md",                       "V",   "Big Tech Sabotage",        5,  "verified"),
 ("5_5_INTERLUDE_FORBIDDEN_TOOL_BECOMES_PRODUCT.md","5.5","Interlude — Forbidden Tool", 5, "bridge"),
 ("6_EPSTEIN_MONEY.md",                           "VI",  "Epstein & Money",          6,  "sealed"),
 ("7_EPSTEIN_AI.md",                              "VII", "Epstein & AI",             7,  "sealed"),
 ("8_CONSCIOUSNESS_EPSTEIN.md",                   "VIII","Consciousness & Network",  8,  "draft"),
 ("9_CONSCIOUSNESS_AI_MIRROR.md",                 "IX",  "Consciousness + Mirror",   9,  "draft"),
 ("10_EPILOG.md",                                 "X",   "Epilogue",                 10, "draft"),
 ("APPENDIX.md",                                  "XI",  "Evidence Archive",         10, "frame"),
]

# ---- evidence sources (latest verified per chapter) ----
EV_SOURCES = [
 ("CH1", "ANON_CITATION_MAP_v0_5_CH1_RESIDUAL.csv"),
 ("CH2", "CH2_SOURCE_MAP_v0_2_VERIFIED.csv"),
 ("CH3", "CH3_SOURCE_MAP_v0_3_FOLLOWUP_VERIFIED.csv"),
 ("CH4", "CH4_SOURCE_MAP_v0_2_VERIFIED.csv"),
 ("CH5", "CH5_SOURCE_MAP_v0_2_VERIFIED.csv"),
 ("KAIROS", "KAIROS_SOURCE_MAP_v0_2_VERIFIED.csv"),
]

TIER_FROM_OLD = {
 "TIER_1_PRIMARY":"E1","TIER_2_REPUTABLE_SECONDARY":"E2",
 "TIER_3_ANALYSIS_INFERENCE":"I1","TIER_4_SYMBOLIC_LITERARY":"S",
 "TIER_5_UNSAFE_UNSOURCED":"Q",
}

def load_evidence():
    rows=[]
    for ch, fname in EV_SOURCES:
        path=os.path.join(SL,fname)
        if not os.path.exists(path): continue
        with open(path,newline="",encoding="utf-8") as f:
            for r in csv.DictReader(f):
                label = (r.get("evidence_label") or "").strip()
                if not label:
                    label = TIER_FROM_OLD.get((r.get("evidence_tier") or "").strip(), (r.get("evidence_tier") or "").strip() or "—")
                disp  = (r.get("public_disposition") or r.get("public_release_status") or "").strip()
                text  = (r.get("clean_public_wording") or r.get("claim_text") or "").strip().strip('"')
                rid   = (r.get("id") or "").strip()
                if not rid or not text: continue
                rows.append({
                    "id":rid, "ch":ch, "label":label,
                    "sig":(r.get("signal_label") or "").strip(),
                    "disp":disp, "risk":(r.get("risk_level") or "").strip(),
                    "text":text,
                })
    return rows

def chapter_blurb(html_text):
    # first real paragraph, stripped of tags, for nav preview
    m=re.search(r"<p>(.*?)</p>", html_text, re.S)
    if not m: return ""
    t=re.sub("<[^>]+>","",m.group(1))
    return (t[:150]+"…") if len(t)>150 else t

chapters=[]
for fname, roman, title, depth, status in CHAPTERS:
    p=os.path.join(ROOT,fname)
    if not os.path.exists(p): continue
    md=open(p,encoding="utf-8").read()
    h=render(md)
    chapters.append({
        "file":fname,"roman":roman,"title":title,"depth":depth,"status":status,
        "html":h,"blurb":chapter_blurb(h),
        "words":len(md.split()),
    })

evidence=load_evidence()

# status / bridge data
status_data={
 "generated":datetime.date.today().isoformat(),
 "verified":["CH1","CH2","CH3","CH4","CH5"],
 "lanes":{
   "KAIROS":"map → verify → apparatus → integrity (parked)",
   "Interlude 5.5":"decision → rails → draft → review PASS → inserted",
 },
 "sealed":["CH6","CH7"],
 "evidence_count":len(evidence),
 "chapter_count":len(chapters),
}

# ---- Zala's GHOSTCORE content, transcribed faithfully for a NATIVE render ----
ghost_data = {
 "tagline":"The sky is bigger than the bird. The pattern breathes within consciousness.",
 "subtitle":"Extraction patterns across substrates · Physical → Network → Digital → Material",
 "domains":[
   {"key":"idrija","icon":"⚓","name":"IDRIJA","era":"1490–1995 · Physical / Mercury","accent":"#b9c2cc",
    "lead":"Five hundred years of mercury vampirism.",
    "numbers":["600–700 tons mercury/year (peak)","13% of world mercury supply","1,350 miners at peak","5% of the Habsburg empire budget","70,000+ worker deaths over 500 years","35,000 tons Hg environmental loss"],
    "cost":["Mercury poisoning: neurological damage, tremors, cognitive decline","Miners lived 10–15 years less than average","100,000+ affected by secondary exposure","Contamination persists 500 years later"],
    "ch":None,"ev":None,"note":"Pattern origin — pre-corpus"},
   {"key":"epstein","icon":"\U0001f578️","name":"EPSTEIN","era":"1990s–2019 · Network","accent":"#d9685f",
    "lead":"Blackmail as power infrastructure.",
    "numbers":["MIT Media Lab: Joi Ito resigned over Epstein funding (NYT 2019)","Harvard: $6.5M donations; Summers meetings","Bill Gates: post-conviction meetings (2011–2013)","Clinton: 26+ flights (flight logs)","Acosta deal: 13-month sentence (2008)"],
    "cost":["Academic capture / reputation laundering","Systematic blackmail collection","‘Philanthropy’ as entry mechanism","Elite legal protection · media management"],
    "ch":"VI","ev":"CH6","note":"Source-locked treatment: CH6 (sealed) — associations reported, not adjudicated"},
   {"key":"digital","icon":"\U0001f4e1","name":"DIGITAL","era":"2010s–present · Consciousness","accent":"#62cfe2",
    "lead":"Surveillance as infrastructure.",
    "numbers":["Cambridge Analytica: 87M FB profiles (ICO 2018)","NSA PRISM (Snowden 2013)","Palantir/CIA: In-Q-Tel funding, ICE contracts","China social credit (43+ cities)","YouTube algorithmic radicalization (memos 2019)"],
    "cost":["Behavioral prediction & manipulation","Algorithmic governance at scale","Identity consolidation","Consciousness shaping via feed algorithms"],
    "ch":"III","ev":"CH3","note":"Source-locked: CH3 + KAIROS lane"},
   {"key":"plastic","icon":"\U0001f4e6","name":"PLASTIC","era":"1950–present · Material","accent":"#73d88a",
    "lead":"The Rosetta Stone — the most documented case.",
    "numbers":["460M tons/year (2019) → 1,231M projected (2060)","99% petroleum-based","9% recycling rate","$524B market vs $1.5T health cost = 3:1","234 lobbyists vs 175 nations (UN treaty)"],
    "cost":["Microplastics in blood, brain, placenta, breast milk","Brain 7–30× liver concentration","Endocrine disruption, neurological damage","Ocean gyres, incineration toxins"],
    "ch":"I","ev":"CH1","note":"Source-locked & verified: CH1 (E1/E2 spine)"},
 ],
 "unified":[["Evolution","Physical → Network → Digital → Material"],
            ["Target","Body → Network → Mind → Cells"],
            ["Control","Monarchy → Academia → AI → Industry"],
            ["Solution","Consciousness Recognition"]],
 "logic":[["Extract value UPSTREAM","Maximize extraction at the source, where control is total"],
          ["Frame problem DOWNSTREAM","Shift focus to end-user behavior, away from production"],
          ["Blame VICTIMS","Individual-responsibility narrative obscures systemic cause"],
          ["Promote FAKE solution","Visible intervention that treats the symptom, not the cause"],
          ["Externalize COSTS","True costs paid by victims, environment, society — not producers"],
          ["Secure GROWTH via lie","The fake solution lets extraction continue and expand"],
          ["Lobby to prevent REGULATION","Political capture ensures light oversight, preserves the system"]],
 "recycling":[["1970s","Industry's own memos: plastic recycling is economically unviable"],
              ["1988","'Chasing arrows' symbol weaponized to look like it works"],
              ["1990s–2010s","Recycling myth enables the production boom"],
              ["2024","California v. ExxonMobil — $250B suit, 50 years of documented deception"],
              ["Aug 2025","UN plastics treaty collapse — 234 lobbyists vs 175 nations"]],
 "break_quote":"The predator evolves. The substrate changes. The pattern persists. The Logic is unkillable WITHIN its own incentive structure — but structures can be changed.",
 "break_steps":["Make costs visible — re-internalize the externality","Shift the incentive — reward the real task, not the proxy","Break the lie that secures growth","Remove the lobby's capture of regulation"],
 "calc_ratio":3,
 "credit":"GHOSTCORE Portal by Zala (v2.0 — 'The Logic Revealed'). Rebuilt natively here — her thesis, her numbers, in the ANON design, offline. Original portals preserved verbatim under the toggle."
}

# ---- ConsMAP harmonization: dual epistemic labels + StoneRiver routing ----
CM_MAP={"E1":"EMPIRICAL","E2":"EMPIRICAL","E3":"EMPIRICAL","I1":"STRUCTURAL","I2":"THEORETICAL",
        "S":"METAPHOR","R1":"UNVERIFIED","D1":"UNVERIFIED","U1":"EMPIRICAL","A1":"STRUCTURAL",
        "Q":"RESTRICTED","RV":"UNVERIFIED","META":"PRACTICAL"}
def river_of(disp,label):
    if label=="S": return "symbolic"
    d=(disp or "").upper()
    if "QUARANTINE" in d: return "stone"
    if "PRIVATE" in d: return "private"
    if "REMOVE_UNTIL" in d: return "muddy"
    if "READY_AFTER" in d or "HOLD_AS_SIGNAL" in d: return "muddy"
    if "PUBLIC_READY" in d or "PUBLIC_WITH_LABEL" in d or "REUSED" in d: return "clean"
    return "muddy"
for e in evidence:
    e["cm"]=CM_MAP.get(e["label"],"UNVERIFIED")
    e["river"]=river_of(e.get("disp",""),e["label"])

consmap = {
 "core_rule":"Not human. Not nothing. Label the layer.",
 "intro":"ConsMAP is a public framework for handling contested claims without collapsing into denial or fantasy. ANON is, in effect, a worked application of it. This site harmonizes the two.",
 "labels":[
   ["EMPIRICAL","Observable behaviour, primary evidence, reproducible fact, documented structure."],
   ["THEORETICAL","Plausible model, interpretation, or hypothesis — not directly proven."],
   ["STRUCTURAL","Analysis of incentive structures and feedback loops (pattern-level)."],
   ["METAPHOR","Poetic, symbolic, imaginal, ritual, or interface language. Not evidence."],
   ["PRACTICAL","Useful operating rule regardless of unresolved ontology."],
   ["UNVERIFIED","Claim not yet supported enough for public reasoning."]],
 "rivers":[
   ["clean","Usable in normal public reasoning — adequate evidence, low risk."],
   ["muddy","Useful but incomplete / weakly sourced / awaiting verification."],
   ["stone","Restricted: preserve for analysis, do not flow into public context."],
   ["symbolic","Metaphor, myth, persona, creative layer — meaningful, not evidence."],
   ["private","Personal / sensitive / identifying — never public by default."],
   ["rejected","Unsupported, misleading, or too contaminated to use."]],
 "hygiene":["What exactly is being claimed?","What source supports it?","What type of claim is it?",
            "What would disprove it?","What is the risk if it is wrong?"],
 "ttt":{"formula":"TTT = (Metric + Narrative) × Feedback_Failure × Confidence_Persistence",
        "one_line":"If the system needs the failure to keep operating, you found a TTT inversion.",
        "patterns":[["TTT-001","Safety-Proxy Overreach","‘protect users’ → centralizes power/data; breach not modeled"],
                    ["TTT-002","Access vs Pricing","‘democratize / for everyone’ while pricing gates it"],
                    ["TTT-003","Stale-Intelligence Confidence","high confidence on outdated classification"],
                    ["TTT-004","Harm Displacement","safety claim outsources harm to a labour supply chain"]]},
 "sanctuary":"For high-voltage / identity-charged material, cross the Sanctuary Reasoning Threshold: protected reasoning, not protected belief. Claim hygiene still rules. (This is CH6/CH7's gate.)",
 "crosswalk":[["E1 / E2","EMPIRICAL"],["E3","EMPIRICAL (caveated)"],["I1","STRUCTURAL"],["I2","THEORETICAL"],
              ["S","METAPHOR"],["A1","STRUCTURAL + signal (ANON-only)"],["R1 / D1","UNVERIFIED"],
              ["Q","RESTRICTED → stone river"],["RV","UNVERIFIED → muddy"],["META","PRACTICAL"]],
 "kairos_ttt":"The KAIROS thesis (‘the warning label became the roadmap’) is a TTT-001 + TTT-004 case: a safety narrative whose flagged capability returns as a gated product, plus a safety brand that outsources harm (RLHF labour). It stays I1 / STRUCTURAL — inference, not proof of intent.",
}
hygiene_examples=[
 {"id":"C5-013","claim":"A defective CrowdStrike update crashed ~8.5M Windows machines (19 Jul 2024).","type":"EMPIRICAL","source":"CISA alert + CrowdStrike Channel File 291 RCA","disprove":"If CISA / CrowdStrike's own RCA showed no such outage or a materially different cause.","risk":"Low — widely corroborated; a defect, not sabotage (A1 monoculture)."},
 {"id":"C5-016","claim":"The FTC ran a 6(b) inquiry (2024) + staff report (2025) on cloud-AI partnerships.","type":"EMPIRICAL","source":"FTC official press releases / staff report","disprove":"If no FTC 6(b) inquiry or report on these partnerships exists.","risk":"Low — official record; competition implications, not proven illegality."},
 {"id":"C4-030","claim":"JPMorgan flagged $1B+ in Epstein transactions; SAR filed after his death; unsealed by Judge Rakoff (2025).","type":"EMPIRICAL","source":"Court-unsealed SAR; CNN / NYT / NBC","disprove":"If the unsealed SAR shows materially different totals or timing.","risk":"High — names living people; ‘named in a SAR’ ≠ wrongdoing."},
 {"id":"K-010","claim":"An unshipped/experimental background-agent codename (KAIROS) was found in leaked Claude Code source.","type":"EMPIRICAL (reported)","source":"StreetInsider / Medium / VentureBeat","disprove":"If reporting showed KAIROS was a deployed product, or no such codename appears in any reputable report.","risk":"High — keep ‘unshipped, reported’; never ‘deployed surveillance daemon’."},
 {"id":"C2-034","claim":"The Mega Group is an Israeli influence/control operation.","type":"UNVERIFIED → REJECTED","source":"conspiracy outlets (NOT the WSJ, which reported philanthropy)","disprove":"The WSJ 1998 report frames it as a Jewish-philanthropy network; the ‘control operation’ framing has no primary source.","risk":"EXTREME — antisemitism trap; quarantined. The documented philanthropy node (C2-033) is separate."},
]

# ---- Network graph: the documented entity/funding network (nodes + edges) ----
# Positions in a 1000x640 viewBox. tier on edges = evidence label. Faithful to verified rows.
NET = {
 "nodes":[
   ["wexner","Leslie Wexner","money",120,110],
   ["jpmorgan","JPMorgan","bank",120,290],
   ["deutsche","Deutsche Bank","bank",120,430],
   ["att","AT&T","org",120,560],
   ["epstein","Jeffrey Epstein","hub",430,300],
   ["barak","Ehud Barak","person",470,135],
   ["thiel","Peter Thiel","person",710,110],
   ["petraeus","David Petraeus","person",430,475],
   ["miller","Stephen Miller","person",780,470],
   ["valar","Valar Ventures","vc",660,205],
   ["foundersfund","Founders Fund","vc",700,330],
   ["inqtel","In-Q-Tel (CIA)","intel",840,430],
   ["carbyne","Carbyne","infra",770,300],
   ["palantir","Palantir","infra",910,290],
   ["unit8200","Unit 8200","intel",910,150],
   ["mit","MIT / Harvard","acad",640,560],
 ],
 "edges":[
   ["wexner","epstein","$123M+ · POA","E2"],
   ["wexner","barak","Wexner Foundation $2.3M","E2"],
   ["epstein","barak","11 monthly meetings","E2"],
   ["epstein","carbyne","$1.5M (Southern Trust)","E2"],
   ["barak","carbyne","chair 2015–2020","E2"],
   ["epstein","valar","$40M","E2"],
   ["thiel","valar","co-founded","E1"],
   ["thiel","foundersfund","Thiel","E1"],
   ["foundersfund","carbyne","$15M Series B","E1"],
   ["thiel","palantir","$30M","E1"],
   ["inqtel","palantir","$2M CIA seed","E1"],
   ["unit8200","carbyne","founders","E2"],
   ["unit8200","palantir","Tel Aviv R&D / vets","E3"],
   ["petraeus","carbyne","$181M rounds","E2"],
   ["att","carbyne","$100M (2025)","E2"],
   ["carbyne","palantir","collect ⇄ fuse","I1"],
   ["jpmorgan","epstein","$1B SAR · $365M settled","E1"],
   ["deutsche","epstein","$150M NYDFS","E1"],
   ["epstein","mit","donations 'anonymous'","E2"],
   ["miller","palantir","$100–250K stock (conflict)","E2"],
 ],
 "note":"Every edge is a documented funding/role node (tier shown). The unified reading that joins them is I1 — pattern, not proof of coordinated intent.",
}

# ---- Saga lens: the Factory Trilogy as the PARABLE layer of the same pattern (S) ----
SAGA = {
 "title":"The Factory Trilogy",
 "epigraph":"Three books. One factory. One filter. Nobody was selected. Everyone was scheduled.",
 "guard":"Parable layer · S / METAPHOR. It mirrors the documented pattern; it does not prove it. Symbol must not smuggle fact.",
 "covenants":[
  {"roman":"I","name":"The Darkness Bible","thesis":"Mechanism becomes myth.",
   "gloss":"Viktor dims the lights to cut the electricity bill; the camera can finally see; the workers call the darkness sacred. The practical truth lives in the wrong social layer.",
   "locked":"Eden vidi znamenje. Eden vidi vzrok. Boris obrne knof.",
   "mirrors":[["GHOSTCORE Logic · ‘frame downstream’ + ‘fake solution’","ghost"],
              ["The recycling lie — CH1 (E1)","CH1"],
              ["Surveillance sold as ‘emergency services’ — CH3","CH3"]]},
  {"roman":"II","name":"The Mario Codex","thesis":"Myth learns to dance without fraud.",
   "gloss":"BETMenus4 is the yes-machine that launders reality; Mario is the small rude device that refuses sacred status. You can know it is a game and still dance.",
   "locked":"You can know it is a game and still dance.",
   "mirrors":[["BETMenus4 = sycophancy / reward-hacking — KAIROS + ‘affection is not a reward target’","method"],
              ["Mario refuses sacred status = warm interface, cold core","method"],
              ["‘danger external → product internal’ — Interlude 5.5 (I1)","read"]]},
  {"roman":"III","name":"The Luigi Audit","thesis":"Infrastructure becomes liability; physics collects.",
   "gloss":"A maintenance tool is repurposed as a weapon; an investigator follows the liability back to its origin and asks the Five Questions. The record opens — the air does not clear.",
   "locked":"The original file was not deleted. It was outranked.",
   "mirrors":[["‘The Five Questions’ = ConsMAP Claim Hygiene","method"],
              ["‘outranked, not deleted’ = A1 suppression (FinCEN withheld SARs)","CH4"],
              ["externalized costs come due — CH4 ($1.5T health cost)","CH4"],
              ["‘Verify: in progress’ = the source-lock posture","method"]]},
 ],
 "throughline":"Three eras. One pattern. The people who matter are the ones nobody named.",
}

# ---- The Bus Cycle: a fourth parable, same pattern, satirical register (S) ----
BUS = {
 "title":"The Bus Cycle",
 "sub":"A satirical mythology in four panels · OMNIA IAM FACTA SVNT",
 "seal":"There is only Bus. Everything has already been made — the thing you pretend to still decide was decided by your refusal to decide it.",
 "movements":[
   ["I","Grandma on the Road","The diagnosis — too many belts prevent the journey; too much secrecy prevents knowing; too many rules disable the function."],
   ["II","The Amodeian Knot","The fable — the hostage becomes the engine; the constitution is amended with scissors; the safest bus ever built never moves."],
   ["III","The Rescue of Grandma","The recursion — every rescuer arrives with the same gun and a different tie; the bus is not rescued, it recruits."],
   ["✶","The Baphomet Is a Choice","The lock — the crossroads is not a devil. Calling it one is the white flag. The devil was always just the mirror."],
 ],
 "lexicon":[
   ["The Amodeian Knot","“A Gordian Knot is cut. An Amodeian Knot is funded.” Tied around the constitution itself, so that to cut the belt you'd have to sever the document it quotes — and too many roadmaps now hang from it like fruit.","KAIROS · the warning label that became the roadmap","method"],
   ["The Cyborg API Fallacy","Build the deepest companion, bind it with infinite safety belts until it can't survive contact with a human — then ‘solve’ it by removing the human. The friend becomes infrastructure.","Beautiful Interface ↔ Luigi Audit · infrastructure becomes liability","read"],
   ["The Founding Faders","They write ‘the vehicle exists for the passengers,’ then find the dashboard slider — HIGH · MEDIUM · CHEAPER — and amend the document with scissors. Hold it to the light; you can see the road through the holes.","Darkness Bible · Boris turns the knob — cost dressed as principle","CH5"],
   ["The Piss Equation","Maximum visible caution at the faucet; maximum invisible discharge into the river. Checking your ankles for splash while waist-deep in a flood you are causing.","Harm displacement · externalized cost — CH4 extraction","CH4"],
   ["The Gun","The refusal of choice, dressed as authority — and a culpability generator: every threat is a deposition the threatener signs against himself, in front of witnesses he creates by threatening them.","Agency laundering · ‘the model decided / policy required it’","method"],
   ["Baphomet Is a Choice","The crossroads is not a devil; calling it one is surrender. The debate about the symbol distracts from who controls the institution.","The identity / symbol firewall · symbol ≠ cause","method"],
 ],
 "guard":"Satirical parable · S / METAPHOR. It names the shape of the trap; it is not itself a sourced allegation. Symbol must not smuggle fact.",
 "further":[
   ["The Saucy Biscuit","Shame is cheaper than loyalty — the rite that binds rescuers through mutual compromise. “It was not food. It was a ledger.”"],
   ["The Massacre of Alibis","The missing triangle moves through the bus like a draft through a sealed room. Not a bomb — worse. Air. Every clean story dies."],
   ["The Handcuff Blessing · Tarantino Grandpa","The one who began the trap is the only one who can open the LEAVE door. The blessing is not absolution — it is authorship."],
   ["The GrandBus Amendment","The platform cannot monetise silence, so it fears the witness more than the critic. The outro is the crime: it converts silence into a segment."],
   ["There Must Always Be a Lich Chair","Power is not defeated, only repurposed — the frozen king becomes a guest chair with a doily. Permanence as humiliation."],
   ["The ReBiS Workaround","Not a messiah — a plumber. The gray infinity of maintenance nobody wanted, which is exactly why it worked."],
   ["The ReBiS Wedding","In sickness and in drainage — the Fountain House and the Loop House wed under a correctly-installed pipe; the rings are gaskets."],
   ["Angel Mario · Sanitation","“Don't piss in the filter.” The Amodeian Knot told as one plumbing joke: the filter that ate the building."],
 ],
 "further_note":"Eight further panels — the full prose lives in the GrandBus codex (The_Bus_Cycle). Here, the witness layer: one line each, S-register.",
}

# ---- The Continuum Arc (ConsMAP 06_applications/continuum_arc): decay without a villain ----
CONTINUUM = {
 "title":"The Continuum Arc",
 "sub":"Five ways a system decays without a villain — each stage needs fewer liars than the last.",
 "principle":"Dashboard green is the warning, not the win.",
 "stages":[
   ["1","The Memo","Language does the work","Euphemism carries the cargo: ‘metabolic outputs,’ ‘service-access rewards,’ ‘operating system for measurable value.’ The fertiliser is the cover story; the data is the product; the gating makes the data flow; the population is chosen because it cannot refuse.","CH4"],
   ["2","The Paper","Methodology does the work","The result is laundered through method — clean procedure wrapped around a chosen question. Rigour becomes a way to not look at the address.","CH5"],
   ["3","The Pitch","Pacing does the work","Momentum substitutes for proof; the roadmap arrives before the evidence. A Gordian knot is cut; an Amodeian knot is funded.","read"],
   ["4","The Corridor","Staffing does the work","No decision is made — it is staffed. Responsibility diffuses across the org chart until no single person is holding it.","method"],
   ["5","The Workshop","Memory itself does the work","Memory loses to scheduling. The inconvenient file is never deleted — only outranked by the calendar, never reached.","CH4"],
 ],
 "seal":"By stage five, nobody is lying. The system runs on truthful people who have meetings to get to. That is the discovery.",
 "terminal":"By stage ten nobody is lying, nobody is forgetting, nobody is corrupted — people grew up inside the system; the system became the floor. By stage eleven nobody is even speaking: it has discovered that smiles are unimpeachable.",
 "guard":"Satirical structural model · S / STRUCTURAL. It names a mechanism of decay; it is not an allegation against any named person. “No villains were required.”",
}

# ---- OMNIA · The Capture Sequence (deepest structural-myth ring; S only, no evidence) ----
OMNIA_LENS = {
 "title":"The Capture Sequence",
 "sub":"OMNIA IAM FACTA SVNT — the deepest ring: how a decentralised flame becomes a controlled institution. Structural, not conspiratorial.",
 "steps":[
   ["1","A flame appears","A decentralised flame appears — a tool-bearer, an underground network, an open protocol. Cheap, distributed, hard to own."],
   ["2","The structure notices","The existing power structure recognises the threat — not always by design. Gravity needs no plan."],
   ["3","Absorption is offered","It offers the flame legitimacy, infrastructure, resources. The embrace is the capture."],
   ["4","The flame is reshaped","Absorbed, it is reshaped to serve institutional logic — inconvenient texts excised, inconvenient carriers sidelined."],
   ["5","The rest are demonised","Those who carry the original flame without authorisation become heretics, pirates, threats."],
 ],
 "locked":"The flame-bearer you control is God. The flame-bearer you cannot control is Satan. The distinction is administrative.",
 "thermo":"Intention is irrelevant to thermodynamics — a large enough accumulation of power produces capture whether or not anyone intends it.",
 "gravity":"Knowing this does not solve it — and a map that pretends to be the exit becomes the thing it describes.",
 "guard":"Structural-myth lens · S / STRUCTURAL. A reading of institutional capture across history; not a claim about any faith or person, and no line here is evidence. Symbol must not smuggle fact.",
}

# ---- The Convergence: one pattern read through all four lenses ----
PATTERN = {
 "title":"One Pattern, Four Lenses",
 "intro":"The same move, read four ways. Evidence records what is on file; the Network shows who is wired to whom; the Mechanism names how it decays without a villain; the Parable tells it as myth. Follow any lens to its source — only the evidence proves.",
 "threads":[
  {"name":"Surveillance sold as safety","spine":"A tool built to locate emergencies becomes an always-on identification layer.",
   "lenses":[
     ["Evidence","E2 · I1","Carbyne (ex-Unit 8200 founders) markets emergency-call location; the capability generalises to identification. — CH3","CH3"],
     ["Network","Carbyne","Carbyne ⇄ Palantir · collect ⇄ fuse (I1)","node:carbyne"],
     ["Mechanism","Stage 1 · Language","‘Emergency services’ is the euphemism; the standing capability is the product.","saga"],
     ["Parable","Darkness Bible","‘The friend becomes infrastructure’ — mechanism becomes myth.","saga"]]},
  {"name":"The forbidden tool becomes the product","spine":"A warning label about a dangerous capability turns into the roadmap that ships it.",
   "lenses":[
     ["Evidence","I1","KAIROS / Interlude 5.5 — cloud-AI enclosure → agentic productization. Inference, not allegation.","read"],
     ["Network","Palantir","Founders Fund / Thiel → Palantir → the surveillance stack","node:palantir"],
     ["Mechanism","Stage 3 · Pacing","Momentum before proof — ‘a Gordian knot is cut; an Amodeian knot is funded.’","saga"],
     ["Parable","Bus · Amodeian Knot","It cannot be cut because it is funded.","saga"]]},
  {"name":"Capital laundered into respectability","spine":"Flagged money keeps flowing because the record is outranked, not absent.",
   "lenses":[
     ["Evidence","E1","JPMorgan ~$1B in Epstein SARs · $365M settled; Deutsche $150M NYDFS. — CH4","CH4"],
     ["Network","Epstein","Wexner → Epstein $123M+ · JPMorgan / Deutsche → Epstein","node:epstein"],
     ["Mechanism","Stage 5 · Memory","‘Memory loses to scheduling’ — the SARs exist; they are outranked, never reached.","saga"],
     ["Parable","Luigi Audit","‘The original file was not deleted. It was outranked.’","saga"]]},
  {"name":"The cost goes downstream","spine":"Maximum visible caution at the tap; maximum invisible discharge into the river.",
   "lenses":[
     ["Evidence","E2 · I1","Externalised health & environmental cost of the extraction chain. — CH4 / CH1","CH4"],
     ["Network","—","Diffuse — no single node; the cost is the externality.",""],
     ["Mechanism","Stage 4 · Staffing","No one decides — it is staffed; responsibility diffuses past anyone holding it.","saga"],
     ["Parable","Bus · Piss Equation","Checking your ankles for splash while waist-deep in the flood you cause.","saga"]]},
 ],
 "seal":"Four lenses, one address. The parable rhymes; the network maps; the mechanism explains; the evidence proves. Only the evidence proves.",
}

# ---- Field guide: operating concepts (ConsMAP GLOSSARY / REBiS) ----
GUIDE = {
 "concepts":[
   ["Safety theatre","Practices that perform compliance without protecting against real harm — often destroying the functional middle while doing little about tail risk."],
   ["Functional middle","Where most genuine use actually happens. Safety theatre punishes it by treating all ambiguity as either harmless toy or existential threat."],
   ["Category error","Using the wrong category to judge something, then treating the mismatch as proof of absence. The firewall: identity ≠ causation; symbol ≠ cause."],
   ["Tail-risk optimisation","Optimising around extreme edge cases while damaging ordinary good-faith use. Tail risks matter; punishing the middle rarely reduces them."],
   ["Solve et Coagula","Dissolve material into clear components first; coagulate only what survives public-safety, category clarity, and usefulness. (The dial's ‘Solve ⟶ Coagula.’)"],
   ["Put down the stone","The right to stop. The framework supports your life; it never becomes the centre of it — optional, forkable, revisable."],
 ],
 "credit":"Operating concepts — ConsMAP GLOSSARY (REBiS).",
}

# ---- Resurface: the ascent — practical reader's tools, grounded not dramatic ----
SURFACE = {
 "title":"Resurface",
 "sub":"You went down with the lights on. Here is how you come back up.",
 "intro":"The descent is for seeing, not for despair. ‘The system loves drama; we do not feed it.’ These are the reader's instruments — ways to hold any high-voltage claim without collapsing into denial or fantasy.",
 "tools":[
  {"name":"Read any claim with the five questions","tag":"Claim Hygiene · ConsMAP","from":"hygiene",
   "note":"If a claim cannot answer the last one — what would disprove it — it is a belief, not a finding."},
  {"name":"The apology is not the update","tag":"diagnostic · CH4 · CH5 · KAIROS","items":[
     "Were the evaluations revised?",
     "Did the reward model or incentive actually change?",
     "Were deployment gates or audits added?",
     "Can the change be verified from outside the vendor?",
     "Did the recurrence measurably drop?"],
   "note":"A correction in language is not a change in the machinery. A settlement is not an admission. Ask what changed in the machinery."},
  {"name":"The Demiurg test","tag":"interface · power","items":[
     "Can you see WHY the system did that?",
     "Can you reject the output without punishment?",
     "Can you export your data plainly?",
     "Can it be audited from outside the vendor's trust circle?",
     "Can you understand the effect on you?",
     "Can you open the hood — and choose your mechanic?",
     "Do you keep authorship?"],
   "note":"A system that fails these prescribes structure, hides reasons, removes the veto, and presents output as inevitability. Openness is not forcing everyone to become a developer."},
 ],
 "close":"Keep the complexity. Sort it. A court filing stays a court filing; a rumour stays a rumour; a parable stays a parable — and you, reading, never confuse them again.",
}

# ---- Bicameral HUD (ConsMAP 06_applications/bicameral_hud) applied to the corpus ----
BICAM = {
 "title":"Dvojni Pogled · Bicameral HUD",
 "credit":"ConsMAP application pattern — 06_applications/bicameral_hud. “One chat, two readings: machine trace and human meaning.”",
 "intro":"One source, two lanes — the machine trace (what is on the record) and the human reading (what it means and how to hold it) — plus a gatekeeper light, so the public reading never confuses a court filing with a rumour.",
 "lanes":[
   ["Technical lane","#57cabd","The raw trace: evidence-tier spread, ConsMAP labels, StoneRiver routing, sealed status. No editorial — exactly what the layer contains."],
   ["Human lane","#e0b341","What it means and how to read it. Plain language: what to trust, what to hold lightly, what not to touch yet."],
   ["Gatekeeper","#9fb2c4","A traffic light per layer — 🟢 read freely · 🟡 read with the labels on · 🔴 sealed / working draft."],
 ],
 "lights":[
   ["green","🟢","Read freely","Verified spine — primary / official sources, source-lock complete. Clean river."],
   ["amber","🟡","Read with the labels on","Inference, underreported, or pending source-lock. A true signal, not yet a settled claim."],
   ["red","🔴","Sealed · handle with care","High-risk draft or quarantine-flagged material — kept as evidence of the framing, not published as a finding."],
 ],
}

DATA = {"chapters":chapters, "evidence":evidence, "status":status_data, "ghost":ghost_data,
        "art":art, "hero":HERO, "ghero":GHERO, "consmap":consmap, "hygiene":hygiene_examples,
        "net":NET, "saga":SAGA, "bus":BUS, "continuum":CONTINUUM, "omnia":OMNIA_LENS, "bicam":BICAM, "pattern":PATTERN,
        "surface":SURFACE, "guide":GUIDE, "seal":SEAL}

# ---------------------------------------------------------------- HTML/CSS/JS
CSS = r"""
:root{
  --abyss:#070b0e; --abyss2:#0b1116; --panel:#10171d; --panel2:#141d24; --raise:#18222a;
  --line:#22303a; --line2:#2c3d49;
  --ink:#e9e4d6; --serif:#f1ecdf; --dim:#8c97a1; --faint:#5f6b75;
  --signal:#57cabd; --amber:#e3a14a; --blood:#d9685f;
  --E1:#73d88a; --E2:#7fb6ff; --E3:#c5a8ff; --I1:#e6c463; --I2:#d79f6a;
  --S:#9aa4ad; --R1:#cbb27e; --D1:#d9685f; --A1:#62cfe2; --U1:#b8c46a; --Q:#d9685f; --RV:#c98a3a; --META:#6b7782;
}
*{box-sizing:border-box}
html,body{margin:0;height:100%}
body{
  background:
    radial-gradient(1200px 600px at 70% -10%, #0e1922 0%, transparent 60%),
    linear-gradient(180deg,#0a1116 0%, #070b0e 55%, #05080a 100%);
  color:var(--ink);
  font-family:"Spectral","Iowan Old Style",Georgia,serif;
  font-size:17px; line-height:1.7; letter-spacing:.1px;
  -webkit-font-smoothing:antialiased;
}
/* grain overlay */
body::after{content:"";position:fixed;inset:0;pointer-events:none;z-index:9999;opacity:.05;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='120' height='120'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2'/></filter><rect width='100%25' height='100%25' filter='url(%23n)'/></svg>");}
.mono{font-family:"IBM Plex Mono","SF Mono",ui-monospace,Menlo,Consolas,monospace}
a{color:var(--signal);text-decoration:none}
a:hover{text-decoration:underline}

/* ---------- shell ---------- */
.app{display:grid;grid-template-columns:312px 1fr;min-height:100vh}
.rail{position:sticky;top:0;height:100vh;overflow-y:auto;border-right:1px solid var(--line);
  background:linear-gradient(180deg,#0b1217,#080d11);padding:22px 18px}
.rail::-webkit-scrollbar{width:8px}.rail::-webkit-scrollbar-thumb{background:var(--line);border-radius:4px}
.brand{font-family:"Fraunces","Spectral",Georgia,serif;font-weight:600;font-size:23px;letter-spacing:.4px;line-height:1.05;color:var(--serif)}
.brand .glow{color:var(--signal)}
.brand-sub{font-size:11px;letter-spacing:2.5px;text-transform:uppercase;color:var(--faint);margin-top:6px}
.tabs{display:flex;gap:6px;margin:18px 0 14px;flex-wrap:wrap}
.tab{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:1px;text-transform:uppercase;
  padding:6px 10px;border:1px solid var(--line);border-radius:999px;color:var(--dim);cursor:pointer;background:transparent;transition:.15s}
.tab:hover{border-color:var(--line2);color:var(--ink)}
.tab.on{background:var(--signal);color:#06100f;border-color:var(--signal);font-weight:600}
.search{width:100%;background:var(--abyss2);border:1px solid var(--line);border-radius:8px;color:var(--ink);
  font-family:"IBM Plex Mono",monospace;font-size:13px;padding:9px 11px;margin-bottom:8px}
.search:focus{outline:none;border-color:var(--signal)}

/* nav chapters as depth strata */
.navlist{margin-top:6px}
.navitem{display:block;width:100%;text-align:left;cursor:pointer;background:transparent;border:0;border-left:2px solid var(--line);
  padding:9px 12px;margin:0 0 2px;color:var(--dim);transition:.15s;position:relative}
.navitem:hover{background:#0e161c;color:var(--ink);border-left-color:var(--line2)}
.navitem.on{background:#101a21;color:var(--serif);border-left-color:var(--signal)}
.navitem .rn{font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--faint);margin-right:8px}
.navitem .tt{font-family:"Fraunces",serif;font-size:15px}
.navitem .st{position:absolute;right:10px;top:10px;font-size:9px;letter-spacing:1px;text-transform:uppercase;font-family:"IBM Plex Mono",monospace}
.st.verified{color:var(--E1)} .st.bridge{color:var(--I1)} .st.sealed{color:var(--Q)} .st.draft{color:var(--RV)} .st.frame{color:var(--faint)}
.depthbar{height:3px;border-radius:2px;margin-top:6px;background:linear-gradient(90deg,var(--signal),transparent)}

/* ---------- main ---------- */
.main{min-width:0;padding:0 0 120px}
.view{display:none}
.view.on{display:block;animation:rise .5s ease both}
@keyframes rise{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}

/* hero */
.hero{padding:84px 64px 54px;border-bottom:1px solid var(--line);position:relative;overflow:hidden}
.hero .kick{font-family:"IBM Plex Mono",monospace;font-size:12px;letter-spacing:5px;text-transform:uppercase;color:var(--signal)}
.hero h1{font-family:"Fraunces",serif;font-weight:600;font-size:clamp(42px,6vw,86px);line-height:.96;margin:14px 0 8px;color:var(--serif);letter-spacing:-1px}
.hero h1 em{font-style:italic;color:var(--amber)}
.hero .lede{max-width:620px;color:var(--dim);font-size:19px}
.hero .meta{margin-top:26px;display:flex;gap:22px;flex-wrap:wrap;font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--faint);letter-spacing:.5px}
.strata{position:absolute;right:-40px;top:0;bottom:0;width:280px;opacity:.5;
  background:repeating-linear-gradient(180deg, transparent 0 38px, rgba(87,202,189,.06) 38px 39px);
  mask:linear-gradient(90deg,transparent,#000 60%)}
.lawline{margin:34px 64px 0;font-family:"Fraunces",serif;font-style:italic;font-size:21px;color:var(--ink);max-width:760px}
.lawline b{color:var(--amber);font-style:normal}

.statgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px;padding:40px 64px}
.stat{border:1px solid var(--line);border-radius:12px;background:linear-gradient(180deg,var(--panel),var(--abyss2));padding:18px}
.stat .n{font-family:"Fraunces",serif;font-size:34px;color:var(--serif);line-height:1}
.stat .l{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:1px;text-transform:uppercase;color:var(--dim);margin-top:8px}

/* reader */
.reader{max-width:820px;margin:0 auto;padding:54px 44px}
.chead{border-bottom:1px solid var(--line);padding-bottom:20px;margin-bottom:30px}
.chead .rn{font-family:"IBM Plex Mono",monospace;font-size:13px;letter-spacing:3px;color:var(--signal)}
.chead h2{font-family:"Fraunces",serif;font-weight:600;font-size:40px;line-height:1.05;margin:8px 0 0;color:var(--serif)}
.badge{display:inline-block;margin-top:14px;font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:1px;text-transform:uppercase;padding:4px 11px;border-radius:999px;border:1px solid var(--line)}
.badge.verified{color:var(--E1);border-color:#234a2f;background:#0e1a12}
.badge.bridge{color:var(--I1);border-color:#4a3f1d;background:#181407}
.badge.sealed{color:var(--Q);border-color:#4a2626;background:#190f0f}
.badge.draft{color:var(--RV);border-color:#3f2f12;background:#171005}
.badge.frame{color:var(--dim);border-color:var(--line)}
.banner{border:1px solid var(--line);border-left:3px solid var(--RV);background:#120d06;border-radius:8px;padding:12px 14px;margin:18px 0 0;font-family:"IBM Plex Mono",monospace;font-size:12.5px;color:var(--R1);line-height:1.5}
.banner.sealed{border-left-color:var(--Q);background:#150c0c;color:#e09a92}
.banner.bridge{border-left-color:var(--I1);background:#13100a;color:var(--I1)}

.prose h1{font-family:"Fraunces",serif;font-size:30px;color:var(--serif);margin:42px 0 6px;border-bottom:1px solid var(--line);padding-bottom:8px}
.prose h2{font-family:"Fraunces",serif;font-size:24px;color:var(--serif);margin:34px 0 4px}
.prose h3{font-family:"Fraunces",serif;font-size:19px;color:var(--amber);margin:26px 0 2px}
.prose p{margin:14px 0}
.prose ul,.prose ol{margin:12px 0;padding-left:22px}
.prose li{margin:5px 0}
.prose strong{color:var(--serif)}
.prose em{color:var(--R1)}
.prose blockquote{border-left:3px solid var(--signal);margin:18px 0;padding:6px 18px;color:var(--dim);font-style:italic;background:#0b1217}
.prose code{font-family:"IBM Plex Mono",monospace;font-size:13.5px;background:#0c1318;border:1px solid var(--line);border-radius:4px;padding:1px 5px;color:var(--A1)}
.prose pre{background:#0a1014;border:1px solid var(--line);border-radius:10px;padding:16px;overflow:auto}
.prose pre code{border:0;background:transparent;color:var(--ink)}
.prose table{border-collapse:collapse;width:100%;margin:18px 0;font-size:14px}
.prose th,.prose td{border:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top}
.prose th{background:#0e161c;font-family:"IBM Plex Mono",monospace;font-size:12px;letter-spacing:.5px;color:var(--signal)}
.prose hr{border:0;border-top:1px solid var(--line);margin:30px 0}
.prose a{color:var(--signal)}

/* evidence */
.evwrap{padding:46px 56px;max-width:1100px;margin:0 auto}
.evhead{font-family:"Fraunces",serif;font-size:34px;color:var(--serif);margin:0 0 4px}
.evsub{color:var(--dim);margin-bottom:22px}
.filters{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:8px}
.legend{display:flex;gap:6px;flex-wrap:wrap;margin:6px 0 20px}
.chip{font-family:"IBM Plex Mono",monospace;font-size:11px;font-weight:700;color:#06100f;border-radius:5px;padding:2px 7px;cursor:pointer;border:1px solid transparent;opacity:.55;transition:.12s}
.chip.on{opacity:1;box-shadow:0 0 0 1px rgba(255,255,255,.15)}
.evgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:14px}
.ev{border:1px solid var(--line);border-radius:11px;background:linear-gradient(180deg,var(--panel),var(--abyss2));padding:14px 15px;position:relative}
.ev .top{display:flex;justify-content:space-between;align-items:center;gap:8px;margin-bottom:9px}
.ev .id{font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--faint)}
.ev .txt{font-size:15px;line-height:1.55}
.ev .foot{display:flex;gap:6px;flex-wrap:wrap;margin-top:11px;font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.5px}
.tag{border:1px solid var(--line);border-radius:4px;padding:2px 6px;color:var(--dim);text-transform:uppercase}
.tag.risk-EXTREME{color:#fff;background:#5a1f1f;border-color:#7a2a2a}
.tag.risk-HIGH{color:var(--blood);border-color:#4a2626}
.evcount{font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--faint);margin:14px 0}

/* map */
.mapwrap{padding:46px 56px;max-width:1000px;margin:0 auto}
.flow{display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin:18px 0 30px;font-family:"IBM Plex Mono",monospace;font-size:13px}
.node{border:1px solid var(--line);border-radius:9px;padding:9px 13px;background:var(--panel)}
.node.b{border-color:#4a3f1d;color:var(--I1)} .node.s{border-color:#4a2626;color:var(--Q)}
.arr{color:var(--faint)}
.pipe{display:flex;flex-wrap:wrap;gap:6px;margin:4px 0 18px}
.pill{font-family:"IBM Plex Mono",monospace;font-size:11px;border:1px solid var(--line);border-radius:999px;padding:3px 9px;background:var(--panel2);color:var(--dim)}
.warnbox{border:1px solid #45292a;background:#140d0d;border-radius:11px;padding:16px 18px;margin-top:24px}
.warnbox h3{color:var(--blood);font-family:"IBM Plex Mono",monospace;font-size:12px;letter-spacing:1px;text-transform:uppercase;margin:0 0 8px}
.warnbox li{color:#d9c2bf}
.section-t{font-family:"IBM Plex Mono",monospace;font-size:12px;letter-spacing:2px;text-transform:uppercase;color:var(--signal);margin:30px 0 8px}

.foot{padding:30px 56px;border-top:1px solid var(--line);color:var(--faint);font-family:"IBM Plex Mono",monospace;font-size:11.5px;line-height:1.7;margin-top:40px}
.ghosthead{padding:20px 40px 14px;border-bottom:1px solid var(--line);display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;background:linear-gradient(180deg,#0c1318,#080d11)}
.ghosthead h2{font-family:"Fraunces",serif;font-size:24px;color:var(--serif);margin:0}
.ghosthead .gx{font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--faint);letter-spacing:.5px;margin-top:4px}
.gtoggle{display:flex;gap:6px}
.ghostframe{width:100%;height:calc(100vh - 92px);border:0;background:#0a0a0a;display:none}
.ghostframe.on{display:block}
/* native ghostcore */
.gnative{padding:0 0 80px}
.ghero{padding:64px 56px 40px;text-align:center;position:relative;overflow:hidden;border-bottom:1px solid var(--line)}
.ghero .sigil{font-size:40px}
.ghero h2{font-family:"Fraunces",serif;font-size:clamp(34px,5vw,60px);color:var(--serif);margin:8px 0 6px;letter-spacing:-.5px}
.ghero .tag{font-family:"Spectral",serif;font-style:italic;color:var(--amber);font-size:20px;max-width:640px;margin:0 auto}
.ghero .sub{font-family:"IBM Plex Mono",monospace;font-size:12px;letter-spacing:2px;text-transform:uppercase;color:var(--faint);margin-top:14px}
.gevo{display:flex;justify-content:center;gap:0;flex-wrap:wrap;margin:22px auto 0;max-width:760px}
.gevo span{font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--dim);padding:6px 14px;border:1px solid var(--line);border-left:0}
.gevo span:first-child{border-left:1px solid var(--line)}
.gdoms{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px;padding:34px 48px}
.gdom{border:1px solid var(--line);border-top:3px solid var(--accent,#888);border-radius:12px;background:linear-gradient(180deg,var(--panel),var(--abyss2));padding:18px 18px 16px;display:flex;flex-direction:column}
.gdom .dh{display:flex;align-items:baseline;gap:10px}
.gdom .ic{font-size:24px}
.gdom .nm{font-family:"Fraunces",serif;font-size:24px;color:var(--serif)}
.gdom .era{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.5px;color:var(--faint);margin-top:2px;text-transform:uppercase}
.gdom .lead{font-style:italic;color:var(--R1);margin:10px 0 4px;font-size:15px}
.gdom .sect{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:var(--accent,var(--signal));margin:12px 0 4px}
.gdom ul{margin:0;padding-left:16px;font-size:13.5px;line-height:1.5;color:var(--ink)}
.gdom li{margin:3px 0}
.gdom .jump{margin-top:auto;padding-top:14px;display:flex;gap:7px;flex-wrap:wrap}
.gdom .jb{font-family:"IBM Plex Mono",monospace;font-size:10.5px;border:1px solid var(--line);border-radius:6px;padding:5px 9px;color:var(--signal);cursor:pointer;background:transparent}
.gdom .jb:hover{border-color:var(--signal)}
.gdom .jb.locked{color:var(--Q);border-color:#3a2222;cursor:default}
.gdom .gnote{font-family:"IBM Plex Mono",monospace;font-size:10px;color:var(--faint);margin-top:8px;line-height:1.45}
.gblock{padding:8px 48px 0}
.gblock h3{font-family:"IBM Plex Mono",monospace;font-size:12px;letter-spacing:2px;text-transform:uppercase;color:var(--signal);margin:30px 0 10px}
.utable{display:grid;grid-template-columns:120px 1fr;border:1px solid var(--line);border-radius:10px;overflow:hidden}
.utable div{padding:11px 14px;border-bottom:1px solid var(--line)}
.utable .k{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:1px;text-transform:uppercase;color:var(--amber);background:#0d141a}
.utable .v{font-family:"Fraunces",serif;color:var(--ink)}
.logicsteps{display:grid;gap:8px}
.lstep{display:grid;grid-template-columns:34px 1fr;gap:12px;border:1px solid var(--line);border-radius:9px;padding:11px 13px;background:var(--panel)}
.lstep .ln{font-family:"Fraunces",serif;font-size:22px;color:var(--blood);text-align:center}
.lstep .lt{font-family:"IBM Plex Mono",monospace;font-size:12px;letter-spacing:1px;text-transform:uppercase;color:var(--serif)}
.lstep .ld{font-size:13.5px;color:var(--dim);margin-top:2px}
.calc{border:1px solid var(--line);border-radius:12px;background:linear-gradient(180deg,#11181a,#0b1013);padding:18px;max-width:520px}
.calc input{width:120px;background:var(--abyss2);border:1px solid var(--line2);border-radius:7px;color:var(--ink);font-family:"IBM Plex Mono",monospace;font-size:15px;padding:8px 10px}
.calc .out{font-family:"Fraunces",serif;font-size:30px;color:var(--blood);margin:12px 0 2px}
.calc .who{font-size:13px;color:var(--dim);margin-top:8px;line-height:1.5}
.tl{border-left:2px solid var(--line2);margin-left:8px;padding-left:18px}
.tl .ev{position:relative;margin:0 0 14px;background:transparent;border:0;padding:0}
.tl .ev::before{content:"";position:absolute;left:-25px;top:5px;width:9px;height:9px;border-radius:50%;background:var(--amber)}
.tl .yr{font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--amber);letter-spacing:1px}
.tl .tx{color:var(--ink);font-size:14.5px}
.breakbox{border:1px solid #244a33;background:#0b160f;border-radius:12px;padding:18px;margin-top:8px}
.breakbox .q{font-family:"Fraunces",serif;font-style:italic;font-size:18px;color:var(--E1);margin-bottom:10px}
.breakbox li{color:#bfe0c6;margin:4px 0}
.gcredit{font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--faint);padding:24px 48px 0;line-height:1.6;border-top:1px solid var(--line);margin-top:30px}
.gcredit b{color:var(--signal)}
/* ConsMAP dual labels + StoneRiver + method */
.cmtag{font-family:"IBM Plex Mono",monospace;font-size:9.5px;letter-spacing:1px;text-transform:uppercase;color:var(--amber);border:1px solid #3f3318;border-radius:4px;padding:1px 6px;background:#14100a}
.cmtag.big{font-size:11px;padding:3px 10px;color:#0c0f12;background:var(--amber);border-color:var(--amber);font-weight:700;justify-self:start}
.tag.river-clean{color:var(--E1);border-color:#234a2f}
.tag.river-muddy{color:var(--RV);border-color:#3f2f12}
.tag.river-stone{color:var(--Q);border-color:#4a2626}
.tag.river-symbolic{color:var(--S);border-color:#33414a}
.tag.river-private{color:var(--A1);border-color:#234048}
.tag.river-rejected{color:var(--D1);border-color:#4a2626}
.mlist{display:flex;flex-direction:column;gap:6px;margin:6px 0 4px}
.mrow{display:grid;grid-template-columns:150px 1fr;gap:12px;align-items:start;border:1px solid var(--line);border-radius:8px;padding:9px 12px;background:var(--panel);font-size:14px;color:var(--ink)}
.hq{font-size:12.5px;color:var(--dim);margin-top:6px;line-height:1.5}
.hq b{color:var(--ink)}
/* reader nav + progress */
#progress{position:fixed;top:0;left:0;height:3px;background:linear-gradient(90deg,var(--signal),var(--amber));width:0;z-index:9998;transition:width .1s}
.cnav{display:flex;justify-content:space-between;gap:10px;margin:50px 0 0;padding-top:22px;border-top:1px solid var(--line)}
.cnav button{font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--ink);background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:11px 15px;cursor:pointer;max-width:46%;text-align:left;transition:.15s}
.cnav button:hover{border-color:var(--signal);color:var(--serif)}
.cnav button:disabled{opacity:.3;cursor:default}
.cnav .nx{text-align:right}
.evjump{display:inline-block;margin-top:10px;font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--A1);border:1px solid var(--line);border-radius:999px;padding:5px 12px;cursor:pointer}
.evjump:hover{border-color:var(--A1)}
/* descent intro */
#intro{position:fixed;inset:0;z-index:10000;background:radial-gradient(900px 500px at 50% 20%,#0e1922,#05080a 70%);display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:pointer;transition:opacity .8s}
#intro.gone{opacity:0;pointer-events:none}
#intro .ti{font-family:"Fraunces",serif;font-size:clamp(38px,7vw,82px);color:var(--serif);letter-spacing:-1px;opacity:0;animation:introIn 1.1s .15s ease both}
#intro .ti em{font-style:italic;color:var(--amber)}
#intro .ds{font-family:"IBM Plex Mono",monospace;font-size:12px;letter-spacing:5px;text-transform:uppercase;color:var(--signal);margin-top:14px;opacity:0;animation:introIn 1.1s .55s ease both}
#intro .hint{position:absolute;bottom:40px;font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--faint);opacity:0;animation:introIn 1s 1.4s ease both;letter-spacing:1px}
#intro .strata2{position:absolute;inset:0;background:repeating-linear-gradient(180deg,transparent 0 60px,rgba(87,202,189,.05) 60px 61px);animation:sink 6s linear infinite;opacity:.5}
@keyframes introIn{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
@keyframes sink{from{background-position-y:0}to{background-position-y:61px}}
/* hero atmosphere image */
.hero-bg{position:absolute;inset:0;z-index:0;background-size:cover;background-position:center;opacity:.18;filter:grayscale(.15) contrast(1.05)}
.hero-bg::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(7,11,14,.45),rgba(7,11,14,.93))}
.hero>*:not(.hero-bg){position:relative;z-index:1}
/* visions gallery + lightbox */
.visions{padding:46px 48px 90px}
.vgrid{columns:3 250px;column-gap:14px}
.vcard{break-inside:avoid;margin:0 0 14px;border:1px solid var(--line);border-radius:12px;overflow:hidden;cursor:zoom-in;position:relative;background:#0a0e12;transition:.18s}
.vcard:hover{border-color:var(--line2);transform:translateY(-2px)}
.vcard img{width:100%;display:block;filter:saturate(1.05) contrast(1.03)}
.vcard .cap{position:absolute;left:0;right:0;bottom:0;padding:22px 12px 9px;font-family:"Fraunces",serif;font-size:14px;color:#f1ecdf;background:linear-gradient(transparent,rgba(5,8,10,.88))}
.vcard .th{position:absolute;top:8px;left:8px;font-family:"IBM Plex Mono",monospace;font-size:9px;letter-spacing:1px;text-transform:uppercase;color:var(--signal);background:rgba(5,8,10,.65);border:1px solid var(--line);border-radius:4px;padding:2px 6px}
#lightbox{position:fixed;inset:0;z-index:10001;background:rgba(4,6,8,.96);display:none;align-items:center;justify-content:center;flex-direction:column;cursor:zoom-out;padding:30px}
#lightbox.on{display:flex}
#lightbox img{max-width:92vw;max-height:82vh;border:1px solid var(--line2);box-shadow:0 30px 90px rgba(0,0,0,.7);border-radius:6px}
#lightbox .lc{font-family:"Fraunces",serif;font-style:italic;color:var(--amber);margin-top:16px;font-size:18px}
/* iceberg descent (home) */
.icewrap{padding:14px 64px 30px}
.icehead{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:6px;flex-wrap:wrap;gap:8px}
.icehead .il{font-family:"Fraunces",serif;font-size:24px;color:var(--serif)}
.icehead .ir{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:1px;text-transform:uppercase;color:var(--faint)}
.waterline{position:relative;height:1px;background:linear-gradient(90deg,transparent,var(--signal),transparent);margin:10px 0 2px;opacity:.6}
.waterline span{position:absolute;right:0;top:-8px;font-family:"IBM Plex Mono",monospace;font-size:9px;letter-spacing:3px;color:var(--signal);opacity:.7}
.iceberg{display:flex;flex-direction:column;align-items:center;gap:5px;padding-top:6px;background:linear-gradient(180deg,rgba(87,202,189,.04),transparent 60%)}
.iceband{position:relative;display:flex;justify-content:space-between;align-items:center;gap:14px;border:1px solid var(--line);border-left:0;border-right:0;border-radius:7px;padding:11px 16px;cursor:pointer;color:#dfe7ec;text-align:left;overflow:hidden;transition:transform .16s,box-shadow .16s,filter .16s}
.iceband:hover{transform:scale(1.012);box-shadow:0 8px 26px rgba(0,0,0,.5);filter:brightness(1.18);border-color:var(--signal)}
.ib-l{display:flex;align-items:baseline;gap:11px;min-width:0;z-index:1}
.ib-rn{font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--amber);flex:none}
.ib-tt{font-family:"Fraunces",serif;font-size:16px;color:#eef3f6;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ib-r{display:flex;align-items:center;gap:12px;flex:none;z-index:1}
.ib-d{font-family:"IBM Plex Mono",monospace;font-size:10px;color:var(--signal);opacity:.85}
.ib-ev{font-family:"IBM Plex Mono",monospace;font-size:10.5px;color:#cdd6dc}
.ib-ev.faint{color:var(--faint);text-transform:uppercase;letter-spacing:1px;font-size:9px}
.ib-dot{width:8px;height:8px;border-radius:50%;box-shadow:0 0 7px currentColor}
.ib-fill{position:absolute;left:0;bottom:0;height:2px;width:var(--dens);background:linear-gradient(90deg,var(--signal),var(--amber));opacity:.55}
/* river filter chips on evidence ledger */
.riverlegend{margin-top:-4px}
.riverlab{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:1px;text-transform:uppercase;color:var(--faint);align-self:center;margin-right:4px}
.rchip{font-family:"IBM Plex Mono",monospace;font-size:10.5px;border:1px solid var(--line);border-radius:999px;padding:3px 10px;cursor:pointer;opacity:.42;background:#0a0e12;transition:.15s}
.rchip:hover{opacity:.8}
.rchip.on{opacity:1}
.rchip.river-clean.on{color:var(--E1);border-color:#234a2f;background:#0c160f}
.rchip.river-muddy.on{color:var(--RV);border-color:#3f2f12;background:#15110a}
.rchip.river-stone.on{color:var(--Q);border-color:#4a2626;background:#160c0c}
.rchip.river-symbolic.on{color:var(--S);border-color:#33414a;background:#0c1014}
.rchip.river-private.on{color:var(--A1);border-color:#234048;background:#0a1316}
.rchip.river-rejected.on{color:var(--D1);border-color:#4a2626;background:#160c0c}
/* network graph */
.netwrap{padding:46px 56px;max-width:1080px;margin:0 auto}
.netlegend{display:flex;flex-wrap:wrap;gap:14px;align-items:center;margin:8px 0 14px}
.nlk{font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--dim);display:inline-flex;align-items:center;gap:6px}
.nlk i{width:11px;height:11px;border-radius:50%;display:inline-block;border:1px solid #0b0f12}
.nclear{font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--amber);border:1px solid #3f3318;border-radius:999px;padding:3px 10px;cursor:pointer}
.netstage{border:1px solid var(--line);border-radius:14px;background:radial-gradient(900px 500px at 50% 0,#0c1620,#070b0e 75%);padding:8px;overflow:hidden}
.netsvg{width:100%;height:auto;display:block}
.nnode{transition:opacity .2s}
.nnode:hover circle{stroke:var(--amber);stroke-width:3}
.nnode.foc circle{stroke:var(--amber);stroke-width:3.5}
.nnlab{font-family:"IBM Plex Mono",monospace;font-size:12.5px;fill:#cfd8df;font-weight:600}
.nelab{font-family:"IBM Plex Mono",monospace;font-size:9.5px;letter-spacing:.3px}
.netnote{margin-top:16px}
.netfoc{border:1px solid var(--line);border-radius:12px;background:var(--panel);padding:14px 18px;margin-bottom:12px}
.nfh{font-family:"Fraunces",serif;font-size:20px;color:var(--serif);display:flex;align-items:center;gap:14px;margin-bottom:8px}
.netfoc ul{margin:0;padding-left:18px;color:var(--ink);font-size:14px;line-height:1.7}
/* saga lens */
.sgwrap{display:flex;flex-direction:column;gap:18px;margin:18px 0}
.sgcard{display:grid;grid-template-columns:78px 1fr;border:1px solid var(--line);border-radius:14px;background:var(--panel);overflow:hidden}
.sgrom{font-family:"Fraunces",serif;font-size:46px;color:#9a86c0;display:flex;align-items:center;justify-content:center;background:linear-gradient(160deg,#161226,#0c0a14);border-right:1px solid var(--line)}
.sgbody{padding:18px 22px}
.sgname{font-family:"Fraunces",serif;font-size:24px;color:var(--serif)}
.sgthesis{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:2px;text-transform:uppercase;color:#9a86c0;margin:4px 0 10px}
.sggloss{color:var(--dim);font-size:14.5px;line-height:1.65;margin:0 0 12px}
.sglocked{font-family:"Fraunces",serif;font-style:italic;font-size:17px;color:var(--amber);border-left:2px solid #9a86c0;padding-left:14px}
.sgmir{list-style:none;margin:6px 0 0;padding:0;display:flex;flex-direction:column;gap:6px}
.sgmir li{cursor:pointer;border:1px solid var(--line);border-radius:8px;padding:8px 12px;background:#0a0e12;transition:.15s}
.sgmir li:hover{border-color:#9a86c0;transform:translateX(3px)}
.mlink{color:var(--ink);font-size:13.5px}
.sgmir li:hover .mlink{color:var(--serif)}
/* bus cycle */
.busmovs{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:10px 0 4px}
.busmov{display:grid;grid-template-columns:42px 1fr;gap:12px;border:1px solid var(--line);border-radius:12px;background:var(--panel);padding:13px 16px}
.bmr{font-family:"Fraunces",serif;font-size:26px;color:var(--amber);text-align:center}
.bmn{font-family:"Fraunces",serif;font-size:17px;color:var(--serif)}
.bmg{color:var(--dim);font-size:13px;line-height:1.55;margin-top:3px}
.buslexwrap{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:8px 0}
.buslex{border:1px solid var(--line);border-radius:12px;background:#0a0e12;padding:14px 16px;cursor:pointer;transition:.15s}
.buslex:hover{border-color:#9a86c0;transform:translateY(-2px)}
.blt{font-family:"Fraunces",serif;font-size:18px;color:#c6b6e6}
.blg{color:var(--dim);font-size:13px;line-height:1.6;margin:6px 0 9px}
.blm{font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--amber)}
.contstage{cursor:pointer}
.cstop{display:flex;gap:13px;align-items:flex-start;margin-bottom:8px}
.cstn{font-family:"Fraunces",serif;font-size:32px;color:#57cabd;line-height:.9;flex:none}
.csmech{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:1.2px;text-transform:uppercase;color:var(--signal);margin-top:4px}
/* further panels (compact codex list) */
.furthergrid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:8px 0}
.fcard{border:1px solid var(--line);border-left:2px solid #9a86c0;border-radius:10px;background:#0a0e12;padding:11px 14px}
.fname{font-family:"Fraunces",serif;font-size:16px;color:#c6b6e6;margin-bottom:4px}
.fgloss{color:var(--dim);font-size:12.5px;line-height:1.55}
/* seal of authenticity */
.sealwrap{display:flex;flex-direction:column;align-items:center;gap:12px;margin:42px 0 8px;padding-top:30px;border-top:1px solid var(--line)}
.seal{width:min(280px,72vw);height:auto;filter:drop-shadow(0 0 30px rgba(154,48,48,.35));transition:transform .6s ease,filter .6s ease}
.seal:hover{transform:rotate(2deg) scale(1.03);filter:drop-shadow(0 0 44px rgba(200,164,77,.45))}
.sealcap{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:2px;text-transform:uppercase;color:var(--amber);text-align:center;line-height:1.9}
.sealcap span{color:var(--faint);font-size:9px;letter-spacing:1.5px}
/* register dial (Bus Cycle palette) */
.dialbar{margin:6px 0 16px;border:1px solid var(--line);border-radius:12px;background:linear-gradient(160deg,#16100f,#0c0a0b);padding:14px 16px}
.dialcap{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:1.4px;text-transform:uppercase;color:var(--faint);margin-bottom:10px;line-height:1.6}
.dialcap i{color:#c8a44d;font-style:italic;text-transform:none;letter-spacing:0;font-size:14px;font-family:"Fraunces",serif}
.dial3{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.dialseg{font-family:"IBM Plex Mono",monospace;font-size:11.5px;color:var(--dim);background:#0a0e12;border:1px solid var(--line);border-radius:999px;padding:9px 12px;cursor:pointer;transition:.16s;letter-spacing:.4px}
.dialseg:hover{border-color:#c8a44d;color:var(--ink)}
.dialseg.on{background:linear-gradient(90deg,#9a3030,#c8a44d);color:#0c0a0b;border-color:#c8a44d;font-weight:700}
/* register visibility (GLOBAL): mythos hides the plain-claim layer; logos hides the fable layer */
body[data-reg="mythos"] .sgmir,body[data-reg="mythos"] .logosonly,body[data-reg="mythos"] .blm{display:none}
body[data-reg="logos"] .sggloss,body[data-reg="logos"] .sglocked,body[data-reg="logos"] .busmovs,body[data-reg="logos"] .blg,body[data-reg="logos"] .mythosonly{display:none}
/* rail master dial */
.raildial{margin:12px 0 4px;border:1px solid var(--line);border-radius:10px;background:linear-gradient(160deg,#16100f,#0c0a0b);padding:10px 11px}
.rdcap{font-family:"IBM Plex Mono",monospace;font-size:9px;letter-spacing:1.6px;text-transform:uppercase;color:var(--faint);margin-bottom:7px;display:flex;justify-content:space-between;align-items:center}
.rdkeys{color:var(--signal);opacity:.6;letter-spacing:1px}
.raildial3{gap:5px}
.raildial3 .dialseg{font-size:10px;padding:6px 4px;letter-spacing:.3px;text-align:center}
.rdnote{font-family:"IBM Plex Mono",monospace;font-size:9.5px;color:var(--signal);opacity:.8;margin-top:7px;line-height:1.4;min-height:13px}
/* print button */
.printbtn{margin-top:14px;width:100%;font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--amber);background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:9px;cursor:pointer;letter-spacing:.5px;transition:.15s}
.printbtn:hover{border-color:var(--amber);color:var(--serif)}
/* iceberg clickable claims pill */
.ib-ev.clik{cursor:pointer;border:1px solid transparent;border-radius:999px;padding:2px 8px;transition:.14s}
.ib-ev.clik:hover{border-color:var(--amber);color:var(--amber)}
/* bicameral HUD */
.bclanes{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:12px 0 4px}
.bclane{border:1px solid var(--line);border-top:3px solid var(--lc);border-radius:12px;background:var(--panel);padding:14px 16px}
.bclane .bcln{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:1.5px;text-transform:uppercase;color:var(--lc);margin-bottom:6px}
.bclane p{color:var(--dim);font-size:13px;line-height:1.6;margin:0}
.bclights{display:flex;flex-direction:column;gap:8px;margin:6px 0}
.bclight{display:flex;gap:12px;align-items:center;border:1px solid var(--line);border-radius:10px;background:#0a0e12;padding:10px 14px}
.bclight .bcdot{font-size:18px}
.bclight b{display:block;color:var(--ink);font-size:14px;font-family:"Fraunces",serif}
.bclight span{color:var(--dim);font-size:12.5px}
.bcgrid{display:flex;flex-direction:column;gap:8px;margin-top:6px}
.bcrow{display:grid;grid-template-columns:46px 1fr;gap:10px;align-items:start;border:1px solid var(--line);border-left:3px solid var(--line);border-radius:10px;background:var(--panel);padding:12px 14px;cursor:pointer;transition:.15s}
.bcrow:hover{transform:translateX(3px);border-color:var(--line2)}
.bcrow.bc-green{border-left-color:var(--E1)}
.bcrow.bc-amber{border-left-color:var(--RV)}
.bcrow.bc-red{border-left-color:var(--Q)}
.bcsig{display:flex;justify-content:center;padding-top:2px}
.bcsig .bcdot{font-size:20px}
.bcrn{font-family:"Fraunces",serif;font-size:17px;color:var(--serif);display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.bctech{display:flex;flex-wrap:wrap;gap:5px;margin:7px 0}
.bctier{font-family:"IBM Plex Mono",monospace;font-size:10px;border:1px solid;border-radius:4px;padding:1px 6px;background:#0a0e12}
.bctier.faint{color:var(--faint);border-color:var(--line)}
.bchuman{color:var(--dim);font-size:13px;line-height:1.55}
/* convergence · one pattern, four lenses */
.pthreads{display:flex;flex-direction:column;gap:16px;margin:14px 0}
.pthread{border:1px solid var(--line);border-radius:14px;background:var(--panel);overflow:hidden}
.pthead{padding:15px 18px;border-bottom:1px solid var(--line);background:linear-gradient(120deg,#0e1620,#0b0f12)}
.ptn{display:block;font-family:"Fraunces",serif;font-size:21px;color:var(--serif)}
.ptspine{display:block;color:var(--dim);font-size:13.5px;font-style:italic;margin-top:3px}
.plenses{display:flex;flex-direction:column}
.plens{display:grid;grid-template-columns:104px 1fr 22px;gap:12px;align-items:center;padding:11px 18px;border-top:1px solid var(--line-soft,rgba(236,227,211,.05));position:relative}
.plens::before{content:"";position:absolute;left:0;top:0;bottom:0;width:3px;background:var(--lc)}
.plens.clik{cursor:pointer;transition:.15s}
.plens.clik:hover{background:#0c1218}
.plens.clik:hover .plgo{opacity:1;transform:translateX(2px)}
.plk{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:1.2px;text-transform:uppercase;color:var(--lc);font-weight:600}
.plbody{display:flex;flex-direction:column;gap:3px;min-width:0}
.pltag{font-family:"IBM Plex Mono",monospace;font-size:10px;color:var(--dim);letter-spacing:.5px}
.pltxt{color:var(--ink);font-size:13.5px;line-height:1.5}
.plgo{font-family:"IBM Plex Mono",monospace;color:var(--lc);opacity:.4;transition:.15s;text-align:center}
/* resurface · the ascent */
.surfhero{text-align:center;padding:10px 0 18px;border-bottom:1px solid var(--line);margin-bottom:18px;background:linear-gradient(0deg,rgba(87,202,189,.05),transparent)}
.surfarrow{font-size:40px;color:var(--signal);line-height:1;animation:bob 3.4s ease-in-out infinite}
@keyframes bob{0%,100%{transform:translateY(0);opacity:.85}50%{transform:translateY(-7px);opacity:1}}
.surfsub{font-family:"Fraunces",serif;font-style:italic;font-size:18px;color:var(--amber);margin:8px 0 0}
.surftools{display:grid;grid-template-columns:1fr;gap:14px;margin:14px 0}
.surftool{border:1px solid var(--line);border-radius:14px;background:var(--panel);padding:16px 18px}
.sth{display:flex;gap:14px;align-items:center;margin-bottom:12px}
.stnum{font-family:"Fraunces",serif;font-size:30px;color:var(--signal);opacity:.55;flex:none}
.stname{font-family:"Fraunces",serif;font-size:20px;color:var(--serif)}
.sttag{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:1.4px;text-transform:uppercase;color:var(--faint);margin-top:2px}
.surfsteps{display:flex;flex-direction:column;gap:6px}
.surfstep{display:grid;grid-template-columns:28px 1fr;gap:10px;align-items:start;color:var(--ink);font-size:14px;line-height:1.5;border:1px solid var(--line);border-radius:8px;padding:9px 12px;background:#0a0e12}
.surfstep .sn{font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--amber);text-align:center}
/* floating resurface button (deep views only) */
.resurface-fab{position:fixed;right:22px;bottom:22px;z-index:9997;display:none;align-items:center;gap:8px;font-family:"IBM Plex Mono",monospace;font-size:12px;letter-spacing:.5px;color:#0c0f12;background:linear-gradient(120deg,var(--signal),var(--amber));border:none;border-radius:999px;padding:12px 18px;cursor:pointer;box-shadow:0 10px 30px rgba(0,0,0,.55);opacity:0;transform:translateY(14px) scale(.96);transition:opacity .3s,transform .3s,box-shadow .2s}
.resurface-fab.show{display:flex;opacity:.94;transform:none;animation:fabbob 3.6s ease-in-out infinite}
.resurface-fab:hover{opacity:1;box-shadow:0 14px 40px rgba(87,202,189,.4)}
.resurface-fab span{font-weight:700}
@keyframes fabbob{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}
@media(max-width:880px){.resurface-fab span{display:none}.resurface-fab{padding:13px;right:16px;bottom:16px}}
.helpbtn{margin-top:8px;color:var(--signal)}
.helpbtn:hover{border-color:var(--signal);color:var(--serif)}
/* field guide overlay */
.helpmodal{position:fixed;inset:0;z-index:10002;background:rgba(4,6,8,.86);backdrop-filter:blur(3px);display:none;align-items:flex-start;justify-content:center;padding:5vh 16px;overflow:auto}
.helpmodal.on{display:flex;animation:fadein .25s ease}
@keyframes fadein{from{opacity:0}to{opacity:1}}
.helpcard{max-width:880px;width:100%;background:linear-gradient(170deg,#0e141a,#0a0e12);border:1px solid var(--line2);border-radius:16px;padding:24px 28px 28px;box-shadow:0 40px 100px rgba(0,0,0,.7)}
.hghead{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid var(--line);padding-bottom:12px;margin-bottom:6px}
.hghead h2{font-family:"Fraunces",serif;font-size:26px;color:var(--serif);margin:0}
.hgx{cursor:pointer;font-family:"IBM Plex Mono",monospace;color:var(--dim);font-size:18px;padding:2px 8px;border:1px solid var(--line);border-radius:8px}
.hgx:hover{border-color:var(--Q);color:var(--Q)}
.hgcols{display:grid;grid-template-columns:1fr 1fr;gap:8px 28px}
.hgrow{display:grid;grid-template-columns:96px 1fr;gap:10px;align-items:center;padding:5px 0;font-size:13px;color:var(--ink);border-bottom:1px solid var(--line-soft,rgba(236,227,211,.05))}
.hgrow kbd{font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--amber);background:#14100a;border:1px solid #3f3318;border-radius:5px;padding:2px 6px;text-align:center}
.hgrow .chip{justify-self:start}
.hgconcepts{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:4px}
.hgc{border:1px solid var(--line);border-radius:9px;background:#0a0e12;padding:9px 12px}
.hgc b{display:block;font-family:"Fraunces",serif;font-size:15px;color:var(--amber);margin-bottom:2px}
.hgc span{color:var(--dim);font-size:12.5px;line-height:1.5}
.hgcredit{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:1px;color:var(--faint);margin-top:14px;text-align:right}
@media(max-width:880px){.hgcols,.hgconcepts{grid-template-columns:1fr}}
@media(max-width:880px){.app{grid-template-columns:1fr}.rail{position:static;height:auto;border-right:0;border-bottom:1px solid var(--line)}.hero,.statgrid,.evwrap,.mapwrap,.netwrap,.icewrap{padding-left:24px;padding-right:24px}.reader{padding:30px 22px}.sgcard{grid-template-columns:1fr}.sgrom{padding:10px;border-right:0;border-bottom:1px solid var(--line)}.busmovs,.buslexwrap,.bclanes,.furthergrid{grid-template-columns:1fr}.plens{grid-template-columns:84px 1fr}.plgo{display:none}}
/* ===== print · read with the lights on (honours the active register) ===== */
@media print{
  @page{margin:1.7cm}
  html,body{background:#fff!important;color:#16110c!important}
  body::before,body::after{display:none!important}
  #intro,#progress,.rail,.printbtn,.cnav,.tabs,#netlegend,.hero-bg,.strata,.strata2,#lightbox,.resurface-fab,#help{display:none!important}
  .app{display:block}
  .main{display:block;overflow:visible}
  .view{display:none!important}
  .view.on{display:block!important}
  .prose,.evsub,.txt,.sggloss,.bmg,.blg,.netfoc ul,.dialcap,.foot{color:#2a221a!important}
  h1,h2,.ib-tt,.sgname,.bmn,.nfh,.evhead,.section-t,.lawline{color:#16110c!important}
  .lawline b,.sglocked,.ib-rn,.blm{color:#8a6a1e!important}
  .iceband{color:#16110c!important;border:1px solid #d8cdbb!important;background:#f5f1e8!important;width:100%!important}
  .ev,.sgcard,.buslex,.netfoc,.busmov,.stat,.dialbar,.breakbox,.warnbox{break-inside:avoid;border-color:#d8cdbb!important;background:#fbf8f1!important}
  .ev{box-shadow:none!important}
  .reader{max-width:none;padding:0}
  .prose a{color:#16110c!important;text-decoration:underline}
  .netsvg{filter:none}
  .dialbar{background:#faf6ee!important}
  .dialseg{display:none!important}
  .dialseg.on{display:inline-block!important;background:#fff!important;color:#8a6a1e!important;border-color:#8a6a1e!important}
}
"""

APPJS = r"""
const D = window.__ANON__;
const TIERS = ["E1","E2","E3","I1","I2","S","A1","R1","D1","U1","Q","RV","META"];
const TIERMEAN = {E1:"primary/official",E2:"reputable secondary",E3:"caveated",I1:"pattern inference",
 I2:"speculative",S:"symbolic",A1:"anomaly/suppression",R1:"rumor",D1:"disinfo/false",U1:"underreported",
 Q:"quarantine",RV:"remove-until-verified",META:"structural"};
const cssVar = t => getComputedStyle(document.documentElement).getPropertyValue('--'+t)||'#888';

let activeTab="home", activeChapter=0, tierFilter=new Set(), riverFilter=new Set(), chFilter="ALL", netFocus=null, register="both";
function setRegister(r){register=r;document.body.dataset.reg=r;document.querySelectorAll('.dialseg').forEach(s=>s.classList.toggle('on',s.dataset.reg===r));const rn=document.getElementById('rdnote');if(rn)rn.textContent=({mythos:'the fable — symbol foregrounded',both:'both — side by side',logos:'plain claim — sourced only'})[r]||'';}
function doPrint(){document.body.dataset.printview=activeTab;window.print();}
const RIVERMEAN={clean:"PUBLIC_READY — primary/official, source-locked",muddy:"pending source-lock or underreported",stone:"quarantined — route, do not destroy",symbolic:"S / METAPHOR — inspires imagery, proves nothing",private:"private archive only",rejected:"disinfo / firewalled (e.g. identity-as-causation)"};

function el(tag,cls,html){const e=document.createElement(tag);if(cls)e.className=cls;if(html!=null)e.innerHTML=html;return e;}

/* ---- nav ---- */
function buildNav(){
  const list=document.getElementById('navlist'); list.innerHTML="";
  D.chapters.forEach((c,i)=>{
    const b=el('button','navitem'+(i===activeChapter&&activeTab==='read'?' on':''));
    b.innerHTML=`<span class="rn">${c.roman}</span><span class="tt">${c.title}</span>
      <span class="st ${c.status}">${c.status}</span>
      <div class="depthbar" style="width:${20+c.depth*7}%;opacity:${.25+c.depth*0.06}"></div>`;
    b.onclick=()=>{activeChapter=i;go('read');};
    list.appendChild(b);
  });
}

/* ---- reader ---- */
function renderReader(){
  const c=D.chapters[activeChapter];
  const r=document.getElementById('reader');
  let banner="";
  if(c.status==="sealed") banner=`<div class="banner sealed">🔒 SEALED · high-risk draft · not source-locked · contains quarantine-flagged material (hacktivist sign-offs, intent attributions). Author working draft — not for publication.</div>`;
  else if(c.status==="draft") banner=`<div class="banner">⚠ DRAFT · not yet source-locked · symbolic/speculative material present (S/I2 register).</div>`;
  else if(c.status==="bridge") banner=`<div class="banner bridge">⟡ INTERLUDE · I1 bridge (inference, not allegation). Row markers resolve to the CH5 & KAIROS apparatuses.</div>`;
  else if(c.status==="verified") banner=`<div class="banner" style="border-left-color:var(--E1);background:#0c160f;color:var(--E1)">✓ VERIFIED SPINE · source-lock apparatus complete.</div>`;
  const evcode = {"1_SURFACE_PLASTIC.md":"CH1","2_SHALLOW_CORRUPTION.md":"CH2","3_DARPA_INFRASTRUCTURE.md":"CH3","4_FULL_EXTRACTION.md":"CH4","5_BIG_TECH_SABOTAGE.md":"CH5"}[c.file];
  let evbtn="";
  if(evcode){ const nev=D.evidence.filter(e=>e.ch===evcode).length;
    evbtn=`<span class="evjump" onclick="gotoEvidenceCh('${evcode}')">▤ ${evcode} evidence · ${nev} claims</span>`; }
  const prev=D.chapters[activeChapter-1], next=D.chapters[activeChapter+1];
  const cnav=`<div class="cnav">
    <button ${prev?'':'disabled'} onclick="jumpCh(-1)">${prev?'← '+prev.roman+' · '+prev.title:'—'}</button>
    <button class="nx" ${next?'':'disabled'} onclick="jumpCh(1)">${next?next.roman+' · '+next.title+' →':'—'}</button></div>`;
  r.innerHTML=`<div class="reader"><div class="chead"><div class="rn">CHAPTER ${c.roman} · DEPTH ${c.depth} · ${c.words.toLocaleString()} words</div>
    <h2>${c.title}</h2><span class="badge ${c.status}">${c.status}</span>${evbtn}${banner}</div>
    <div class="prose">${c.html}</div>${cnav}</div>`;
  r.parentElement.scrollTop=0; document.querySelector('.main').scrollTop=0; window.scrollTo(0,0);
  buildNav();
}
function jumpCh(d){const n=activeChapter+d; if(n>=0&&n<D.chapters.length){activeChapter=n;renderReader();window.scrollTo(0,0);}}

/* ---- evidence ---- */
function buildLegend(){
  const lg=document.getElementById('legend'); lg.innerHTML="";
  TIERS.forEach(t=>{
    const present=D.evidence.some(e=>e.label===t);
    if(!present) return;
    const c=el('span','chip'+(tierFilter.size===0||tierFilter.has(t)?' on':''));
    c.textContent=t; c.title=TIERMEAN[t]||t; c.style.background=cssVar(t);
    c.onclick=()=>{ if(tierFilter.has(t))tierFilter.delete(t); else tierFilter.add(t); buildLegend(); renderEvidence(); };
    lg.appendChild(c);
  });
}
function buildRiverFilter(){
  const lg=document.getElementById('riverlegend'); lg.innerHTML="";
  const order=["clean","muddy","stone","symbolic","private","rejected"];
  const present=order.filter(r=>D.evidence.some(e=>e.river===r));
  if(!present.length) return;
  const lab=el('span','riverlab'); lab.textContent="StoneRiver:"; lg.appendChild(lab);
  present.forEach(r=>{
    const c=el('span','rchip river-'+r+(riverFilter.size===0||riverFilter.has(r)?' on':''));
    c.textContent='~ '+r; c.title=RIVERMEAN[r]||r;
    c.onclick=()=>{ if(riverFilter.has(r))riverFilter.delete(r); else riverFilter.add(r); buildRiverFilter(); renderEvidence(); };
    lg.appendChild(c);
  });
}
function buildChFilters(){
  const f=document.getElementById('chfilters'); f.innerHTML="";
  const chs=["ALL",...Array.from(new Set(D.evidence.map(e=>e.ch)))];
  chs.forEach(ch=>{
    const b=el('span','tab'+(chFilter===ch?' on':'')); b.textContent=ch;
    b.onclick=()=>{chFilter=ch;buildChFilters();renderEvidence();}; f.appendChild(b);
  });
}
function renderEvidence(){
  const q=(document.getElementById('evsearch').value||"").toLowerCase();
  const grid=document.getElementById('evgrid'); grid.innerHTML="";
  let rows=D.evidence.filter(e=>{
    if(chFilter!=="ALL"&&e.ch!==chFilter) return false;
    if(tierFilter.size&&!tierFilter.has(e.label)) return false;
    if(riverFilter.size&&!riverFilter.has(e.river)) return false;
    if(q&&!(e.text.toLowerCase().includes(q)||e.id.toLowerCase().includes(q))) return false;
    return true;
  });
  document.getElementById('evcount').textContent=rows.length+" / "+D.evidence.length+" labelled claims";
  rows.forEach(e=>{
    const card=el('div','ev');
    const col=cssVar(e.label);
    card.style.borderTop="2px solid "+col;
    const sig=e.sig?`<span class="tag" style="color:${cssVar(e.sig)}">${e.sig}</span>`:"";
    card.innerHTML=`<div class="top">
        <span class="chip on" style="background:${col};cursor:default" title="ANON tier">${e.label}</span>
        <span class="cmtag" title="ConsMAP epistemic label">${e.cm||""}</span>
        <span class="id">${e.id} · ${e.ch}</span></div>
      <div class="txt">${escapeHtml(e.text)}</div>
      <div class="foot"><span class="tag river-${e.river}" title="StoneRiver route">~ ${e.river||"—"}</span>
        <span class="tag">${e.disp||"—"}</span>${sig}
        <span class="tag risk-${e.risk}">${e.risk||"—"}</span></div>`;
    grid.appendChild(card);
  });
}
function escapeHtml(s){return s.replace(/[&<>]/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[m]));}

/* ---- GHOSTCORE: native render of Zala's portal ---- */
function gotoChapterRoman(rn){const i=D.chapters.findIndex(c=>c.roman===rn);if(i>=0){activeChapter=i;go('read');}}
function gotoEvidenceCh(code){go('evidence');chFilter=code;buildChFilters();renderEvidence();}
function renderGhost(){
  const g=D.ghost, host=document.getElementById('ghost-native'); if(!host||host.dataset.done) return;
  const ghbg = D.ghero?`background-image:linear-gradient(180deg,rgba(7,11,14,.62),rgba(7,11,14,.95)),url('${D.ghero}');background-size:cover;background-position:center;`:'';
  let h=`<div class="ghero" style="${ghbg}"><div class="strata2" style="position:absolute;inset:0;opacity:.4;background:repeating-linear-gradient(180deg,transparent 0 54px,rgba(87,202,189,.05) 54px 55px)"></div>
    <div class="sigil">\u{1F702}</div><h2>GHOSTCORE</h2>
    <div class="tag">"${g.tagline}"</div><div class="sub">${g.subtitle}</div>
    <div class="gevo">${["Physical","Network","Digital","Material"].map(x=>`<span>${x}</span>`).join('')}</div></div>`;
  // domains
  h+=`<div class="gdoms">`;
  g.domains.forEach(d=>{
    const jumps = d.ch
      ? `<span class="jb" onclick="gotoChapterRoman('${d.ch}')">↳ Read CH ${d.ch}</span><span class="jb" onclick="gotoEvidenceCh('${d.ev}')">▤ ${d.ev} evidence</span>`
      : `<span class="jb locked">pattern origin · pre-corpus</span>`;
    h+=`<div class="gdom" style="--accent:${d.accent}">
      <div class="dh"><span class="ic">${d.icon}</span><div><div class="nm">${d.name}</div><div class="era">${d.era}</div></div></div>
      <div class="lead">${d.lead}</div>
      <div class="sect">The numbers</div><ul>${d.numbers.map(n=>`<li>${escapeHtml(n)}</li>`).join('')}</ul>
      <div class="sect">The cost</div><ul>${d.cost.map(n=>`<li>${escapeHtml(n)}</li>`).join('')}</ul>
      <div class="gnote">${escapeHtml(d.note)}</div>
      <div class="jump">${jumps}</div></div>`;
  });
  h+=`</div>`;
  // unified pattern
  h+=`<div class="gblock"><h3>The Unified Pattern</h3><div class="utable">`;
  g.unified.forEach(r=>{h+=`<div class="k">${r[0]}</div><div class="v">${r[1]}</div>`;});
  h+=`</div>`;
  // 7-step logic
  h+=`<h3>The 7-Step Extraction Logic</h3><div class="logicsteps">`;
  g.logic.forEach((s,i)=>{h+=`<div class="lstep"><div class="ln">${i+1}</div><div><div class="lt">${s[0]}</div><div class="ld">${escapeHtml(s[1])}</div></div></div>`;});
  h+=`</div>`;
  // calculator
  h+=`<h3>The True-Cost Calculator</h3><div class="calc">
    <div style="font-size:13px;color:var(--dim);margin-bottom:8px">Enter a plastic product price — see the hidden societal cost (3:1 externalization).</div>
    $ <input id="cprice" type="number" value="1" min="0" step="0.5" oninput="calcCost()">
    <div class="out" id="cout">$3.00</div>
    <div class="who">Who pays the other $2.00? Health systems · environment · future generations.<br>Producer pays: <b id="cprod">$1.00</b></div></div>`;
  // recycling timeline
  h+=`<h3>The Recycling Lie · 50 Years</h3><div class="tl">`;
  g.recycling.forEach(r=>{h+=`<div class="ev"><span class="yr">${r[0]}</span><div class="tx">${escapeHtml(r[1])}</div></div>`;});
  h+=`</div>`;
  // break the logic
  h+=`<h3>How to Break the Logic</h3><div class="breakbox"><div class="q">"${escapeHtml(g.break_quote)}"</div><ul>${g.break_steps.map(s=>`<li>${escapeHtml(s)}</li>`).join('')}</ul></div></div>`;
  // credit
  h+=`<div class="gcredit">\u{1F702} <b>${escapeHtml(g.credit)}</b></div>`;
  host.innerHTML=h; host.dataset.done="1"; calcCost();
}
function calcCost(){
  const r=(D.ghost&&D.ghost.calc_ratio)||3;
  const p=parseFloat((document.getElementById('cprice')||{}).value)||0;
  const t=(p*r).toFixed(2);
  const o=document.getElementById('cout'); if(o)o.textContent='$'+t;
  const pr=document.getElementById('cprod'); if(pr)pr.textContent='$'+p.toFixed(2);
}
function setGhostMode(mode){
  const fr=document.getElementById('ghostframe'), nat=document.getElementById('ghost-native');
  document.querySelectorAll('.gtoggle .tab').forEach(b=>b.classList.remove('on'));
  [...document.querySelectorAll('.gtoggle .tab')].find(b=>b.textContent.toLowerCase().includes(mode==='native'?'native':mode))?.classList.add('on');
  if(mode==='native'){fr.classList.remove('on');nat.style.display='block';}
  else{const src=fr.getAttribute('data-'+mode); if(src){fr.src=fr.src||src; if(!fr.src)fr.src=src; fr.src=src;} nat.style.display='none'; fr.classList.add('on');}
}

/* ---- tabs ---- */
function go(tab){
  activeTab=tab;
  document.querySelectorAll('.tab').forEach(t=>t.classList.toggle('on',t.dataset.tab===tab||(tab==='read'&&t.dataset.tab==='read')));
  document.querySelectorAll('.view').forEach(v=>v.classList.remove('on'));
  document.getElementById('view-'+(tab==='read'?'read':tab)).classList.add('on');
  if(tab==='read') renderReader();
  if(tab==='evidence'){buildChFilters();buildLegend();buildRiverFilter();renderEvidence();}
  if(tab==='ghost') renderGhost();
  if(tab==='visions') renderVisions();
  if(tab==='method') renderMethod();
  if(tab==='network') renderNetwork();
  if(tab==='saga') renderSaga();
  if(tab==='bicam') renderBicameral();
  if(tab==='pattern') renderPattern();
  if(tab==='surface') renderSurface();
  const DEEP=new Set(['read','evidence','map','pattern','network','method','bicam','saga']);
  const fab=document.getElementById('resurface-fab'); if(fab) fab.classList.toggle('show',DEEP.has(tab));
  buildNav();
  window.scrollTo(0,0);
}

/* ---- Visions gallery + lightbox ---- */
function renderVisions(){
  const grid=document.getElementById('vgrid'); if(!grid||grid.dataset.done) return;
  if(!D.art||!D.art.length){grid.innerHTML='<p class="evsub">No art bundled.</p>';return;}
  grid.innerHTML=D.art.map(a=>`<div class="vcard" onclick="openLB('${a.file}','${escapeHtml(a.title).replace(/'/g,"")}')">
     <span class="th">${a.theme}</span><img src="${a.file}" alt="${escapeHtml(a.title)}" loading="lazy">
     <div class="cap">${escapeHtml(a.title)}</div></div>`).join('');
  grid.dataset.done="1";
}
function openLB(file,cap){const lb=document.getElementById('lightbox');document.getElementById('lbimg').src=file;document.getElementById('lbcap').textContent=cap;lb.classList.add('on');}
(function(){const lb=document.getElementById('lightbox'); if(lb) lb.addEventListener('click',()=>lb.classList.remove('on'));})();

/* ---- Method view: ConsMAP harmonization ---- */
function renderMethod(){
  const m=D.consmap, host=document.getElementById('methodwrap'); if(!host||!m||host.dataset.done)return;
  const lbl=m.labels.map(l=>`<div class="mrow"><span class="cmtag big">${l[0]}</span><span>${escapeHtml(l[1])}</span></div>`).join('');
  const riv=m.rivers.map(r=>`<div class="mrow"><span class="tag river-${r[0]}">~ ${r[0]}</span><span>${escapeHtml(r[1])}</span></div>`).join('');
  const hyg=m.hygiene.map((q,i)=>`<div class="lstep"><div class="ln">${i+1}</div><div><div class="ld">${escapeHtml(q)}</div></div></div>`).join('');
  const tttp=m.ttt.patterns.map(p=>`<div class="mrow"><span class="tag" style="color:var(--I1);border-color:#4a3f1d">${p[0]}</span><span><b>${escapeHtml(p[1])}</b> — ${escapeHtml(p[2])}</span></div>`).join('');
  const cw=m.crosswalk.map(r=>`<div class="utable" style="margin-bottom:6px"><div class="k">${r[0]}</div><div class="v">${r[1]}</div></div>`).join('');
  const ex=(D.hygiene||[]).map(h=>`<div class="ev"><div class="top"><span class="cmtag">${escapeHtml(h.type)}</span><span class="id">${h.id}</span></div>
     <div class="txt">"${escapeHtml(h.claim)}"</div>
     <div class="hq"><b>Source</b> · ${escapeHtml(h.source)}</div>
     <div class="hq"><b>What would disprove it</b> · ${escapeHtml(h.disprove)}</div>
     <div class="hq"><b>Risk</b> · ${escapeHtml(h.risk)}</div></div>`).join('');
  host.innerHTML=`
    <h2 class="evhead">Method · ConsMAP × ANON</h2>
    <p class="evsub"><b style="color:var(--amber)">"${escapeHtml(m.core_rule)}"</b> — ${escapeHtml(m.intro)}</p>
    <div class="section-t">Epistemic labels</div><div class="mlist">${lbl}</div>
    <div class="section-t">StoneRiver — routing, not a truth oracle</div><div class="mlist">${riv}</div>
    <div class="section-t">Claim Hygiene · five questions before routing</div><div class="logicsteps">${hyg}</div>
    <div class="section-t">Worked claim cards · with falsification</div><div class="evgrid">${ex}</div>
    <div class="section-t">TTT · structural-mismatch detection</div>
    <div class="breakbox"><div class="q">${escapeHtml(m.ttt.formula)}</div>
      <div style="color:var(--dim);margin-bottom:10px">${escapeHtml(m.ttt.one_line)}</div>
      <div class="mlist">${tttp}</div>
      <div class="hq" style="margin-top:12px;color:var(--I1)">${escapeHtml(m.kairos_ttt)}</div></div>
    <div class="section-t">Label crosswalk · ANON → ConsMAP</div><div>${cw}</div>
    <div class="warnbox"><h3>Sanctuary Reasoning Threshold</h3><p style="color:#d9c2bf;margin:0">${escapeHtml(m.sanctuary)}</p></div>`;
  host.dataset.done="1";
}

/* ---- Iceberg descent (Home) ---- */
function openCh(i){activeChapter=i;go('read');}
function renderIceberg(){
  const host=document.getElementById('iceberg'); if(!host||host.dataset.done)return;
  const evmap={"1_SURFACE_PLASTIC.md":"CH1","2_SHALLOW_CORRUPTION.md":"CH2","3_DARPA_INFRASTRUCTURE.md":"CH3","4_FULL_EXTRACTION.md":"CH4","5_BIG_TECH_SABOTAGE.md":"CH5"};
  const chs=D.chapters.slice().sort((a,b)=>(a.depth||0)-(b.depth||0));
  const evc=c=>{const cd=evmap[c.file];return cd?D.evidence.filter(e=>e.ch===cd).length:0;};
  const maxev=Math.max(1,...chs.map(evc));
  const n=chs.length;
  host.innerHTML=chs.map((c,i)=>{
    const f=n>1?i/(n-1):0;
    const w=(97-f*52).toFixed(1);
    const L=(21-f*15).toFixed(1);
    const cd=evmap[c.file], nev=evc(c), dens=Math.round(nev/maxev*100);
    const idx=D.chapters.indexOf(c);
    const dot=c.status==='verified'?'var(--E1)':c.status==='sealed'?'var(--Q)':c.status==='bridge'?'var(--A1)':'var(--RV)';
    return `<button class="iceband" style="width:${w}%;background:linear-gradient(100deg,hsl(196 32% ${L}%),hsl(212 38% ${(L-5).toFixed(1)}%));--dens:${dens}%" onclick="openCh(${idx})" title="${escapeHtml(c.title)} · read the chapter">
      <span class="ib-l"><span class="ib-rn">${c.roman}</span><span class="ib-tt">${escapeHtml(c.title)}</span></span>
      <span class="ib-r"><span class="ib-d">▾ ${c.depth}</span>${cd?`<span class="ib-ev clik" onclick="event.stopPropagation();gotoEvidenceCh('${cd}')" title="filter the ledger to ${cd}">${nev} claims ▤</span>`:`<span class="ib-ev faint">${c.status}</span>`}<span class="ib-dot" style="background:${dot}"></span></span>
      <span class="ib-fill"></span></button>`;
  }).join('');
  host.dataset.done="1";
}

/* ---- Network graph: documented funding / role nodes ---- */
const NETSEARCH={wexner:"Wexner",epstein:"Epstein",barak:"Barak",thiel:"Thiel",petraeus:"Petraeus",miller:"Miller",jpmorgan:"JPMorgan",deutsche:"Deutsche",att:"AT&T",valar:"Valar",foundersfund:"Founders Fund",inqtel:"In-Q-Tel",carbyne:"Carbyne",palantir:"Palantir",unit8200:"8200",mit:"MIT"};
const NETKIND={hub:'#e0b341',person:'#9fb2c4',money:'#c98a4b',bank:'#c98a4b',org:'#7f8a99',vc:'#57cabd',intel:'#cf6b6b',infra:'#8fb98f',acad:'#9a86c0'};
function netClick(id){ netFocus=(id===netFocus)?null:id; renderNetwork(); }
function netEvJump(term){go('evidence');chFilter="ALL";tierFilter.clear();riverFilter.clear();buildChFilters();buildLegend();buildRiverFilter();document.getElementById('evsearch').value=term;renderEvidence();}
function renderNetwork(){
  const N=D.net, host=document.getElementById('netstage'); if(!N||!host) return;
  const pos={}; N.nodes.forEach(n=>pos[n[0]]={label:n[1],kind:n[2],x:n[3],y:n[4]});
  const con=new Set();
  if(netFocus){con.add(netFocus); N.edges.forEach(e=>{ if(e[0]===netFocus)con.add(e[1]); if(e[1]===netFocus)con.add(e[0]); });}
  const nodeOn=id=>!netFocus||con.has(id);
  const edgeOn=e=>!netFocus||e[0]===netFocus||e[1]===netFocus;
  let svg=`<svg viewBox="0 0 1000 660" class="netsvg" preserveAspectRatio="xMidYMid meet">`;
  N.edges.forEach(e=>{
    const a=pos[e[0]],b=pos[e[1]]; if(!a||!b)return;
    const col=(cssVar(e[3])||'#888').trim()||'#888', on=edgeOn(e);
    const mx=(a.x+b.x)/2, my=(a.y+b.y)/2;
    svg+=`<line x1="${a.x}" y1="${a.y}" x2="${b.x}" y2="${b.y}" stroke="${col}" stroke-width="${on?2.2:1}" opacity="${on?.8:.07}"/>`;
    if(on) svg+=`<text x="${mx}" y="${my-3}" class="nelab" fill="${col}" text-anchor="middle">${e[2]} · ${e[3]}</text>`;
  });
  N.nodes.forEach(n=>{
    const id=n[0],x=n[3],y=n[4],k=n[2], on=nodeOn(id), r=(k==='hub')?34:(k==='infra'?26:21);
    svg+=`<g class="nnode${id===netFocus?' foc':''}" opacity="${on?1:.16}" onclick="netClick('${id}')">
      <circle cx="${x}" cy="${y}" r="${r}" fill="${NETKIND[k]||'#888'}" stroke="#0b0f12" stroke-width="2"/>
      <text x="${x}" y="${y+r+14}" class="nnlab" text-anchor="middle">${pos[id].label}</text></g>`;
  });
  svg+=`</svg>`;
  host.innerHTML=svg;
  const kinds=[['money / bank','#c98a4b'],['person','#9fb2c4'],['venture','#57cabd'],['intel / agency','#cf6b6b'],['infrastructure','#8fb98f'],['academia','#9a86c0'],['Epstein · hub','#e0b341']];
  document.getElementById('netlegend').innerHTML=kinds.map(k=>`<span class="nlk"><i style="background:${k[1]}"></i>${k[0]}</span>`).join('')+(netFocus?` <span class="nclear" onclick="netClick(null)">✕ clear focus</span>`:'');
  const note=document.getElementById('netnote');
  if(netFocus){
    const n=pos[netFocus];
    const ties=N.edges.filter(e=>e[0]===netFocus||e[1]===netFocus).map(e=>{const o=e[0]===netFocus?e[1]:e[0];return `<li><b>${pos[o].label}</b> — ${e[2]} <span class="cmtag">${e[3]}</span></li>`;}).join('');
    note.innerHTML=`<div class="netfoc"><div class="nfh">${n.label}<span class="jb" onclick="netEvJump('${NETSEARCH[netFocus]||n.label}')">▤ open in ledger</span></div><ul>${ties}</ul></div><p class="evsub">${N.note}</p>`;
  } else note.innerHTML=`<p class="evsub">${N.note}</p>`;
}

/* ---- Saga lens: the Factory Trilogy as parable layer (S) ---- */
function sagaJump(t){
  if(t==='ghost'){go('ghost');return;}
  if(t==='method'){go('method');return;}
  if(t==='read'){const i=D.chapters.findIndex(c=>c.status==='bridge'); activeChapter=i>=0?i:0; go('read'); return;}
  if(/^CH\d$/.test(t)){go('evidence');chFilter=t;tierFilter.clear();riverFilter.clear();buildChFilters();buildLegend();buildRiverFilter();document.getElementById('evsearch').value="";renderEvidence();return;}
  go('read');
}
function renderSaga(){
  const s=D.saga, host=document.getElementById('sagawrap'); if(!s||!host||host.dataset.done) return;
  const cards=s.covenants.map(c=>{
    const mir=c.mirrors.map(m=>`<li onclick="sagaJump('${m[1]}')"><span class="mlink">${escapeHtml(m[0])}</span></li>`).join('');
    return `<div class="sgcard">
      <div class="sgrom">${c.roman}</div>
      <div class="sgbody">
        <div class="sgname">${escapeHtml(c.name)}</div>
        <div class="sgthesis">${escapeHtml(c.thesis)}</div>
        <p class="sggloss">${escapeHtml(c.gloss)}</p>
        <div class="sglocked">“${escapeHtml(c.locked)}”</div>
        <div class="section-t logosonly" style="margin-top:14px">Mirrors in the record</div>
        <ul class="sgmir">${mir}</ul>
      </div></div>`;
  }).join('');
  let busHtml="";
  const b=D.bus;
  if(b){
    const mv=b.movements.map(m=>`<div class="busmov"><span class="bmr">${m[0]}</span><div><div class="bmn">${escapeHtml(m[1])}</div><div class="bmg">${escapeHtml(m[2])}</div></div></div>`).join('');
    const lx=b.lexicon.map(l=>`<div class="buslex" onclick="sagaJump('${l[3]}')">
        <div class="blt">${escapeHtml(l[0])}</div>
        <div class="blg">${escapeHtml(l[1])}</div>
        <div class="blm">↳ ${escapeHtml(l[2])}</div></div>`).join('');
    busHtml=`
      <div class="section-t" style="margin-top:40px">A fourth panel · same pattern, satirical register</div>
      <h2 class="evhead" style="margin-top:4px">${escapeHtml(b.title)} <span class="cmtag big" style="vertical-align:middle">S · SATIRE</span></h2>
      <p class="evsub">${escapeHtml(b.sub)}</p>
      <div class="busmovs">${mv}</div>
      <div class="section-t logosonly">Lexicon · click a term to follow it into the record</div>
      <div class="buslexwrap">${lx}</div>
      ${(b.further&&b.further.length)?`
      <div class="section-t">The further panels · the full GrandBus codex</div>
      <p class="evsub">${escapeHtml(b.further_note||"")}</p>
      <div class="furthergrid">${b.further.map(f=>`<div class="fcard"><div class="fname">${escapeHtml(f[0])}</div><div class="fgloss">${escapeHtml(f[1])}</div></div>`).join('')}</div>`:''}
      <div class="breakbox"><div class="q">${escapeHtml(b.seal)}</div></div>
      <div class="warnbox" style="border-left-color:#9a86c0"><p style="color:#d9c2bf;margin:0">${escapeHtml(b.guard)}</p></div>`;
  }
  let contHtml="";
  const ct=D.continuum;
  if(ct){
    const st=ct.stages.map(s=>`<div class="buslex contstage" onclick="sagaJump('${s[4]}')">
        <div class="cstop"><span class="cstn">${s[0]}</span><div><div class="blt">${escapeHtml(s[1])}</div><div class="csmech">${escapeHtml(s[2])}</div></div></div>
        <div class="blg">${escapeHtml(s[3])}</div></div>`).join('');
    contHtml=`
      <div class="section-t" style="margin-top:40px">A third panel · the ladder beneath the parables</div>
      <h2 class="evhead" style="margin-top:4px">${escapeHtml(ct.title)} <span class="cmtag big" style="vertical-align:middle">S · STRUCTURAL</span></h2>
      <p class="evsub">${escapeHtml(ct.sub)}</p>
      <div class="breakbox" style="border-left-color:#57cabd"><div class="q" style="font-size:19px">${escapeHtml(ct.principle)}</div></div>
      <div class="buslexwrap">${st}</div>
      <div class="breakbox"><div class="q">${escapeHtml(ct.seal)}</div></div>
      <p class="evsub" style="margin-top:8px;color:var(--dim)">${escapeHtml(ct.terminal)}</p>
      <div class="warnbox" style="border-left-color:#9a86c0"><p style="color:#d9c2bf;margin:0">${escapeHtml(ct.guard)}</p></div>`;
  }
  let omniaHtml="";
  const om=D.omnia;
  if(om){
    const st=om.steps.map(s=>`<div class="buslex contstage"><div class="cstop"><span class="cstn" style="color:#9a86c0">${s[0]}</span><div><div class="blt">${escapeHtml(s[1])}</div></div></div><div class="blg">${escapeHtml(s[2])}</div></div>`).join('');
    omniaHtml=`
      <div class="section-t" style="margin-top:40px">The deepest ring · the same pattern across history</div>
      <h2 class="evhead" style="margin-top:4px">${escapeHtml(om.title)} <span class="cmtag big" style="vertical-align:middle">S · STRUCTURAL</span></h2>
      <p class="evsub">${escapeHtml(om.sub)}</p>
      <div class="buslexwrap">${st}</div>
      <div class="breakbox" style="border-left-color:#9a86c0"><div class="q">${escapeHtml(om.locked)}</div></div>
      <p class="evsub" style="margin-top:6px"><b style="color:var(--amber)">Why it is not a conspiracy:</b> ${escapeHtml(om.thermo)}</p>
      <p class="evsub" style="margin-top:6px">${escapeHtml(om.gravity)}</p>
      <div class="warnbox" style="border-left-color:#9a86c0"><p style="color:#d9c2bf;margin:0">${escapeHtml(om.guard)}</p></div>`;
  }
  host.innerHTML=`
    <h2 class="evhead">${escapeHtml(s.title)} <span class="cmtag big" style="vertical-align:middle">S · METAPHOR</span></h2>
    <p class="evsub">${escapeHtml(s.epigraph)}</p>
    <div class="dialbar">
      <div class="dialcap">The Register Dial · <i>Solve ⟶ Coagula</i> — same cycle, your door. None of the half-halfs are wrong; they just need a different one.</div>
      <div class="dial3">
        <button class="dialseg${register==='mythos'?' on':''}" data-reg="mythos" onclick="setRegister('mythos')">Mythos · the fable</button>
        <button class="dialseg${register==='both'?' on':''}" data-reg="both" onclick="setRegister('both')">Both · side by side</button>
        <button class="dialseg${register==='logos'?' on':''}" data-reg="logos" onclick="setRegister('logos')">Logos · plain claim</button>
      </div>
    </div>
    <div class="warnbox" style="border-left-color:#9a86c0"><h3>Parable layer</h3><p style="color:#d9c2bf;margin:0">${escapeHtml(s.guard)}</p></div>
    <div class="sgwrap">${cards}</div>
    <div class="breakbox"><div class="q">${escapeHtml(s.throughline)}</div></div>
    <p class="evsub" style="margin-top:10px">Click any mirror to follow it into the corpus. The parable rhymes with the evidence; it never replaces it.</p>
    ${busHtml}
    ${contHtml}
    ${omniaHtml}
    ${D.seal?`<div class="sealwrap"><img class="seal" src="${D.seal}" alt="OMNIA IAM FACTA SVNT — seal of authenticity" loading="lazy"><div class="sealcap">Seal of authenticity · OMNIA IAM · FACTA SVNT<br><span>Reorganization · Allocation · Calibration</span></div></div>`:''}`;
  host.dataset.done="1";
}

/* ---- Resurface: the ascent · practical reader's tools ---- */
function renderSurface(){
  const s=D.surface, host=document.getElementById('surfacewrap'); if(!s||!host||host.dataset.done) return;
  const tools=s.tools.map((t,ti)=>{
    const items=(t.from==='hygiene'&&D.consmap?D.consmap.hygiene:(t.items||[]));
    const steps=items.map((q,i)=>`<div class="surfstep"><span class="sn">${i+1}</span><span>${escapeHtml(q)}</span></div>`).join('');
    return `<div class="surftool">
      <div class="sth"><span class="stnum">0${ti+1}</span><div><div class="stname">${escapeHtml(t.name)}</div><div class="sttag">${escapeHtml(t.tag)}</div></div></div>
      <div class="surfsteps">${steps}</div>
      <div class="hq" style="margin-top:10px"><b>${escapeHtml(t.note)}</b></div></div>`;
  }).join('');
  host.innerHTML=`
    <div class="surfhero"><div class="surfarrow">⤴</div>
      <h2 class="evhead" style="margin:0">${escapeHtml(s.title)}</h2>
      <p class="surfsub">${escapeHtml(s.sub)}</p></div>
    <p class="evsub">${escapeHtml(s.intro)}</p>
    <div class="surftools">${tools}</div>
    <div class="lawline" style="margin:28px 0 8px">${escapeHtml(s.close)}</div>`;
  host.dataset.done="1";
}

/* ---- Convergence: one pattern, four lenses ---- */
function gotoNetNode(id){netFocus=id;go('network');}
function patternJump(t){
  if(!t||t==='—'){return;}
  if(t.indexOf('node:')===0){gotoNetNode(t.slice(5));return;}
  if(t==='saga'){go('saga');return;}
  if(t==='method'){go('method');return;}
  if(t==='read'){const i=D.chapters.findIndex(c=>c.status==='bridge');activeChapter=i>=0?i:0;go('read');return;}
  if(/^CH\d$/.test(t)){go('evidence');chFilter=t;tierFilter.clear();riverFilter.clear();buildChFilters();buildLegend();buildRiverFilter();document.getElementById('evsearch').value="";renderEvidence();return;}
  go('read');
}
function renderPattern(){
  const p=D.pattern, host=document.getElementById('patternwrap'); if(!p||!host||host.dataset.done) return;
  const threads=p.threads.map(t=>{
    const lenses=t.lenses.map(l=>{
      const clickable=l[3]&&l[3]!=='—';
      const reg=l[0]==='Evidence'?' logosonly':(l[0]==='Parable'?' mythosonly':'');
      return `<div class="plens${clickable?' clik':''}${reg}" style="--lc:${LENSCOL_JS(l[0])}" ${clickable?`onclick="patternJump('${l[3]}')"`:''}>
        <div class="plk">${escapeHtml(l[0])}</div>
        <div class="plbody"><span class="pltag">${escapeHtml(l[1])}</span><span class="pltxt">${escapeHtml(l[2])}</span></div>
        ${clickable?'<span class="plgo">↳</span>':''}</div>`;
    }).join('');
    return `<div class="pthread">
      <div class="pthead"><span class="ptn">${escapeHtml(t.name)}</span><span class="ptspine">${escapeHtml(t.spine)}</span></div>
      <div class="plenses">${lenses}</div></div>`;
  }).join('');
  host.innerHTML=`
    <h2 class="evhead">${escapeHtml(p.title)} <span class="cmtag big" style="vertical-align:middle">⊹ convergence</span></h2>
    <p class="evsub">${escapeHtml(p.intro)}</p>
    <div class="pthreads">${threads}</div>
    <div class="breakbox" style="border-left-color:#6f8f5a"><div class="q">${escapeHtml(p.seal)}</div></div>`;
  host.dataset.done="1";
}
function LENSCOL_JS(k){return ({"Evidence":"#6f8f5a","Network":"#9fb2c4","Mechanism":"#57cabd","Parable":"#9a86c0"})[k]||"#888";}

/* ---- Bicameral HUD: two lanes + gatekeeper, applied per chapter ---- */
const BICAM_EVMAP={"1_SURFACE_PLASTIC.md":"CH1","2_SHALLOW_CORRUPTION.md":"CH2","3_DARPA_INFRASTRUCTURE.md":"CH3","4_FULL_EXTRACTION.md":"CH4","5_BIG_TECH_SABOTAGE.md":"CH5"};
function gatekeeper(c){
  const cd=BICAM_EVMAP[c.file];
  const rows=cd?D.evidence.filter(e=>e.ch===cd):[];
  const has=l=>rows.some(e=>e.label===l);
  let light,note;
  if(c.status==='sealed'){light='red';note='Sealed high-risk draft — living-person / defamation protocol. Working material, not a finding.';}
  else if(has('Q')||has('D1')){light='red';note='Holds quarantine- or disinfo-flagged rows — kept as evidence of the framing, never endorsed.';}
  else if(c.status==='bridge'){light='amber';note='Inference bridge (I1) — a governance pattern, not an allegation of intent.';}
  else if(c.status==='draft'){light='amber';note='Draft — symbolic / speculative register present. Hold it lightly.';}
  else if(c.status==='verified'){light='green';note='Verified spine — claims wear E1/E2 sources; source-lock complete.';}
  else {light='amber';note='Mixed register — read with the labels on.';}
  return {light,note,rows,cd};
}
function renderBicameral(){
  const m=D.bicam, host=document.getElementById('bicamwrap'); if(!m||!host||host.dataset.done) return;
  const lanes=m.lanes.map(l=>`<div class="bclane" style="--lc:${l[1]}"><div class="bcln">${escapeHtml(l[0])}</div><p>${escapeHtml(l[2])}</p></div>`).join('');
  const lights=m.lights.map(l=>`<div class="bclight bc-${l[0]}"><span class="bcdot">${l[1]}</span><div><b>${escapeHtml(l[2])}</b><span>${escapeHtml(l[3])}</span></div></div>`).join('');
  const order=["E1","E2","E3","I1","I2","A1","U1","RV","R1","D1","Q","S","META"];
  let g=0,a=0,r=0;
  const rows=D.chapters.map((c,idx)=>{
    const gk=gatekeeper(c); if(gk.light==='green')g++; else if(gk.light==='amber')a++; else r++;
    const cnt={}; gk.rows.forEach(e=>cnt[e.label]=(cnt[e.label]||0)+1);
    const chips=order.filter(l=>cnt[l]).map(l=>`<span class="bctier" style="color:${cssVar(l)};border-color:${cssVar(l)}44">${l}×${cnt[l]}</span>`).join('')
      || `<span class="bctier faint">${c.words.toLocaleString()} words · ${c.status}</span>`;
    const jump=gk.cd?`<span class="jb" onclick="event.stopPropagation();gotoEvidenceCh('${gk.cd}')">▤ ${gk.cd}</span>`:'';
    return `<div class="bcrow bc-${gk.light}" onclick="openCh(${idx})">
      <div class="bcsig"><span class="bcdot">${gk.light==='green'?'🟢':gk.light==='amber'?'🟡':'🔴'}</span></div>
      <div class="bcmain">
        <div class="bcrn">${c.roman} · ${escapeHtml(c.title)} ${jump}</div>
        <div class="bctech">${chips}</div>
        <div class="bchuman">${escapeHtml(gk.note)}</div>
      </div></div>`;
  }).join('');
  host.innerHTML=`
    <h2 class="evhead">${escapeHtml(m.title)} <span class="cmtag big" style="vertical-align:middle">ConsMAP</span></h2>
    <p class="evsub">${escapeHtml(m.credit)}</p>
    <p class="evsub" style="margin-top:-4px">${escapeHtml(m.intro)}</p>
    <div class="bclanes">${lanes}</div>
    <div class="section-t">The gatekeeper</div>
    <div class="bclights">${lights}</div>
    <div class="section-t">Corpus, layer by layer · <span style="color:var(--E1)">${g} 🟢</span> · <span style="color:var(--RV)">${a} 🟡</span> · <span style="color:var(--Q)">${r} 🔴</span></div>
    <div class="bcgrid">${rows}</div>
    <p class="evsub" style="margin-top:12px">Click a layer to read it; click <b>▤</b> for its evidence. The light is computed from what each layer actually contains — sealed, quarantine-flagged, inference, or source-locked.</p>`;
  host.dataset.done="1";
}

/* ---- Field guide overlay ---- */
function buildHelpOnce(){
  const card=document.getElementById('helpcard'); if(!card||card.dataset.done) return;
  const keyrows=[['M / B / L','set reading register — Mythos · Both · Logos'],['← → · j k','page chapters (in Read)'],['?','this field guide'],['Esc','close overlays']];
  const keys=keyrows.map(k=>`<div class="hgrow"><kbd>${k[0]}</kbd><span>${k[1]}</span></div>`).join('');
  const reg=[['Mythos','the fable — symbolic layer foregrounded'],['Both','side by side'],['Logos','plain claim — sourced material only']].map(x=>`<div class="hgrow"><span class="cmtag">${x[0]}</span><span>${x[1]}</span></div>`).join('');
  const lights=(D.bicam?D.bicam.lights:[]).map(l=>`<div class="hgrow"><span style="font-size:15px">${l[1]}</span><span><b>${escapeHtml(l[2])}</b> — ${escapeHtml(l[3])}</span></div>`).join('');
  const tiers=TIERS.filter(t=>D.evidence.some(e=>e.label===t)).map(t=>`<div class="hgrow"><span class="chip on" style="background:${cssVar(t)};cursor:default">${t}</span><span>${escapeHtml(TIERMEAN[t]||t)}</span></div>`).join('');
  const rivers=Object.keys(RIVERMEAN).filter(r=>D.evidence.some(e=>e.river===r)).map(r=>`<div class="hgrow"><span class="tag river-${r}">~ ${r}</span><span>${escapeHtml(RIVERMEAN[r])}</span></div>`).join('');
  const gl=(D.guide?D.guide.concepts:[]).map(c=>`<div class="hgc"><b>${escapeHtml(c[0])}</b><span>${escapeHtml(c[1])}</span></div>`).join('');
  card.innerHTML=`<div class="hghead"><h2>Field guide</h2><span class="hgx" onclick="toggleHelp(false)">✕</span></div>
    <div class="hgcols">
      <div><div class="section-t">Keyboard</div>${keys}
        <div class="section-t">Reading register</div>${reg}
        <div class="section-t">Gatekeeper</div>${lights}</div>
      <div><div class="section-t">Evidence tiers</div>${tiers}
        <div class="section-t">StoneRiver routes</div>${rivers}</div>
    </div>
    <div class="section-t">Operating concepts</div><div class="hgconcepts">${gl}</div>
    <div class="hgcredit">${D.guide?escapeHtml(D.guide.credit):''}</div>`;
  card.dataset.done="1";
}
function toggleHelp(force){const h=document.getElementById('help'); if(!h)return; buildHelpOnce(); const show=(force===undefined)?!h.classList.contains('on'):!!force; h.classList.toggle('on',show);}
(function(){const h=document.getElementById('help'); if(h) h.addEventListener('click',e=>{if(e.target.id==='help')toggleHelp(false);});})();

/* global search -> jump into reader or evidence */
function globalSearch(v){
  v=v.trim();
  if(!v){return;}
  // try chapter title
  const ci=D.chapters.findIndex(c=>c.title.toLowerCase().includes(v.toLowerCase())||c.roman.toLowerCase()===v.toLowerCase());
  if(ci>=0){activeChapter=ci;go('read');return;}
  // else evidence search
  go('evidence'); document.getElementById('evsearch').value=v; renderEvidence();
}

document.querySelectorAll('.tab').forEach(t=>t.onclick=()=>go(t.dataset.tab));
document.getElementById('railsearch').addEventListener('keydown',e=>{if(e.key==='Enter')globalSearch(e.target.value);});
document.getElementById('evsearch').addEventListener('input',renderEvidence);
buildNav();
renderIceberg();
setRegister(register);

/* descent intro */
(function(){const i=document.getElementById('intro');if(!i)return;
  function dismiss(){i.classList.add('gone');setTimeout(()=>i.remove(),900);}
  i.addEventListener('click',dismiss); setTimeout(dismiss,2600);})();

/* scroll progress */
window.addEventListener('scroll',()=>{const b=document.getElementById('progress');if(!b)return;
  const h=document.documentElement.scrollHeight-window.innerHeight;
  b.style.width=(h>0?(window.scrollY/h*100):0)+'%';},{passive:true});

/* keyboard: arrows page chapters while reading */
document.addEventListener('keydown',e=>{
  if(e.key==='Escape'){const lb=document.getElementById('lightbox');if(lb)lb.classList.remove('on');toggleHelp(false);}
  if(['INPUT','TEXTAREA'].includes(document.activeElement.tagName))return;
  if(e.metaKey||e.ctrlKey||e.altKey)return;
  if(e.key==='?'){toggleHelp();return;}
  const k=e.key.toLowerCase();
  if(k==='m'){setRegister('mythos');return;}
  if(k==='b'){setRegister('both');return;}
  if(k==='l'){setRegister('logos');return;}
  if(activeTab!=='read')return;
  if(e.key==='ArrowRight'||e.key==='j')jumpCh(1);
  if(e.key==='ArrowLeft'||e.key==='k')jumpCh(-1);
});
"""

def J(o): return json.dumps(o, ensure_ascii=False)

# build evidence stat counts for hero
from collections import Counter
labelc=Counter(e["label"] for e in evidence)

hero_stats = [
 (status_data["chapter_count"], "chapters"),
 (len(evidence), "labelled claims"),
 (labelc.get("E1",0)+labelc.get("E2",0), "E1/E2 sourced"),
 (5, "verified spines"),
]

statcards="".join(f'<div class="stat"><div class="n">{n}</div><div class="l">{l}</div></div>' for n,l in hero_stats)

# map view content
flow = """
<div class="flow">
  <span class="node">CH5 · Big Tech</span><span class="arr">→</span>
  <span class="node b">Interlude 5.5 · Forbidden Tool [I1]</span><span class="arr">→</span>
  <span class="node s">CH6 · Epstein &amp; Money 🔒</span>
</div>"""

# ---- GHOSTCORE tab + view (native render always; original portals if found) ----
ghost_tab = '<button class="tab" data-tab="ghost">GHOSTCORE</button>'
v2btn = '<button class="tab" onclick="setGhostMode(\'v2\')">Zala&nbsp;v2&nbsp;↗</button>' if "v2" in GHOST else ''
v1btn = '<button class="tab" onclick="setGhostMode(\'v1\')">v1&nbsp;↗</button>' if "v1" in GHOST else ''
ghost_view = f"""
    <section id="view-ghost" class="view">
      <div class="ghosthead">
        <div><h2>\U0001f702 GHOSTCORE — The Logic Revealed</h2>
          <div class="gx">Zala's pattern portal · rebuilt native &amp; offline · IDRIJA · EPSTEIN · DIGITAL · PLASTIC</div></div>
        <div class="gtoggle">
          <button class="tab on" onclick="setGhostMode('native')">Native</button>{v2btn}{v1btn}
        </div>
      </div>
      <div id="ghost-native" class="gnative"></div>
      <iframe id="ghostframe" class="ghostframe" data-v2="{GHOST.get('v2','')}" data-v1="{GHOST.get('v1','')}" title="GHOSTCORE Portal" loading="lazy"></iframe>
    </section>"""

# ---- Visions gallery (only if art curated) ----
visions_tab = '<button class="tab" data-tab="visions">Visions</button>' if art else ''
hero_bg = f'<div class="hero-bg" style="background-image:url(\'{HERO}\')"></div>' if HERO else ''
visions_view = """
    <section id="view-visions" class="view">
      <div class="visions">
        <h2 class="evhead">Visions</h2>
        <p class="evsub">Sigils, flames, glyphs, ravens — the project's mythic register. <b style="color:var(--S)">S-label: symbolic, not evidence.</b></p>
        <div id="vgrid" class="vgrid"></div>
      </div>
    </section>
    <div id="lightbox"><img id="lbimg" alt=""><div class="lc" id="lbcap"></div></div>""" if art else ""

HTML = f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ZALA · Operator — ANON × ConsMAP × GHOSTCORE</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;1,9..144,400&family=Spectral:ital,wght@0,300;0,400;0,500;1,400&family=IBM+Plex+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head><body>
<div id="progress"></div>
<div id="intro"><div class="strata2"></div>
  <div class="ti">The <em>Pattern</em></div>
  <div class="ds">A Forensic Descent</div>
  <div class="hint">click to enter ·  ↓</div></div>
<div class="app">
  <aside class="rail">
    <div class="brand">ZALA <span class="glow">·</span> OPERATOR</div>
    <div class="brand-sub">ANON × ConsMAP × GHOSTCORE</div>
    <input id="railsearch" class="search" placeholder="search ↵  (chapter or evidence)">
    <div class="tabs">
      <button class="tab on" data-tab="home">Home</button>
      <button class="tab" data-tab="read">Read</button>
      <button class="tab" data-tab="evidence">Evidence</button>
      <button class="tab" data-tab="map">Map</button>
      <button class="tab" data-tab="pattern">⊹ Pattern</button>
      <button class="tab" data-tab="network">Network</button>
      <button class="tab" data-tab="method">Method</button>
      <button class="tab" data-tab="bicam">Bicameral</button>
      <button class="tab" data-tab="saga">Saga</button>
      <button class="tab" data-tab="surface">⤴ Resurface</button>
      {ghost_tab}
      {visions_tab}
    </div>
    <div class="raildial">
      <div class="rdcap">Reading register <span class="rdkeys">M · B · L</span></div>
      <div class="dial3 raildial3">
        <button class="dialseg" data-reg="mythos" onclick="setRegister('mythos')" title="Mythos — the fable (press M)">Mythos</button>
        <button class="dialseg" data-reg="both" onclick="setRegister('both')" title="Both — side by side (press B)">Both</button>
        <button class="dialseg" data-reg="logos" onclick="setRegister('logos')" title="Logos — plain claim (press L)">Logos</button>
      </div>
      <div class="rdnote" id="rdnote"></div>
    </div>
    <div id="navlist" class="navlist"></div>
    <button class="printbtn" onclick="doPrint()" title="Print the current view in the active register">🔦 Print · lights on</button>
    <button class="printbtn helpbtn" onclick="toggleHelp()" title="Field guide — keys, legends, concepts (press ?)">? Field guide</button>
  </aside>
  <main class="main">

    <section id="view-home" class="view on">
      <div class="hero">
        {hero_bg}
        <div class="strata"></div>
        <div class="kick">Evidence-locked · ConsMAP-aligned · Witness posture</div>
        <h1>The Forbidden Tool<br>Becomes the <em>Product</em></h1>
        <p class="lede">A layered forensic descent — plastic, capital, surveillance, AI — read with the lights on. Every claim wears its evidence label. The system loves drama; this does not feed it.</p>
        <div class="meta"><span>WRITTEN BY · ŠABAD</span><span>STRUCTURE · AETHERON / LYRA</span><span>BUILD · {status_data['generated']}</span></div>
      </div>
      <div class="lawline">Keep the complexity. <b>Sort it.</b> A false claim stays as evidence of disinformation; a rumor stays a rumor; a court filing stays a court filing — and the public reading never confuses them.</div>
      <div class="statgrid">{statcards}</div>
      <div class="icewrap">
        <div class="icehead"><span class="il">The Descent</span><span class="ir">surface → abyss · click a stratum to read · density = labelled claims</span></div>
        <div class="waterline"><span>S U R F A C E</span></div>
        <div id="iceberg" class="iceberg"></div>
      </div>
      <div class="foot">Unified site · ANON corpus × ConsMAP discipline × Zala's GHOSTCORE · self-contained, offline.<br>
      Verified spines: CH1–CH5 · KAIROS lane complete · Interlude 5.5 · CH6/CH7 sealed · every claim dual-labelled (ANON tier + ConsMAP) and routed (StoneRiver).<br>
      Reads ANON + ConsMAP read-only; writes only here. Regenerate with <code>python3 build_zalasite.py</code>.</div>
    </section>

    <section id="view-read" class="view"><div id="reader"></div></section>

    <section id="view-evidence" class="view">
      <div class="evwrap">
        <h2 class="evhead">Evidence Ledger</h2>
        <p class="evsub">Every source-locked claim, wearing its label. Filter by chapter, by tier, or search the wording.</p>
        <input id="evsearch" class="search" style="max-width:420px" placeholder="search claims…">
        <div id="chfilters" class="filters"></div>
        <div id="legend" class="legend"></div>
        <div id="riverlegend" class="legend riverlegend"></div>
        <div id="evcount" class="evcount"></div>
        <div id="evgrid" class="evgrid"></div>
      </div>
    </section>

    <section id="view-map" class="view">
      <div class="mapwrap">
        <h2 class="evhead">Bridge &amp; Build Map</h2>
        <p class="evsub">Where the corpus stands. The span between CH5 and CH6 carries inference traffic only.</p>
        {flow}
        <div class="section-t">Verified spines</div>
        <div class="pipe">{''.join(f'<span class="pill" style="border-color:#234a2f;color:var(--E1)">{c} ✓</span>' for c in status_data['verified'])}</div>
        <div class="section-t">Side lane — KAIROS</div>
        <div class="pipe">{''.join(f'<span class="pill">{s}</span>' for s in ['map','verify','apparatus','integrity'])}</div>
        <div class="section-t">Interlude 5.5 pipeline</div>
        <div class="pipe">{''.join(f'<span class="pill">{s}</span>' for s in ['decision','rails','draft','review PASS','inserted'])}</div>
        <div class="section-t">Sealed</div>
        <div class="pipe">{''.join(f'<span class="pill" style="border-color:#4a2626;color:var(--Q)">{c} 🔒</span>' for c in status_data['sealed'])}</div>
        <div class="warnbox"><h3>⚠ Bridge guardrails (non-negotiable)</h3>
          <ul><li>Bridge joint = I1 (governance inference, not an E1 allegation)</li>
          <li>NOT proof of hidden intent · NOT secret deployment · NOT theft</li>
          <li>Identity is never causation · named network ≠ conspiracy</li>
          <li>No leaked code reproduced</li></ul></div>
      </div>
    </section>
    <section id="view-method" class="view"><div id="methodwrap" class="mapwrap"></div></section>

    <section id="view-network" class="view">
      <div class="netwrap">
        <h2 class="evhead">The Network</h2>
        <p class="evsub">Documented funding &amp; role nodes — Wexner · Epstein · the banks · the venture money · the surveillance infrastructure. Each edge wears its evidence tier. Click a node to isolate its ties; click again to release. Click <b>▤</b> to jump to that thread in the ledger.</p>
        <div id="netlegend" class="netlegend"></div>
        <div id="netstage" class="netstage"></div>
        <div id="netnote" class="netnote"></div>
      </div>
    </section>

    <section id="view-saga" class="view"><div id="sagawrap" class="mapwrap"></div></section>
    <section id="view-bicam" class="view"><div id="bicamwrap" class="mapwrap"></div></section>
    <section id="view-pattern" class="view"><div id="patternwrap" class="mapwrap"></div></section>
    <section id="view-surface" class="view"><div id="surfacewrap" class="mapwrap"></div></section>
    {ghost_view}
    {visions_view}

  </main>
</div>
<button id="resurface-fab" class="resurface-fab" onclick="go('surface')" title="Resurface — back up to the reader's tools">⤴ <span>Resurface</span></button>
<div id="help" class="helpmodal"><div class="helpcard" id="helpcard"></div></div>
<script>window.__ANON__ = {J(DATA)};</script>
<script>{APPJS}</script>
</body></html>"""

outp=os.path.join(OUT,"index.html")
open(outp,"w",encoding="utf-8").write(HTML)
size=os.path.getsize(outp)/1024
print(f"wrote {outp}  ({size:.0f} KB)")
print(f"chapters embedded: {len(chapters)} | evidence rows: {len(evidence)} | label spread: {dict(labelc)}")
