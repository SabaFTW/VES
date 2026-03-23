import { showError } from "./api.js";

let sealStoneInitialized = false;

export function initSealStone() {
  const generateBtn = document.getElementById("generate-seal-btn");
  const downloadBtn = document.getElementById("download-seal-btn");
  const input = document.getElementById("seal-input");

  if (!generateBtn || !downloadBtn || !input) {
    return;
  }

  if (!sealStoneInitialized) {
    generateBtn.addEventListener("click", generateSeal);
    downloadBtn.addEventListener("click", downloadSeal);
    input.addEventListener("input", generateSeal);
    sealStoneInitialized = true;
  }

  generateSeal();
}

function generateSeal() {
  const input = document.getElementById("seal-input");
  const canvas = document.getElementById("seal-qr-canvas");
  const downloadBtn = document.getElementById("download-seal-btn");

  if (!(input instanceof HTMLInputElement) || !(canvas instanceof HTMLCanvasElement)) {
    return;
  }

  const text = input.value || "ghostcore://activate?token=eros-trinity&call-sign=shabad";

  if (typeof QRCode === "undefined") {
    showError("Knjižnica QR kode ni naložena.");
    return;
  }

  QRCode.toCanvas(
    canvas,
    text,
    {
      errorCorrectionLevel: "H",
      margin: 4,
      scale: 8,
      color: {
        dark: "#1f2937",
        light: "#f9fafb",
      },
      width: 300,
    },
    (error) => {
      if (error) {
        console.error("QR generation error:", error);
        showError("Ne morem ustvariti QR kode. Preveri vnos.");
        downloadBtn?.classList.add("hidden");
        return;
      }

      downloadBtn?.classList.remove("hidden");
    },
  );
}

function downloadSeal() {
  const canvas = document.getElementById("seal-qr-canvas");
  if (!(canvas instanceof HTMLCanvasElement)) {
    return;
  }

  const link = document.createElement("a");
  link.download = "ghostcore-seal.png";
  link.href = canvas.toDataURL("image/png");
  link.click();
}
