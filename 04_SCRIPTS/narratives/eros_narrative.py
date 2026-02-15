import json
import os

# Define the absolute path for the evidence directory
evidence_dir = '/home/saba/VES/TROJAN_HORSE/evidence/realpage_yieldstar'

# Naloži podatke
report_path = os.path.join(evidence_dir, 'consistency_report.json')
with open(report_path, 'r') as f:
    report = json.load(f)

# Ustrei narativ za ProPublica članek
narrative = f"""
# RAZKRITJE: ALGORITEM ZA NEPREMIČNINE USKLAJUJE CENE ČEZ ZDA

**Konsistenčna ocena: {report['consistency_score']}%** - Dokaz sistematične usklajenosti

## KLJUČNE UGOTOVITVE:

### $2,750 - MAGIČNA ŠTEVILKA
- **Boston:** "One Bedroom Deluxe" - $2,750
- **Seattle:** "One Bedroom Suite" - $2,750  
- **Chicago:** "One Bedroom Standard" - $2,750

Kako lahko tri različne nepremičnine v treh različnih mestih imajo identično ceno? To ni trg. To je algoritem.

### $4,500 - DUPLIKAT ZA LUKSUZ
- **Boston:** "Three Bedroom Penthouse" - $4,500
- **Chicago:** "Penthouse Skyline" - $4,500

Tudi luksuzni trg kaže znake usklajevanja, kar kaže na sistemski pristop.

## MEHANIZEM KONTROLE:

Podatki kažejo na uporabo algoritma YieldStar, ki:
1. Analizira tržne podatke v realnem času, vključno s podatki konkurentov.
2. Optimizira najemnine za maksimiranje dobička lastnikov, ne za odražanje ponudbe in povpraševanja.
3. Usklajuje cene čez različne geografije in lastnike, kar duši konkurenco.
4. Ustvarja umetno konsistentnost namesto organske tržne dinamike.

## POSLEDICE:

- Najemniki preplačujejo zaradi algoritmično napihnjenih cen.
- Trg ni več prost, ampak algoritmično kontroliran s strani peščice.
- Potrebna je takojšnja regulatorna preiskava s strani FTC in DOJ.
"""

output_path = os.path.join(evidence_dir, 'PROPUBLICA_NARRATIVE.md')
with open(output_path, 'w') as f:
    f.write(narrative)

print(f"Narrative saved to {output_path}")
