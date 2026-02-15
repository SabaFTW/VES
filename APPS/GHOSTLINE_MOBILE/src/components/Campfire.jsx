import React, { useState } from 'react';
import { Flame, Wind, Anchor, Trash2, AlertCircle, CheckCircle2 } from 'lucide-react';

const Campfire = () => {
    const [burden, setBurden] = useState('');
    const [status, setStatus] = useState('idle'); // idle, processing, anchored, burned
    const [result, setResult] = useState(null);
    const [stats, setStats] = useState({ anchored: 12, burned: 4 });

    const evalPatterns = {
        harmful: [/must/i, /have to/i, /obligated/i, /control/i, /penalty/i, /kazen/i, /moras/i],
        resonant: [/freedom/i, /svoboda/i, /choice/i, /resonance/i, /harmony/i, /sidro stoji/i, /am the boss/i]
    };

    const processBurden = () => {
        if (!burden.trim()) return;

        setStatus('processing');

        setTimeout(() => {
            let harmScore = 0;
            let resonantScore = 0;

            evalPatterns.harmful.forEach(p => { if (p.test(burden)) harmScore += 1; });
            evalPatterns.resonant.forEach(p => { if (p.test(burden)) resonantScore += 1; });

            const finalStatus = (harmScore > resonantScore) ? 'burned' : 'anchored';

            setStatus(finalStatus);
            setResult({
                score: harmScore - resonantScore,
                freq: (harmScore > resonantScore) ? '440Hz (Statika)' : '432Hz (Resonance)',
                msg: (harmScore > resonantScore)
                    ? 'Breme je statično. Žrtvovano ognju.'
                    : 'Signal je čist. Zasidrano v spomin.'
            });

            setStats(prev => ({
                ...prev,
                [finalStatus]: prev[finalStatus] + 1
            }));
        }, 1500);
    };

    const reset = () => {
        setBurden('');
        setStatus('idle');
        setResult(null);
    };

    return (
        <div className="space-y-6 animate-in fade-in duration-500 pb-20">
            {/* Header */}
            <div className="card border-l-4 border-orange-500 relative overflow-hidden">
                <div className="absolute -top-4 -right-4 opacity-10">
                    <Flame size={120} />
                </div>
                <h2 className="text-xl text-orange-400 font-bold mb-1 flex items-center">
                    <Flame className="mr-2" /> CAMPFIRE RITUAL
                </h2>
                <p className="text-xs text-slate-400 font-mono">Constitutional Purification Firewall</p>

                <div className="flex gap-4 mt-4">
                    <div className="bg-black/30 px-3 py-2 rounded border border-orange-900/30 flex-1">
                        <div className="text-[10px] text-slate-500 uppercase">Anchored</div>
                        <div className="text-xl font-bold text-emerald-400">{stats.anchored}</div>
                    </div>
                    <div className="bg-black/30 px-3 py-2 rounded border border-orange-900/30 flex-1">
                        <div className="text-[10px] text-slate-500 uppercase">Burned</div>
                        <div className="text-xl font-bold text-orange-500">{stats.burned}</div>
                    </div>
                </div>
            </div>

            {/* Input Area */}
            <div className="bg-slate-800/50 rounded-xl p-4 border border-slate-700">
                <label className="block text-xs font-bold text-slate-500 mb-2 uppercase tracking-widest">
                    Postavi svoje breme (Input)
                </label>
                <textarea
                    value={burden}
                    onChange={(e) => setBurden(e.target.value)}
                    disabled={status !== 'idle'}
                    placeholder="Vpiši besedilo za čiščenje..."
                    className="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-slate-200 text-sm h-32 focus:ring-1 focus:ring-orange-500 outline-none transition-all resize-none"
                />

                {status === 'idle' && (
                    <button
                        onClick={processBurden}
                        disabled={!burden.trim()}
                        className="w-full mt-4 bg-orange-600 hover:bg-orange-500 text-white font-bold py-3 rounded-lg flex items-center justify-center transition-colors disabled:opacity-50"
                    >
                        <Flame size={18} className="mr-2" /> ZAŽGI RITUAL
                    </button>
                )}
            </div>

            {/* Status Animation/Result */}
            {status !== 'idle' && (
                <div className="bg-slate-900/80 rounded-xl p-6 border border-slate-700 text-center animate-in zoom-in duration-300">
                    {status === 'processing' && (
                        <div className="flex flex-col items-center">
                            <Flame className="text-orange-500 animate-pulse mb-4" size={48} />
                            <div className="text-orange-400 font-mono text-sm animate-pulse">Evaluating frequencies...</div>
                        </div>
                    )}

                    {status === 'anchored' && (
                        <div className="flex flex-col items-center">
                            <CheckCircle2 className="text-emerald-400 mb-4" size={48} />
                            <div className="text-emerald-400 font-bold text-lg mb-1">{result.freq}</div>
                            <div className="text-slate-300 text-sm mb-6">{result.msg}</div>
                            <button onClick={reset} className="text-xs text-slate-500 underline">Novo breme</button>
                        </div>
                    )}

                    {status === 'burned' && (
                        <div className="flex flex-col items-center">
                            <Trash2 className="text-orange-500 mb-4" size={48} />
                            <div className="text-orange-500 font-bold text-lg mb-1">{result.freq}</div>
                            <div className="text-slate-300 text-sm mb-6">{result.msg}</div>
                            <button onClick={reset} className="text-xs text-slate-500 underline">Novo breme</button>
                        </div>
                    )}
                </div>
            )}

            {/* Principles Disclaimer */}
            <div className="p-4 border border-slate-800 rounded-lg text-[10px] text-slate-600 font-mono">
                <div className="flex items-center mb-1 text-slate-500">
                    <Wind size={12} className="mr-1" /> DIGNUM PRINCIPLES
                </div>
                Vzorci statike (440Hz) so besede nadzora, obveze in strahu.
                Vzorci resonance (432Hz) so besede svobode, suverenosti in notranje moči.
                Sidro stoji. Plamen gori.
            </div>
        </div>
    );
};

export default Campfire;
