// src/utils/shadowLedger.js

const PRODUCTS = {
    krompir: { weight: 50, systemPriceRange: [40, 55], toneIncome: [7, 15] },
    drva: { weight: 1, systemPriceRange: [150, 250], toneIncome: [50, 100] },
    mleko: { weight: 10, systemPriceRange: [1.2, 1.8], toneIncome: [0.4, 0.8] },
    jajca: { weight: 30, systemPriceRange: [3.5, 5.0], toneIncome: [1.0, 2.0] },
};

export const analyzeProduct = (productKey, quantity, customPrice) => {
    const data = PRODUCTS[productKey];
    if (!data) return null;

    const systemAvg = customPrice || (data.systemPriceRange[0] + data.systemPriceRange[1]) / 2;
    const toneAvg = (data.toneIncome[0] + data.toneIncome[1]) / 2;

    // Ghost Gap: (System Price - Tone Income) / System Price
    const ghostGap = systemAvg > 0 ? (systemAvg - toneAvg) / systemAvg : 0;

    // Bypass (CSA) Calculation
    const csaPrice = systemAvg * 0.8; // 20% cheaper for consumer
    const csaToneIncome = toneAvg * 1.5; // 50% more for Tone

    const newGhostGap = csaPrice > 0 ? (csaPrice - csaToneIncome) / csaPrice : 0;

    return {
        systemAvg: systemAvg.toFixed(2),
        toneAvg: toneAvg.toFixed(2),
        ghostGap: (ghostGap * 100).toFixed(1),
        csaPrice: csaPrice.toFixed(2),
        csaToneIncome: csaToneIncome.toFixed(2),
        newGhostGap: (newGhostGap * 100).toFixed(1),
        customerSavings: (systemAvg - csaPrice).toFixed(2),
        toneIncomeIncrease: (csaToneIncome - toneAvg).toFixed(2),
    };
};

export const PRODUCT_LIST = Object.keys(PRODUCTS);
