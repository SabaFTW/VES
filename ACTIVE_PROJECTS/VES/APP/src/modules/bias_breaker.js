import { biasGameState, saveSessionData } from "./archive.js";

export function initBiasBreaker() {
  const pathSelection = document.getElementById("path-selection");
  const pathsContainer = document.getElementById("paths-container");
  const resultDiv = document.getElementById("result");
  const paths = document.querySelectorAll("#bias-section .path");

  if (!pathSelection || !pathsContainer || !resultDiv) {
    return;
  }

  if (biasGameState.completed) {
    pathSelection.classList.add("hidden");
    pathsContainer.classList.remove("hidden");
    paths.forEach((path) => path.classList.add("animate"));
    resultDiv.style.opacity = "1";
  } else {
    pathSelection.classList.remove("hidden");
    pathsContainer.classList.add("hidden");
    paths.forEach((path) => path.classList.remove("animate"));
    resultDiv.style.opacity = "0";
  }

  window.selectPath = (side) => {
    biasGameState.completed = true;
    biasGameState.lastPath = side;
    saveSessionData();

    pathSelection.classList.add("hidden");
    pathsContainer.classList.remove("hidden");
    paths.forEach((path) => path.classList.add("animate"));

    window.setTimeout(() => {
      resultDiv.style.opacity = "1";
    }, 3000);
  };

  window.resetGame = () => {
    biasGameState.completed = false;
    biasGameState.lastPath = null;
    saveSessionData();

    pathSelection.classList.remove("hidden");
    pathsContainer.classList.add("hidden");
    resultDiv.style.opacity = "0";
    paths.forEach((path) => {
      path.classList.remove("animate");
      void path.getBoundingClientRect();
    });
  };
}
