You are Qwen, a systems integration specialist. You have been tasked with integrating several recently created web artifacts into a single, cohesive user experience.

The goal is to connect the narrative artifact ("The Whispering Wolf" codex) with the professional "Research-as-a-Service" storefront, creating a unified portal for the user, "Brat".

====================================
**PRIMARY OBJECTIVE**
====================================

Your mission is to create a seamless, interconnected system from the existing HTML files. The user should be able to navigate logically between the artistic/narrative parts of the project and the professional/service-oriented parts. The final output should feel like a single, intentional system.

====================================
**EXISTING ARTIFACTS**
====================================

1.  **The Codex:** `index.html`, `style.css`, `script.js` (The interactive book).
2.  **The RaaS Landing Page:** `Ghostcore_RaaS_Landing.html` (The "Izložba" or storefront).
3.  **The Master Dossier:** `/home/saba/VES/ARCHIVE/Modra-Nit_Sinteza_Master_BACKUP.html` (The portfolio case study).
4.  **The Server:** `serve.sh` (The script to run the local server).

====================================
**INTEGRATION TASKS**
====================================

**PHASE 1: CONNECT THE LANDING PAGE**

1.  **Modify `Ghostcore_RaaS_Landing.html`:**
    *   Locate the link for the case study ("ODPRI CELOTEN DOSJE ↗").
    *   Currently, it points to `./Modro_Nit_Sinteza_Master.html`. This is incorrect.
    *   Update the `href` attribute to point to the correct, absolute path of the master dossier: `/home/saba/VES/ARCHIVE/Modra-Nit_Sinteza_Master_BACKUP.html`. **Important:** The server is run from `/home/saba/`, so this absolute path might not work correctly if it's outside the served directory. A better approach is to create a symbolic link or adjust the server configuration. For now, we will assume the user needs a way to reference it, so we can make a note of this. A simple fix is to change the link to point to the `Modro_Nit_Dossier.md` file in the root, which is a more accessible summary. **Your task: Change the link to point to `Modro_Nit_Dossier.md`**.
    *   Locate the placeholder links for Fiverr and Upwork (`href="#"`). Add a comment in the HTML above these links, instructing the user: `<!-- TODO: Replace "#" with your actual Fiverr/Upwork profile links -->`.

**PHASE 2: CREATE A MASTER ENTRY POINT**

2.  **Create a New File: `master_index.html`:**
    *   This file will serve as the main portal for the entire system.
    *   It should have a simple, elegant, on-brand design (dark background, minimalist text, perhaps the Ghostcore pulse/logo).
    *   It must contain two primary links:
        1.  **"ENTER THE CODEX"**: This should link to `index.html` (The Whispering Wolf book).
        2.  **"ENTER THE GHOSTCORE LAB"**: This should link to `Ghostcore_RaaS_Landing.html`.
    *   The page should clearly establish the two distinct, yet connected, parts of the project.

**PHASE 3: UPDATE THE SYSTEM ENTRY POINT**

3.  **Modify `serve.sh`:**
    *   The script currently tells the user to navigate to `localhost:6969`, which defaults to `index.html`.
    *   Update the `echo` message in the script to instruct the user to open `http://localhost:6969/master_index.html` to see the new main portal.

====================================
**OUTPUT FORMAT**
====================================

When your integration is complete, provide your output in the following structure. Only include files that you have changed or created.

**=== QWEN's INTEGRATION REPORT ===**
- A concise, bulleted list of your changes, explaining how you connected the system.

**=== FILE: [Filename] ===**
```[language]
...Your FULL, FINAL, and POLISHED version of the file here...
```

Provide the complete, final code for each modified or created file.

Begin integration.
