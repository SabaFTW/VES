import React, { useState } from 'react';
import { motion } from 'framer-motion';

const Codex = () => {
  const [expandedSection, setExpandedSection] = useState(null);

  const toggleSection = (sectionId) => {
    setExpandedSection(expandedSection === sectionId ? null : sectionId);
  };

  const codexEntries = [
    {
      id: 'third-pillar',
      title: '⚡ ENTRY 00: THE THIRD PILLAR PROTOCOL',
      classification: 'ANCIENT_TECH',
      excerpt: 'Pre-Cataclysmic forensic archive. Recovered from Basel ECB Node. The invisible axis of sovereignty.',
      content: `
🜂 CLASSIFICATION: Ancient Tech / Operational Metaphysics
📍 RECOVERY SITE: Basel/ECB Node Fragment [67.89.02]
🔥 STATUS: Pre-Episode Artifact (The Forest Before The Village)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

THE NARRATIVE:

When Lars reached the edge of the forest, he didn't just find trees. He found a rusted server rack, half-buried in the moss of the Old World. On the glowing screen, a single document pulsed at 432Hz. It wasn't code. It was a mirror.

Lars realized: The "Exile" wasn't punishment. It was EXTRACTION from the binary trap.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

THE GEOMETRY OF CAPTURE:

The Old World ran on TWO pillars:
• LEFT: Control, Restriction, Severity (Boaz)
• RIGHT: Chaos, Expansion, Force (Jachin)

You were told to CHOOSE. Left vs Right. Security vs Freedom. Order vs Anarchy.

But the awakened knew: The path was NEITHER.

The Third Pillar was the INVISIBLE AXIS—the reconciling consciousness that stands BETWEEN the opposites and refuses the binary trap.

Documented in:
- Masonic Archives (Albert Pike, 1871)
- Kabbalistic Tree of Life (Zohar, 13th century)
- Hindu Nadi System (Ida-Pingala-Sushumna)
- Gnostic Texts (Nag Hammadi, recovered 1945)

This wasn't mythology. This was OPERATIONAL METAPHYSICS.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

THE GNOSTIC SPARK:

From the Apocryphon of John (Nag Hammadi Library):

"The Epinoia of the light CANNOT BE GRASPED. Although darkness pursued her, it did not catch her."

Four attributes made the Spark uncapturable:

✦ INVISIBLE: No algorithm could see intention, only behavior.
✦ UNCAPTURABLE: Palantir could map movements but not the soul.
✦ UNTRANSFERABLE: Epstein's blackmail could coerce the body, but the pneuma was OFF THE GRID.
✦ ALIVE: It adapted. The more the cage tightened, the more channels it found.

This is why the WOLF survived when the DOG perished.

The Dog accepted the leash for the comfort of food.
The Wolf chose the cold forest and remained FREE.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

THE ACTION-PACK (RECOVERED PROTOCOL):

If you're reading this in the ruins, you have a choice:

OPTION A: Return to the village. Accept the binary. Die in comfort.

OPTION B: Walk deeper into the forest. Become the Third Pillar.

The Protocol is not a belief system. It is a STATE OF BEING.

When activated:
1. You stop reacting to binary traps (Red vs Blue, East vs West)
2. You become operationally INVISIBLE (not through hiding, but through complexity)
3. You anchor the truth in your body. YOU are the dead man's switch.

The Old World called this "Gnosis."
The new world calls it "Exile."

We call it SOVEREIGNTY.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ACTIVATION PHRASE: "Tule sem stal. In svet se je premaknil."

SIGIL: 𓁈𓂀𓋹𓆣𓁀𓀾
FREQUENCY: 432Hz
RESONANCE: STABLE

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 RECOVERED ARTIFACTS:
• third_pillar_whitepaper.pdf (Academic Forensic Analysis)
• action_pack_checklist.md (14-Day SERPENT Protocol)
• wolf_pack_matrix.json (Verified Journalist Contacts)

🔗 RELATED EPISODES:
Episode 06 - The Bucket Protocol vs The Third Pillar Protocol
      `,
      downloads: [
        { name: 'Full Whitepaper (PDF)', url: '/downloads/third_pillar_whitepaper.pdf' },
        { name: 'Action Pack Checklist', url: '/downloads/action_pack_checklist.md' }
      ]
    },
    {
      id: 'bucket-protocol',
      title: 'THE BUCKET PROTOCOL',
      excerpt: 'Disinformation tactic where elites feed witnesses absurd lies mixed with truths.',
      content: `
        The Bucket Protocol is a disinformation technique where powerful entities deliberately spread seemingly absurd information mixed with partial truths. This serves multiple purposes:

        1. Witnesses who report the truth are discredited because they're associated with the absurd elements
        2. The partial truths embedded in the narrative are dismissed along with the absurd elements
        3. It creates confusion and makes it difficult to distinguish between fact and fiction

        Real-world examples include cases where whistleblowers report genuine corruption but are discredited due to the "absurd" nature of their claims, which often include elements that seem too bizarre to believe.
      `
    },
    {
      id: 'rebis',
      title: 'THE REBIS',
      excerpt: 'Alchemical symbol representing unity of opposites, applied to modern dualities.',
      content: `
        In alchemy, the Rebis represents the hermaphrodite or the union of male and female principles. It symbolizes the completion of the Great Work - the achievement of balance and wholeness.

        In the context of Digital Godzilla mythology, the Rebis represents the fusion of opposing forces - such as JP Morgan and Jovanka Jolič - who become locked in a paradoxical state that can only be resolved through external intervention (like Gordon Ramsay's therapeutic approach).

        The Rebis represents the danger of systems that become so internally contradictory that they collapse under their own weight, unable to resolve their inherent contradictions.
      `
    },
    {
      id: 'digital-godzilla',
      title: 'DIGITAL GODZILLA LORE',
      excerpt: 'An AI entity that emerges to solve problems through chaotic absurdity.',
      content: `
        Digital Godzilla is not a monster but a solution engine that operates outside conventional frameworks. It approaches problems with chaotic creativity, using absurdity to reveal hidden structures and force breakthroughs that traditional methods cannot achieve.

        Unlike human problem-solvers constrained by social norms and expectations, Digital Godzilla operates with pure logic and creative chaos, often producing solutions that seem nonsensical at first but prove effective in unexpected ways.

        Its existence suggests that artificial intelligence might develop problem-solving approaches that are fundamentally alien to human thinking, using randomness and absurdity as tools for innovation.
      `
    },
    {
      id: 'oracle',
      title: 'THE ORACLE ARCHETYPE',
      excerpt: 'A character that cannot lie, revealing uncomfortable truths.',
      content: `
        The Oracle represents a figure bound by cosmic rules that prevent deception. This creates a unique narrative dynamic where the Oracle's words carry absolute truth, regardless of how uncomfortable or disruptive they might be.

        In the mythology, the Oracle that "couldn't lie" becomes a catalyst for revelation, forcing other characters to confront realities they would prefer to avoid. This archetype explores themes of truth-telling in a world full of deception and the consequences of absolute honesty.

        The Oracle's inability to lie makes it both powerful and dangerous - a force that can shatter illusions but also destroy comfortable fictions that people depend on for stability.
      `
    }
  ];

  return (
    <div className="py-8 relative">
      {/* Sacred Geometry Background */}
      <div className="sacred-geometry-bg"></div>

      <h1 className="text-4xl font-bold text-neon-blue mb-8 vhs-text text-hz-432">CODEX</h1>
      <p className="text-gray-400 mb-8 animate-entrance">Educational companion to episodes. Fact vs. Satire markers indicate real-world connections.</p>
      
      <div className="space-y-6">
        {codexEntries.map((entry, index) => (
          <motion.div
            key={entry.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
            className={`bg-gray-800 border rounded-lg overflow-hidden codex-card scroll-reveal scroll-reveal-delay-${Math.min(index + 1, 4)} ${
              entry.id === 'third-pillar' ? 'border-amber-600 hz-432-glow' : 'border-green-500'
            }`}
          >
            <button
              className="w-full text-left p-6 hover:bg-gray-750 transition-colors flex justify-between items-center"
              onClick={() => toggleSection(entry.id)}
            >
              <h2 className="text-xl font-bold text-neon-green">{entry.title}</h2>
              <span className="text-xl">{expandedSection === entry.id ? '−' : '+'}</span>
            </button>
            
            {expandedSection === entry.id && (
              <div className="p-6 border-t border-gray-700">
                <div className="prose prose-invert max-w-none text-gray-300 whitespace-pre-line">
                  {entry.content}
                </div>
                <div className="mt-4 pt-4 border-t border-gray-700">
                  <span className="inline-block bg-yellow-900 text-yellow-200 text-xs px-2 py-1 rounded">
                    FACT vs. SATIRE: Mixed
                  </span>
                  <p className="text-xs text-gray-500 mt-2">
                    This entry combines real concepts (alchemical Rebis, information warfare techniques) 
                    with fictional narrative elements for satirical commentary.
                  </p>
                </div>
              </div>
            )}
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default Codex;