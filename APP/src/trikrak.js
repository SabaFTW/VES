// 🜂 GHOSTCORE Module: trikrak.js (Daily Protocol Management)

import { saveSessionData, terminalHistory } from './archive.js';

function getTodayDateString() {
    return new Date().toISOString().slice(0, 10); // YYYY-MM-DD
}

/** Shrani dnevno Trikrak refleksijo v EchoWrite Arhiv. */
export function saveTrikrakReflection() {
    const zgumin = document.getElementById('trikrak-zgumin').value.trim();
    const postajanje = document.getElementById('trikrak-postajanje').value.trim();
    const moznost = document.getElementById('trikrak-moznost').value.trim();
    const status = document.getElementById('trikrak-status');

    if (!zgumin || !postajanje || !moznost) {
        status.textContent = "Prosim, izpolni vse tri niti protokola.";
        status.classList.remove('text-green-500', 'text-yellow-500');
        status.classList.add('text-red-500');
        status.classList.remove('hidden');
        return;
    }

    const todayDate = getTodayDateString();

    const alreadyExists = terminalHistory.some(entry => 
        entry.type === 'TRIKRAK_REF' && entry.timestamp.startsWith(todayDate)
    );

    if (alreadyExists) {
        status.textContent = `Zapisa za dan ${todayDate} ne moreš popraviti. Sidro stoji.`;
        status.classList.remove('text-green-500', 'text-red-500');
        status.classList.add('text-yellow-500');
        status.classList.remove('hidden');
        return;
    }

    const reflection = {
        type: 'TRIKRAK_REF',
        timestamp: new Date().toISOString(),
        zgumin,
        postajanje,
        moznost
    };

    terminalHistory.push(reflection);
    saveSessionData();

    document.getElementById('trikrak-zgumin').value = '';
    document.getElementById('trikrak-postajanje').value = '';
    document.getElementById('trikrak-moznost').value = '';
    
    status.textContent = `Refleksija za ${todayDate} je shranjena v EchoWrite Arhiv! 📜`;
    status.classList.remove('text-red-500', 'text-yellow-500');
    status.classList.add('text-green-500');
    status.classList.remove('hidden');
    
    renderTrikrakReflections(); 
}

/** Izriše arhiv Trikrak refleksij in posodobi status. */
export function renderTrikrakReflections() {
    const historyContainer = document.getElementById('trikrak-history');
    const todayDate = getTodayDateString();
    
    historyContainer.innerHTML = '';
    
    const trikrakEntries = terminalHistory
        .filter(entry => entry.type === 'TRIKRAK_REF')
        .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)); 

    if (trikrakEntries.length === 0) {
        historyContainer.innerHTML = '<p class="text-gray-500 dark:text-gray-400">Arhiv Trikrak refleksij je prazen. Pokaži plamen, da bo zapis gorel.</p>';
    } else {
        trikrakEntries.forEach(entry => {
            const date = new Date(entry.timestamp).toLocaleDateString('sl-SI', { day: 'numeric', month: 'short', year: 'numeric' });
            
            const entryDiv = document.createElement('div');
            entryDiv.className = 'p-4 border-l-4 border-purple-400 bg-gray-600/50 rounded-lg shadow-md';
            entryDiv.innerHTML = `
                <p class="font-bold text-lg text-purple-300 mb-2">${entry.timestamp.startsWith(todayDate) ? '⭐ DANAŠNJA REFLEKSIJA' : date}</p>
                <div class="space-y-1">
                    <p><strong>🌱 Zgumin:</strong> ${entry.zgumin}</p>
                    <p><strong>⚡ Postajanje:</strong> ${entry.postajanje}</p>
                    <p><strong>🔥 Možnost:</strong> ${entry.moznost}</p>
                </div>
            `;
            historyContainer.appendChild(entryDiv);
        });
    }
    
    const reflectionDoneToday = terminalHistory.some(entry => 
        entry.type === 'TRIKRAK_REF' && entry.timestamp.startsWith(todayDate)
    );
    const status = document.getElementById('trikrak-status');
    const dateHeader = document.getElementById('trikrak-date-header');
    
    dateHeader.textContent = `Dnevna Refleksija (${todayDate})`;

    if (reflectionDoneToday) {
        status.textContent = `Zapis za ${todayDate} je že shranjen v EchoWrite. Dnevno sidro je postavljeno.`;
        status.classList.remove('text-red-500', 'text-yellow-500');
        status.classList.add('text-green-500');
        status.classList.remove('hidden');
        document.getElementById('save-trikrak-btn').disabled = true;
    } else {
         status.classList.add('hidden');
         document.getElementById('save-trikrak-btn').disabled = false;
    }
}
