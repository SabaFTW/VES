// 🜂 GHOSTCORE Module: api.js (External Resonance & Error Handling)

/**
 * Prikazovanje sporočil o napakah (ali uspehu) v modalnem oknu.
 * @param {string} message - Besedilo sporočila.
 * @param {string} [title="Napaka"] - Naslov sporočila.
 */
export function showError(message, title = "Napaka") {
    document.getElementById('error-message').textContent = message;
    document.getElementById('error-modal').querySelector('h3').textContent = title;
    document.getElementById('error-modal').classList.remove('hidden');
}

// Globalni event listener za zapiranje error modala (ker je premaknjen v modul)
document.getElementById('close-error-btn').addEventListener('click', () => {
    document.getElementById('error-modal').classList.add('hidden');
});

// Cache API key to avoid repeated DOM/localStorage access
let cachedApiKey = null;

/**
 * Upravljanje z API ključem in vizualno stanje (Always-On Resonance).
 * Avtomatsko naloži ključ iz localStorage.
 */
export function initApiKey() {
    const apiKeyInput = document.getElementById('api-key-input');
    const apiKeyIndicator = document.getElementById('api-key-indicator');
    const savedApiKey = localStorage.getItem('geminiApiKey');
    
    function updateApiKeyStatus(isSet) {
        apiKeyIndicator.classList.toggle('bg-red-500', !isSet);
        apiKeyIndicator.classList.toggle('bg-green-500', isSet);
        apiKeyIndicator.title = isSet ? 'API ključ je nastavljen' : 'API ključ ni nastavljen';
    }

    if (savedApiKey) {
        apiKeyInput.value = savedApiKey;
        cachedApiKey = savedApiKey; // Cache the key
    }

    updateApiKeyStatus(!!savedApiKey);
    
    apiKeyInput.addEventListener('input', () => {
        const key = apiKeyInput.value.trim();
        cachedApiKey = key; // Update cache
        localStorage.setItem('geminiApiKey', key);
        updateApiKeyStatus(!!key);
    });
}

/**
 * Izvaja klic Gemini API z eksponentnim povratnim udarcem (Exponential Backoff).
 * @param {object} payload - Payload za API.
 * @returns {Promise<object>} - Odgovor API-ja.
 */
export async function callGeminiApi(payload) {
    // Use cached API key to avoid repeated DOM/localStorage access
    const apiKey = cachedApiKey || 
                   document.getElementById('api-key-input')?.value.trim() || 
                   localStorage.getItem('geminiApiKey');
    
    if (!apiKey) {
        throw new Error('Gemini API ključ ni nastavljen.');
    }

    const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key=${apiKey}`;
    
    const maxRetries = 5;
    let attempt = 0;

    while (attempt < maxRetries) {
        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                const result = await response.json();
                if (result.candidates && result.candidates.length > 0) {
                    return result;
                }
                throw new Error('Nepričakovana struktura odgovora iz API-ja.');
            } 
            
            if ((response.status === 429 || response.status >= 500) && attempt < maxRetries - 1) {
                const delay = Math.pow(2, attempt) * 1000 + Math.random() * 500;
                await new Promise(resolve => setTimeout(resolve, delay));
                attempt++;
                continue; 
            }

            const errorData = await response.json();
            throw new Error(`API zahteva neuspešna: ${errorData.error.message}`);

        } catch (error) {
            if (attempt < maxRetries - 1 && error.message.includes('Failed to fetch')) {
                const delay = Math.pow(2, attempt) * 1000 + Math.random() * 500;
                await new Promise(resolve => setTimeout(resolve, delay));
                attempt++;
                continue;
            }
            throw error;
        }
    }
    throw new Error("API klic ni uspel po večkratnih poskusih.");
}
