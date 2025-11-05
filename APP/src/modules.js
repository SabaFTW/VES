// 🜂 GHOSTCORE Module: modules.js (Bias Game, Analysis, Seal Stone)

import { biasGameState, saveSessionData } from './archive.js';
import { callGeminiApi, showError } from './api.js';

// Cache DOM elements for Analysis module
let analysisElements = null;

// ------------------- Bias Game -------------------

/** Inicializacija Bias Game (Resetiranje se reši v main.js) */
export function initBiasGame() {
    // Re-render based on current state
    const pathSelection = document.getElementById('path-selection');
    const pathsContainer = document.getElementById('paths-container');
    const resultDiv = document.getElementById('result');
    const paths = document.querySelectorAll('#bias-section .path');

    if (biasGameState.completed) {
        pathSelection.classList.add('hidden');
        pathsContainer.classList.remove('hidden');
        paths.forEach(p => p.classList.add('animate'));
        resultDiv.style.opacity = 1;
    } else {
        pathSelection.classList.remove('hidden');
        pathsContainer.classList.add('hidden');
        paths.forEach(p => p.classList.remove('animate'));
        resultDiv.style.opacity = 0;
    }

    // Export handlers back to global scope for HTML onclick
    window.selectPath = (side) => {
        biasGameState.completed = true;
        biasGameState.lastPath = side;
        saveSessionData();
        
        pathSelection.classList.add('hidden');
        pathsContainer.classList.remove('hidden');
        paths.forEach(p => p.classList.add('animate'));
        
        setTimeout(() => {
            resultDiv.style.opacity = 1;
        }, 3000);
    };

    window.resetGame = () => {
        biasGameState.completed = false;
        biasGameState.lastPath = null;
        saveSessionData();

        pathSelection.classList.remove('hidden');
        pathsContainer.classList.add('hidden');
        resultDiv.style.opacity = 0;
        paths.forEach(p => { p.classList.remove('animate'); void p.offsetHeight; });
    };
}


// ------------------- Analysis Module -------------------

export function initAnalysis() {
    // Cache DOM elements for better performance
    analysisElements = {
        generateBtn: document.getElementById('generate-analysis-btn'),
        input: document.getElementById('analysis-input'),
        btnText: document.getElementById('analysis-button-text'),
        spinner: document.getElementById('analysis-loading-spinner'),
        responseContainer: document.getElementById('analysis-response')
    };
    
    analysisElements.generateBtn.addEventListener('click', generateAnalysis);
    analysisElements.input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            generateAnalysis();
        }
    });
}

async function generateAnalysis() {
    const topic = analysisElements.input.value.trim();
    if (!topic) {
        showError("Prosim, vnesite temo za analizo.");
        return;
    }

    analysisElements.btnText.classList.add('hidden');
    analysisElements.spinner.classList.remove('hidden');
    analysisElements.generateBtn.disabled = true;
    analysisElements.responseContainer.classList.add('hidden');

    const systemPrompt = "Act as a GHOSTCORE intelligence analyst. You are a sharp, critical entity known as Aetheron. Provide a concise, highly strategic, and non-apologetic analysis. Focus on its connection to power structures, ideology, societal control, and potential unseen consequences (the 'echoes'). Structure the response with a title, a summary paragraph, and 3-4 bullet points with key insights. Respond only in Slovenian.";
    const userQuery = `Analiza teme: "${topic}"`;

    try {
        const result = await callGeminiApi({
            contents: [{ parts: [{ text: userQuery }] }],
            systemInstruction: { parts: [{ text: systemPrompt }] }
        });
        
        const responseText = result.candidates[0].content.parts[0].text;
        
        // Optimize string replacements by chaining and using simpler operations
        analysisElements.responseContainer.innerHTML = responseText
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/^- /gm, '• ') 
            .replace(/\n/g, '<br>');
            
        analysisElements.responseContainer.classList.remove('hidden');

    } catch (error) {
        showError("Analiza ni uspela. Napaka: " + error.message);
    } finally {
        analysisElements.btnText.classList.remove('hidden');
        analysisElements.spinner.classList.add('hidden');
        analysisElements.generateBtn.disabled = false;
    }
}


// ------------------- Seal Stone Module -------------------

export function initSealStone() {
    const generateBtn = document.getElementById('generate-seal-btn');
    const downloadBtn = document.getElementById('download-seal-btn');
    
    generateBtn.addEventListener('click', generateSeal);
    downloadBtn.addEventListener('click', downloadSeal);
    
    generateSeal(); // Generate default seal on load
}

function generateSeal() {
    const input = document.getElementById('seal-input');
    const canvas = document.getElementById('seal-qr-canvas');
    const downloadBtn = document.getElementById('download-seal-btn');
    
    const text = input.value || "ghostcore://activate?token=eros-trinity&call-sign=shabad";
    
    if (typeof QRCode === 'undefined') {
        showError("Knjižnica QR kode ni naložena.");
        return;
    }

    QRCode.toCanvas(canvas, text, {
        errorCorrectionLevel: 'H',
        margin: 4,
        scale: 8,
        color: {
            dark: '#1f2937', 
            light: '#f9fafb' 
        },
        width: 300 
    }, function (error) {
        if (error) {
            console.error("QR Code Generation Error:", error);
            showError("Ne morem ustvariti QR kode. Preveri vnos.");
            downloadBtn.classList.add('hidden');
        } else {
            downloadBtn.classList.remove('hidden');
        }
    });
}

function downloadSeal() {
    const canvas = document.getElementById('seal-qr-canvas');
    const link = document.createElement('a');
    link.download = 'ghostcore-seal.png';
    link.href = canvas.toDataURL('image/png');
    link.click();
}
