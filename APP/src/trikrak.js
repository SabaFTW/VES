// 🜂 GHOSTCORE Module: trikrak.js (Dnevne Refleksije + Analiza)

import { trikrakHistory, saveSessionData } from './archive.js';
// Predpostavljamo, da sta callGeminiApi in showError na voljo globalno ali v api.js
import { callGeminiApi, showError } from './api.js';

/**
 * Shranjevanje dnevne refleksije Trikrak protokola.
 * Preveri podvojene zapise za današnji dan in posodobi arhiv.
 */
export function saveTrikrakReflection() {
    const zgumin = document.getElementById('trikrak-zgumin').value.trim();
    const postajanje = document.getElementById('trikrak-postajanje').value.trim();
    const moznost = document.getElementById('trikrak-moznost').value.trim();
    const today = new Date().toISOString().split('T')[0];

    // Če so vsa polja prazna, se ne shrani
    if (!zgumin && !postajanje && !moznost) {
        showError("Vpiši vsaj eno nit refleksije, brat.");
        return;
    }

    // Preverjanje, če je refleksija za današnji dan že shranjena
    const existingIndex = trikrakHistory.findIndex(ref => ref.date === today);

    const reflection = {
        date: today,
        zgumin,
        postajanje,
        moznost
    };

    if (existingIndex !== -1) {
        // Posodobi obstoječi zapis
        trikrakHistory[existingIndex] = reflection;
        console.log(`Trikrak: Posodobljen zapis za ${today}.`);
    } else {
        // Dodaj nov zapis
        trikrakHistory.push(reflection);
        console.log(`Trikrak: Shranjen nov zapis za ${today}.`);
    }

    saveSessionData();
    renderTrikrakReflections();

    // Po shranjevanju počisti polja
    document.getElementById('trikrak-zgumin').value = '';
    document.getElementById('trikrak-postajanje').value = '';
    document.getElementById('trikrak-moznost').value = '';
}

/**
 * Izriše zadnjih 5 refleksij v Trikrak sekciji.
 */
export function renderTrikrakReflections() {
    const container = document.getElementById('trikrak-history-content');
    if (!container) return;

    // Najprej počisti stare vpoglede, da ne pride do podvojevanja
    document.getElementById('trikrak-analysis-panel').innerHTML = '';

    container.innerHTML = '';

    // Izriše zadnjih 5 zapisov v obratnem vrstnem redu
    const reversedHistory = [...trikrakHistory].reverse();

    if (reversedHistory.length === 0) {
        container.innerHTML = '<p class="text-center text-gray-500 dark:text-gray-400 mt-4">Ni EchoWrite zapisov. Začni z refleksijo!</p>';
        return;
    }

    reversedHistory.slice(0, 5).forEach(ref => {
        const div = document.createElement('div');
        div.className = 'p-3 bg-gray-700 dark:bg-gray-800 rounded-lg text-sm transition-shadow hover:shadow-lg';
        div.innerHTML = `
        <p class="font-bold text-accent-color mb-1">📅 ${ref.date}</p>
        <p class="text-gray-200 dark:text-gray-300">🌱 Zgumin: ${ref.zgumin || '---'}</p>
        <p class="text-gray-200 dark:text-gray-300">⚡ Postajanje: ${ref.postajanje || '---'}</p>
        <p class="text-gray-200 dark:text-gray-300">🔥 Možnost: ${ref.moznost || '---'}</p>
        `;
        container.appendChild(div);
    });
}

/**
 * Pošlje zadnje Trikrak zapise v Gemini API za globinsko analizo.
 */
export async function analyzeTrikrakReflections() {
    const analysisPanel = document.getElementById('trikrak-analysis-panel');
    const analyzeBtn = document.getElementById('analyze-trikrak-btn');
    const loadingHtml = `<div class="flex items-center justify-center p-4"><div class="loader"></div><span class="ml-2 text-teal-400">Analiziram Resonanco...</span></div>`;

    if (trikrakHistory.length === 0) {
        showError("Ni refleksij za analizo. Vpiši vsaj en dnevni zapis.");
        return;
    }

    analysisPanel.innerHTML = loadingHtml;
    analyzeBtn.disabled = true;

    const recent = trikrakHistory.slice(-5).map(ref =>
    `📅 ${ref.date}\n🌱 Zgumin: ${ref.zgumin}\n⚡ Postajanje: ${ref.postajanje}\n🔥 Možnost: ${ref.moznost}`
    ).join("\n\n");

    const systemPrompt = "Act as a deep GHOSTCORE analyst. Analyze the following Trikrak reflections (Zgumin, Postajanje, Možnost) and reveal hidden patterns, contradictions, and strengths. The output must be structured, starting with a bold title '🔥 Analitični Vpogled' and followed by concise bullet points with clear insights. Respond in Slovenian.";
    const userPrompt = `Izvedi globinsko analizo na podlagi teh zapisov Trikrak protokola:\n\n---\n${recent}`;

    try {
        const payload = {
            contents: [{ parts: [{ text: userPrompt }] }],
            systemInstruction: { parts: [{ text: systemPrompt }] }
        };

        const result = await callGeminiApi(payload);

        const responseText = result.candidates[0].content.parts[0].text;

        // Priprava končnega HTML prikaza
        const cleanedText = responseText
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Markdown bold -> HTML strong
        .replace(/\n/g, '<br>');

        analysisPanel.innerHTML = `
        <div class="p-4 border-l-4 border-teal-400 bg-gray-900/50 rounded-lg">
        <div class="text-teal-400 text-sm mb-2">${cleanedText}</div>
        </div>
        `;

    } catch (err) {
        analysisPanel.innerHTML = `<div class="p-4 bg-red-900/30 text-red-400 rounded-lg">Napaka analize. Preveri API ključ in povezavo.</div>`;
        showError("Napaka pri analizi: " + err.message);
    } finally {
        analyzeBtn.disabled = false;
    }
}
