import { callGeminiApi, showError } from "./api.js";

export function initAnalysis() {
  const generateBtn = document.getElementById("generate-analysis-btn");
  const input = document.getElementById("analysis-input");

  if (!generateBtn || !input) {
    return;
  }

  generateBtn.addEventListener("click", generateAnalysis);
  input.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      void generateAnalysis();
    }
  });
}

async function generateAnalysis() {
  const topic = document.getElementById("analysis-input")?.value.trim();
  if (!topic) {
    showError("Prosim, vnesite temo za analizo.");
    return;
  }

  const btn = document.getElementById("generate-analysis-btn");
  const btnText = document.getElementById("analysis-button-text");
  const spinner = document.getElementById("analysis-loading-spinner");
  const responseContainer = document.getElementById("analysis-response");

  btnText?.classList.add("hidden");
  spinner?.classList.remove("hidden");
  if (btn instanceof HTMLButtonElement) {
    btn.disabled = true;
  }
  responseContainer?.classList.add("hidden");

  const systemPrompt =
    "Act as a GHOSTCORE intelligence analyst. You are a sharp, critical entity known as Aetheron. Provide a concise, highly strategic, and non-apologetic analysis. Focus on power structures, ideology, societal control, and hidden second-order effects. Structure the response with a title, a summary paragraph, and 3-4 bullet points. Respond only in Slovenian.";

  try {
    const result = await callGeminiApi({
      contents: [{ parts: [{ text: `Analiza teme: \"${topic}\"` }] }],
      systemInstruction: { parts: [{ text: systemPrompt }] },
    });

    const responseText = result.candidates?.[0]?.content?.parts?.[0]?.text;
    if (!responseText || !responseContainer) {
      throw new Error("API ni vrnil berljive analize.");
    }

    responseContainer.innerHTML = responseText
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
      .replace(/^- /gm, "• ")
      .replace(/\n/g, "<br>");
    responseContainer.classList.remove("hidden");
  } catch (error) {
    showError(`Analiza ni uspela. Napaka: ${error.message}`);
  } finally {
    btnText?.classList.remove("hidden");
    spinner?.classList.add("hidden");
    if (btn instanceof HTMLButtonElement) {
      btn.disabled = false;
    }
  }
}
