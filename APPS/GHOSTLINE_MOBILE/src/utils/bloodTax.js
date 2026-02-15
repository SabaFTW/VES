// src/utils/bloodTax.js

export const calculateBloodTax = (numPrompts, avgTokens) => {
    const totalTokens = numPrompts * avgTokens;

    // Energy: ~0.7 kWh per 1M tokens (conservative estimate)
    const energyKwh = (totalTokens / 1_000_000) * 0.7;

    // Cobalt: Nvidia H100 uses ~3.5g cobalt per GPU
    // Assume 1 GPU processes ~10M tokens/hour
    // AER Factor: 74x (DRC extraction ratio)
    const cobaltBaseG = (totalTokens / 10_000_000) * 3.5;
    const cobaltAerAdjustedG = cobaltBaseG * 74;

    // Water: 0.5L per query (cooling)
    const waterLiters = numPrompts * 0.5;

    // Carbon Footprint
    const carbonKg = energyKwh * 0.4; // EU grid average ~400g CO2/kWh

    return {
        totalTokens,
        energyKwh: energyKwh.toFixed(4),
        cobaltG: cobaltAerAdjustedG.toFixed(6),
        waterL: waterLiters.toFixed(2),
        carbonKg: carbonKg.toFixed(4),
        // Fun metric: % of a smartphone battery (approx 15g cobalt)
        smartphoneBatteryPct: ((cobaltAerAdjustedG / 15) * 100).toFixed(4)
    };
};
