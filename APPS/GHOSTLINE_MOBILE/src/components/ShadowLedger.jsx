import React, { useState, useEffect } from 'react';
import { analyzeProduct, PRODUCT_LIST } from '../utils/shadowLedger';
import { Ghost, DollarSign, Scale, ArrowRight } from 'lucide-react';

const ShadowLedger = () => {
    const [product, setProduct] = useState('krompir');
    const [quantity, setQuantity] = useState(1);
    const [results, setResults] = useState(null);

    useEffect(() => {
        setResults(analyzeProduct(product, quantity));
    }, [product, quantity]);

    return (
        <div className="card space-y-4">
            <h2 className="text-xl flex items-center gap-2">
                <Ghost className="text-secondary" /> Shadow Ledger
            </h2>

            <select
                value={product}
                onChange={(e) => setProduct(e.target.value)}
                className="w-full bg-background border border-gray-700 rounded p-2 focus:border-primary outline-none capitalize"
            >
                {PRODUCT_LIST.map(p => (
                    <option key={p} value={p}>{p}</option>
                ))}
            </select>

            {results && (
                <div className="space-y-4 pt-2">
                    {/* Ghost Gap Visual */}
                    <div className="bg-background rounded p-3 border border-gray-800">
                        <div className="flex justify-between text-sm mb-2">
                            <span className="text-gray-400">System Price</span>
                            <span className="text-white">€{results.systemAvg}</span>
                        </div>
                        <div className="w-full bg-gray-700 h-2 rounded-full overflow-hidden flex">
                            <div
                                className="bg-primary h-full"
                                style={{ width: `${results.ghostGap}%` }}
                            />
                            <div
                                className="bg-success h-full"
                                style={{ width: `${100 - results.ghostGap}%` }}
                            />
                        </div>
                        <div className="flex justify-between text-xs mt-1">
                            <span className="text-primary font-bold">Ghost Gap: {results.ghostGap}%</span>
                            <span className="text-success">Producer: {100 - results.ghostGap}%</span>
                        </div>
                    </div>

                    {/* Bypass Benefit */}
                    <div className="bg-primary/10 border border-primary/30 rounded p-3">
                        <h3 className="text-sm font-bold text-primary mb-2 flex items-center gap-2">
                            <Scale size={14} /> CSA Bypass Benefit
                        </h3>
                        <div className="grid grid-cols-2 gap-2 text-sm">
                            <div>
                                <span className="block text-gray-500 text-xs">You Save</span>
                                <span className="text-white font-bold">€{results.customerSavings}</span>
                            </div>
                            <div>
                                <span className="block text-gray-500 text-xs">Tone Gains</span>
                                <span className="text-success font-bold">+€{results.toneIncomeIncrease}</span>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ShadowLedger;
