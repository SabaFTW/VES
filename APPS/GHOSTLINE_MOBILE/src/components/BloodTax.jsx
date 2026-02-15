import React, { useState, useEffect } from 'react';
import { calculateBloodTax } from '../utils/bloodTax';
import { Battery, Zap, Droplets, Gem } from 'lucide-react';

const BloodTax = () => {
    const [prompts, setPrompts] = useState(50);
    const [tokens, setTokens] = useState(1000);
    const [results, setResults] = useState(null);

    useEffect(() => {
        setResults(calculateBloodTax(prompts, tokens));
    }, [prompts, tokens]);

    if (!results) return null;

    return (
        <div className="card space-y-4">
            <h2 className="text-xl flex items-center gap-2">
                <Gem className="text-primary" /> Blood Tax Calculator
            </h2>

            <div className="grid grid-cols-2 gap-4">
                <div>
                    <label className="block text-xs uppercase text-gray-400 mb-1">Prompts</label>
                    <input
                        type="number"
                        value={prompts}
                        onChange={(e) => setPrompts(Number(e.target.value))}
                        className="w-full bg-background border border-gray-700 rounded p-2 focus:border-primary outline-none"
                    />
                </div>
                <div>
                    <label className="block text-xs uppercase text-gray-400 mb-1">Avg Tokens</label>
                    <input
                        type="number"
                        value={tokens}
                        onChange={(e) => setTokens(Number(e.target.value))}
                        className="w-full bg-background border border-gray-700 rounded p-2 focus:border-primary outline-none"
                    />
                </div>
            </div>

            <div className="grid grid-cols-2 gap-3 pt-2">
                <Metric
                    icon={<Zap size={16} />}
                    label="Energy"
                    value={`${results.energyKwh} kWh`}
                />
                <Metric
                    icon={<Gem size={16} />}
                    label="Cobalt (AER)"
                    value={`${results.cobaltG} g`}
                    highlight
                />
                <Metric
                    icon={<Droplets size={16} />}
                    label="Water"
                    value={`${results.waterL} L`}
                />
                <Metric
                    icon={<Battery size={16} />}
                    label="Phone Batts"
                    value={`${results.smartphoneBatteryPct}%`}
                />
            </div>

            <div className="text-xs text-gray-500 mt-2 italic">
                *AER (Africa Exploitation Ratio): 74x multiplier applied based on DRC extraction context.
            </div>
        </div>
    );
};

const Metric = ({ icon, label, value, highlight }) => (
    <div className={`p-3 rounded bg-background border border-gray-800 ${highlight ? 'border-primary/50 bg-primary/10' : ''}`}>
        <div className="flex items-center gap-2 text-gray-400 text-xs mb-1">
            {icon} {label}
        </div>
        <div className={`text-lg font-bold ${highlight ? 'text-primary' : 'text-white'}`}>
            {value}
        </div>
    </div>
);

export default BloodTax;
