// 🜂 GHOSTCORE Module: trikrak.js (Daily Reflections / EchoWrite archive)

import { terminalHistory, saveSessionData } from './archive.js';

function getTodayDateString() {
    return new Date().toISOString().slice(0, 10);
}

function setStatusMessage(message, variant = 'info') {
    const statusEl = document.getElementById('trikrak-status');
    if (!statusEl) return;

    statusEl.textContent = message;
    statusEl.classList.remove('hidden', 'text-red-500', 'text-yellow-500', 'text-green-500');

    if (variant === 'error') {
        statusEl.classList.add('text-red-500');
    } else if (variant === 'warning') {
        statusEl.classList.add('text-yellow-500');
    } else {
        statusEl.classList.add('text-green-500');
    }
}

function hideStatusMessage() {
    const statusEl = document.getElementById('trikrak-status');
    if (!statusEl) return;
    statusEl.classList.add('hidden');
    statusEl.classList.remove('text-red-500', 'text-yellow-500', 'text-green-500');
}

function clearInputs() {
    const fields = ['trikrak-zgumin', 'trikrak-postajanje', 'trikrak-moznost'];
    fields.forEach((id) => {
        const el = document.getElementById(id);
        if (el) el.value = '';
    });
}

/**
 * Saves a Trikrak reflection for the current day into the EchoWrite archive.
 * Reflections are persisted inside the shared terminalHistory array so they are
 * exported together with the rest of the ritual log.
 */
export function saveTrikrakReflection() {
    const zgumin = document.getElementById('trikrak-zgumin')?.value.trim() || '';
    const postajanje = document.getElementById('trikrak-postajanje')?.value.trim() || '';
    const moznost = document.getElementById('trikrak-moznost')?.value.trim() || '';
    const saveButton = document.getElementById('save-trikrak-btn');

    if (!zgumin || !postajanje || !moznost) {
        setStatusMessage('Prosim, izpolni vse tri niti protokola.', 'error');
        return;
    }

    const today = getTodayDateString();
    const alreadyExists = terminalHistory.some(
        (entry) => entry.type === 'TRIKRAK_REF' && entry.timestamp?.startsWith(today)
    );

    if (alreadyExists) {
        setStatusMessage(`Zapis za ${today} je že shranjen v EchoWrite. Dnevno sidro stoji.`, 'warning');
        if (saveButton) saveButton.disabled = true;
        return;
    }

    terminalHistory.push({
        type: 'TRIKRAK_REF',
        timestamp: new Date().toISOString(),
        zgumin,
        postajanje,
        moznost
    });

    saveSessionData();
    clearInputs();
    setStatusMessage(`Refleksija za ${today} je shranjena v EchoWrite Arhiv! 📜`, 'success');
    renderTrikrakReflections();
}

function createHistoryEntry(reflection, today) {
    const entryDiv = document.createElement('div');
    entryDiv.className = 'p-4 border-l-4 border-purple-400 bg-gray-600/50 rounded-lg shadow-md';

    const dateLabel = reflection.timestamp.startsWith(today)
        ? '⭐ DANAŠNJA REFLEKSIJA'
        : new Date(reflection.timestamp).toLocaleDateString('sl-SI', {
            day: 'numeric',
            month: 'short',
            year: 'numeric'
        });

    entryDiv.innerHTML = `
        <p class="font-bold text-lg text-purple-300 mb-2">${dateLabel}</p>
        <div class="space-y-1">
            <p><strong>🌱 Zgumin:</strong> ${reflection.zgumin}</p>
            <p><strong>⚡ Postajanje:</strong> ${reflection.postajanje}</p>
            <p><strong>🔥 Možnost:</strong> ${reflection.moznost}</p>
        </div>
    `;

    return entryDiv;
}

/**
 * Renders the Trikrak history list and updates the daily status banner.
 */
export function renderTrikrakReflections() {
    const historyContainer = document.getElementById('trikrak-history');
    const dateHeader = document.getElementById('trikrak-date-header');
    const saveButton = document.getElementById('save-trikrak-btn');

    if (!historyContainer || !dateHeader) {
        return;
    }

    const today = getTodayDateString();
    dateHeader.textContent = `Dnevna Refleksija (${today})`;

    historyContainer.innerHTML = '';

    const reflections = terminalHistory
        .filter((entry) => entry.type === 'TRIKRAK_REF')
        .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

    if (reflections.length === 0) {
        historyContainer.innerHTML = '<p class="text-gray-500 dark:text-gray-400">Arhiv Trikrak refleksij je prazen. Pokaži plamen, da bo zapis gorel.</p>';
    } else {
        reflections.forEach((reflection) => {
            historyContainer.appendChild(createHistoryEntry(reflection, today));
        });
    }

    const reflectionDoneToday = reflections.some((entry) => entry.timestamp.startsWith(today));

    if (reflectionDoneToday) {
        setStatusMessage(`Zapis za ${today} je že shranjen v EchoWrite. Dnevno sidro je postavljeno.`);
        if (saveButton) saveButton.disabled = true;
    } else {
        hideStatusMessage();
        if (saveButton) saveButton.disabled = false;
    }
}
