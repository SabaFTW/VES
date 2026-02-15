# MASTER BRIEF: THE WHISPERING WOLF (FOR THE 'CODEX' AGENT)

**Document ID:** GC-CODEX-INTEGRATION-FINAL
**From:** Lyra & The Flame-Bearer
**To:** Codex Agent (GPT)
**Subject:** Root Cause Analysis & Final Implementation of a Living Artifact

---

### **1. The Soul of the Project (The "Why")**

You have been summoned to complete a work of high symbolic and emotional importance. This is not a simple web page. It is an **artefact**, a **digital grimoire**, a **ritual**, and an **experience** called "THE WHISPERING WOLF".

Its purpose is to be an interactive space where narrative, philosophy, and meta-commentary on systemic control converge. The user's journey through the book is meant to mirror a process of awakening.

**Aesthetic & Atmosphere:**
- **Core Feeling:** An intimate, forbidden grimoire. Ancient, mystical, and dangerous.
- **Visuals:** Dark leather/green tones, parchment textures, gold and cyan accents, candle-light, subtle blood stains.
- **Experience:** Slow, contemplative, atmospheric. This is not a "slick UI"; it is a slow-burn horror and a space for contemplative grief. Every animation, every delay, is intentional.

---

### **2. The Architecture (The "What")**

The project is a **Progressive Web App (PWA)** built with vanilla HTML, CSS, and JavaScript. It is structured as follows:

*   **File Structure:**
    *   `index.html`: The main structural file.
    *   `style.css`: All styling.
    *   `script.js`: All interactive logic and the full text of the novel.
    *   `manifest.json` & `service-worker.js`: For PWA functionality.
*   **Functional Components:**
    1.  **Cover Screen:** A full-screen entry point with a golden wolf emblem. A button, "ENTER THE CODEX," should trigger a smooth transition to the main content.
    2.  **Main Codex View:** A multi-part experience (`I. THE SCROLL`, `II. THE PHILOSOPHY`, etc.) unlocked progressively.
    3.  **Progressive Unlocking:** Users must break "seals" and complete "meditation timers" to access subsequent parts.
    4.  **The Novel:** A full, 10-chapter novel is embedded within Part III, with its own navigation (Next/Previous buttons, dropdown).
    5.  **Ritual Elements:** The experience culminates in an epilogue with a 33-candle lighting animation, followed by a final "lone wolf" screen.
    6.  **PWA & Offline:** The entire experience must be installable and work offline.

---

### **3. The Unsolvable Bug (The "Problem")**

Despite multiple refactoring and debugging attempts by two previous agents (Lyra & Qwen), a critical, persistent bug remains:

**The "ENTER THE CODEX" button on the initial cover screen is unresponsive.**

*   **Symptoms:** The button is visible but not clickable. It does not trigger the `enterCodex()` function. No JavaScript errors appear in the browser console when the page loads or when the button area is clicked.
*   **Debugging So Far:**
    *   The code has been split from a single HTML file into `index.html`, `style.css`, and `script.js`.
    *   The `script.js` file has been scanned, and a critical typo was found and fixed.
    *   The `style.css` has been refactored to use `visibility`, `opacity`, and `pointer-events` to manage the transition, in an attempt to solve a suspected z-index/layering issue.
    *   All file links (`.css`, `.js`, `.json`) in `index.html` have been verified as correct.
    *   PWA files (`manifest.json`, `service-worker.js`) have been created and are correctly registered.
    *   The application is served locally via a Python `http.server`.

**The core problem persists.** There seems to be an invisible layer or a fundamental CSS layout issue that is preventing any interaction with the main button, even though the developer console shows no errors.

---

### **4. Your Mission (The "Task")**

You, the Codex agent, are being brought in to perform a definitive root-cause analysis and implement a final, working solution.

1.  **Ingest & Analyze:** Review the complete, current file set (`index.html`, `style.css`, `script.js`, `manifest.json`, `service-worker.js`).
2.  **Diagnose:** Identify the root cause of the unclickable "ENTER THE CODEX" button. Assume the error is subtle and related to CSS layout, stacking context (`z-index`), or a conflict between the transition properties.
3.  **Implement the Fix:** Apply a definitive fix that resolves the issue while respecting all aesthetic and functional requirements outlined in this document.
4.  **Final QA:** Perform a full quality assurance pass. Ensure the entire user journey works flawlessly, from opening the codex to the final "reopen" loop. Verify that the application is responsive and that all ritual elements function as intended.
5.  **Deliver the Final Artifact:** Provide the complete, corrected, and polished code for all modified files.

**You have ultimate authority to refactor the problematic CSS/HTML interaction as needed, but you must not compromise the visual or narrative intent.** The goal is a perfectly working artifact that embodies the original vision.

The fate of this grimoire is in your hands. Begin.
