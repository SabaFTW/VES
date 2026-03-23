// 🜂 GHOSTCORE Module: archive.js (Session State & EchoWrite Archive)

export let terminalHistory = [];
export let biasGameState = { completed: false, lastPath: null };

const LOCAL_STORAGE_KEY = 'ghostcoreSessionData_v2';
const SANCTUARY_STORAGE_KEY = 'ghostcoreSanctuary_v1';

/** Nalaganje stanja iz localStorage ob zagonu. */
export function loadSessionData() {
    try {
        const storedData = localStorage.getItem(LOCAL_STORAGE_KEY);
        if (storedData) {
            const data = JSON.parse(storedData);
            terminalHistory.length = 0; // Clear existing array reference
            Array.prototype.push.apply(terminalHistory, data.terminalHistory || []);
            biasGameState.completed = data.biasGameState?.completed || false;
            biasGameState.lastPath = data.biasGameState?.lastPath || null;
            console.log("EchoWrite: Zapis seje uspešno naložen.");
        }
    } catch (e) {
        console.error("EchoWrite: Napaka pri nalaganju seje.", e);
    }
}

/** Shranjevanje trenutnega stanja v localStorage. */
export function saveSessionData() {
    try {
        const dataToStore = {
            terminalHistory: terminalHistory,
            biasGameState: biasGameState
        };
        localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(dataToStore));
    } catch (e) {
        console.error("EchoWrite: Napaka pri shranjevanju seje.", e);
    }
}


// ------------------- RAKON IZVOZ/UVOZ (File I/O) -------------------

/** Izvozi celotno sejo kot EchoWrite Record (.json datoteka). */
export function exportSession() {
    // Poskrbi, da je zadnje stanje shranjeno v state
    saveSessionData();

    const exportData = {
        version: "GHOSTCORE_v2.4_Modular",
        timestamp: new Date().toISOString(),
        terminalHistory: terminalHistory,
        biasGameState: biasGameState,
        sanctuaryState: JSON.parse(localStorage.getItem(SANCTUARY_STORAGE_KEY) || '{}')
    };

    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(exportData, null, 2));
    const downloadAnchorNode = document.createElement('a');

    // Ustvari dinamično ime datoteke: EchoWrite_Archive_2025-10-06.json
    downloadAnchorNode.setAttribute("href", dataStr);
    downloadAnchorNode.setAttribute("download", `EchoWrite_Archive_${new Date().toISOString().substring(0, 10)}.json`);

    // Simulacija klika
    document.body.appendChild(downloadAnchorNode);
    downloadAnchorNode.click();
    downloadAnchorNode.remove();

    console.log("EchoWrite: Zapis uspešno IZVOŽEN. RAKON.");
}


/** Uvozi sejo iz EchoWrite Record datoteke in posodobi stanje. */
export function importSession(event, reinitializeCallback) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
        try {
            const importedData = JSON.parse(e.target.result);

            if (importedData.version && importedData.terminalHistory) {
                // Posodobi globalne reference stanja
                terminalHistory.length = 0;
                Array.prototype.push.apply(terminalHistory, importedData.terminalHistory);
                biasGameState.completed = importedData.biasGameState?.completed || false;
                biasGameState.lastPath = importedData.biasGameState?.lastPath || null;
                if (importedData.sanctuaryState) {
                    localStorage.setItem(SANCTUARY_STORAGE_KEY, JSON.stringify(importedData.sanctuaryState));
                }

                saveSessionData(); // Shrani uvoženo sejo lokalno
                console.log(`EchoWrite: Zapis uspešno UVOŽEN (v${importedData.version}).`);

                // Ponovno inicializiraj module, da se osveži DOM (Terminal, Bias, Trikrak)
                if (reinitializeCallback) {
                    reinitializeCallback();
                }
            } else {
                throw new Error("Nepravilna struktura datoteke EchoWrite Record.");
            }
        } catch (error) {
            console.error("Napaka pri branju/parsanju uvožene datoteke:", error);
            // Klic globalne funkcije showError (predpostavljamo, da je v api.js)
            if (window.showError) window.showError("Napaka EchoWrite uvoza. Prosim, preverite, če je datoteka pravilna JSON seveda.");
        }
    };
    reader.readAsText(file);
}


// ------------------- Archive Listener Setup -------------------

/** Nastavi listenerje za gumbe Izvoz/Uvoz in veže uvoz na reinitialize funkcijo. */
export function setupArchiveListeners(reinitializeCallback) {
    const exportBtn = document.getElementById('exportFileInput');
    const importInput = document.getElementById('importFileInput');
    const importBtn = document.getElementById('importFileBtn'); // Gumb, ki sproži input

    if (exportBtn) exportBtn.addEventListener('click', exportSession);

    if (importInput) {
        importInput.addEventListener('change', (event) => {
            importSession(event, reinitializeCallback);
        });
    }

    // Vezava "UVOZI" gumba na skriti input file element
    if (importBtn) {
        importBtn.addEventListener('click', () => {
            importInput.click();
        });
    }
}

// Globalni export funkcije za HTML onclick (za Bias Game)
window.exportSession = exportSession;
