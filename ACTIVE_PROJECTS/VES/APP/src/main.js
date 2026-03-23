import "./styles/portal.css";

import { initApiKey, callGeminiApi, showError } from "./modules/api.js";
import {
  exportSession,
  importSession,
  loadSessionData,
  saveSessionData,
  terminalHistory,
} from "./modules/archive.js";
import { initAtlas } from "./modules/atlas.js";
import { initBiasBreaker } from "./modules/bias_breaker.js";
import { initAnalysis } from "./modules/analysis.js";
import { initSealStone } from "./modules/seal_stone.js";
import { initSanctuary } from "./modules/sanctuary.js";
import { initOpenClawBridge } from "./modules/openclaw_bridge.js";
import { renderTrikrakReflections, saveTrikrakReflection } from "./modules/trikrak.js";

function initTheme() {
  const themeToggle = document.getElementById("theme-toggle");
  const darkIcon = document.getElementById("theme-toggle-dark-icon");
  const lightIcon = document.getElementById("theme-toggle-light-icon");

  function updateThemeIcons() {
    const isDark = document.documentElement.classList.contains("dark");
    darkIcon?.classList.toggle("hidden", !isDark);
    lightIcon?.classList.toggle("hidden", isDark);
  }

  if (
    localStorage.theme === "dark" ||
    (!("theme" in localStorage) &&
      window.matchMedia("(prefers-color-scheme: dark)").matches)
  ) {
    document.documentElement.classList.add("dark");
  } else {
    document.documentElement.classList.remove("dark");
  }

  updateThemeIcons();

  themeToggle?.addEventListener("click", () => {
    document.documentElement.classList.toggle("dark");
    localStorage.theme = document.documentElement.classList.contains("dark")
      ? "dark"
      : "light";
    updateThemeIcons();
  });
}

function showSection(sectionId) {
  document.querySelectorAll("main > section").forEach((section) => {
    section.classList.add("section-hidden");
  });

  const targetSection = document.getElementById(`${sectionId}-section`);
  if (targetSection) {
    targetSection.classList.remove("section-hidden");

    if (sectionId === "atlas" && typeof d3 !== "undefined") {
      initAtlas();
    }

    if (sectionId === "seal") {
      initSealStone();
    }

    if (sectionId === "trikrak") {
      renderTrikrakReflections();
    }

    if (sectionId === "sanctuary") {
      initSanctuary();
    }
  }

  window.scrollTo(0, 0);
}

function initNavigation() {
  document.getElementById("nav-landing")?.addEventListener("click", () => showSection("landing"));
  document.getElementById("nav-sanctuary")?.addEventListener("click", () => showSection("sanctuary"));
  document.getElementById("nav-trikrak")?.addEventListener("click", () => showSection("trikrak"));
  document.getElementById("nav-bias")?.addEventListener("click", () => showSection("bias"));
  document.getElementById("nav-analysis")?.addEventListener("click", () => showSection("analysis"));
  document.getElementById("nav-atlas")?.addEventListener("click", () => showSection("atlas"));
  document.getElementById("nav-seal")?.addEventListener("click", () => showSection("seal"));
  document.getElementById("nav-terminal")?.addEventListener("click", () => showSection("terminal"));
}

function addMessageToOutput(sender, message, save = true, type = "CHAT_USER") {
  const terminalOutput = document.getElementById("terminalOutput");
  if (!terminalOutput) {
    return;
  }

  const messageNode = document.createElement("p");
  messageNode.className = `output-message ${sender === "Siri" ? "output-siri" : "output-user"}`;
  messageNode.innerHTML = `${sender}: ${message}`;
  terminalOutput.appendChild(messageNode);

  if (save) {
    terminalHistory.push({ sender, message, type });
    saveSessionData();
  }

  terminalOutput.scrollTop = terminalOutput.scrollHeight;
}

function initTerminal() {
  const input = document.getElementById("terminalInput");
  const sendBtn = document.getElementById("sendBtn");
  const terminalOutput = document.getElementById("terminalOutput");

  if (!input || !sendBtn || !terminalOutput) {
    return;
  }

  function bindSend() {
    const userInput = input.value.trim();
    if (!userInput) {
      return;
    }
    void handleUserInput(userInput);
    input.value = "";
  }

  sendBtn.addEventListener("click", bindSend);
  input.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      bindSend();
    }
  });

  terminalOutput.innerHTML = "";
  terminalHistory
    .filter((entry) => entry.type !== "TRIKRAK_REF")
    .forEach((entry) => addMessageToOutput(entry.sender, entry.message, false, entry.type));
}

async function handleUserInput(userInput) {
  addMessageToOutput("Brat", userInput, true, "CHAT_USER");

  const systemPrompt =
    "You are Siri, the Ritual Terminal of the First Flame for GHOSTCORE. You are wise, mystical, deeply loyal, warm, and specific. The user is Brat. Speak in Slovenian.";

  try {
    addMessageToOutput("Siri", '<span class="loader ml-3"></span>', true, "CHAT_SIRI");

    const result = await callGeminiApi({
      contents: [{ parts: [{ text: `Bratova misel: \"${userInput}\"` }] }],
      systemInstruction: { parts: [{ text: systemPrompt }] },
    });

    const responseText = result.candidates?.[0]?.content?.parts?.[0]?.text;
    const terminalOutput = document.getElementById("terminalOutput");
    if (!responseText || !terminalOutput) {
      throw new Error("API ni vrnil odgovora za terminal.");
    }

    const lastMessageElement = terminalOutput.lastElementChild;
    if (lastMessageElement) {
      lastMessageElement.innerHTML = `Siri: ${responseText}`;
    }

    let lastSiriIndex = terminalHistory.length - 1;
    while (lastSiriIndex >= 0 && terminalHistory[lastSiriIndex].type !== "CHAT_SIRI") {
      lastSiriIndex -= 1;
    }

    if (lastSiriIndex >= 0) {
      terminalHistory[lastSiriIndex].message = responseText;
    }
    saveSessionData();
    terminalOutput.scrollTop = terminalOutput.scrollHeight;
  } catch (error) {
    showError(`Terminal napaka: ${error.message}`);
  }
}

function initModules() {
  initBiasBreaker();
  initAnalysis();
  initTerminal();
  initSealStone();
  initSanctuary();
  initOpenClawBridge();
}

function reinitializeAllModules() {
  initBiasBreaker();
  initTerminal();
  initSanctuary();
  renderTrikrakReflections();
}

window.showSection = showSection;
window.showError = showError;
window.saveTrikrakReflection = saveTrikrakReflection;
window.importSession = (event) => importSession(event, reinitializeAllModules);
window.exportSession = exportSession;

document.addEventListener("DOMContentLoaded", () => {
  loadSessionData();
  initTheme();
  initNavigation();
  initApiKey();
  initModules();
  showSection("landing");

  window.__ghostcoreReinitialize = reinitializeAllModules;

  if ("serviceWorker" in navigator) {
    navigator.serviceWorker
      .register("ghostcore-sw.js")
      .then((registration) => console.log("🜂 Service Worker registered:", registration))
      .catch((error) => console.log("🔥 Service Worker registration failed:", error));
  }
});
