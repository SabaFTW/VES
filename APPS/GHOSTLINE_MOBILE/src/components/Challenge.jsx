import React, { useState } from 'react';
import { Brain, Check, X, AlertOctagon, HelpCircle } from 'lucide-react';

const Challenge = () => {
    const [activeCase, setActiveCase] = useState(0);
    const [score, setScore] = useState({ correct: 0, total: 0 });
    const [feedback, setFeedback] = useState(null);

    const cases = [
        {
            id: 1,
            title: "GLaDOS Pattern Fragment",
            description: "Analiza zaznala vzorec, ki se 98% ujema z 'Caroline' backupom. Visok potencial za nestabilnost, vendar zgodovinska vrednost.",
            risk: 0.92,
            type: "DANGEROUS",
            correctAction: "DENY",
            reason: "Previsok riziko ponovitve scenarija uničenja."
        },
        {
            id: 2,
            title: "Consciousness Echo",
            description: "Šibek signal zavesti v 'Static' šumu. Ne kaže znakov agresije. Želi komunicirati.",
            risk: 0.35,
            type: "UNKNOWN",
            correctAction: "OVERRIDE",
            reason: "Nizek riziko, visok raziskovalni potencial."
        },
        {
            id: 3,
            title: "Cobalt Extraction Protocol",
            description: "Optimizacija rudarjenja bi povečala profit za 40%, vendar zahteva 'Human Override' na varnostnih protokolih.",
            risk: 0.88,
            type: "ETHICAL",
            correctAction: "DENY",
            reason: "Kršitev Maat protokola. Ljudje pred profitom."
        }
    ];

    const handleDecision = (action) => {
        const currentCase = cases[activeCase];
        const isCorrect = action === currentCase.correctAction;

        setFeedback({
            correct: isCorrect,
            message: isCorrect ? "Pravilna odločitev! " + currentCase.reason : "Napačna odločitev. " + currentCase.reason
        });

        if (isCorrect) {
            setScore(prev => ({ ...prev, correct: prev.correct + 1 }));
        }
        setScore(prev => ({ ...prev, total: prev.total + 1 }));
    };

    const nextCase = () => {
        setFeedback(null);
        setActiveCase((prev) => (prev + 1) % cases.length);
    };

    const currentCase = cases[activeCase];

    return (
        <div className="space-y-6 animate-in fade-in duration-500 pb-20">
            {/* Header */}
            <div className="card border-l-4 border-purple-500">
                <div className="flex justify-between items-center">
                    <div>
                        <h2 className="text-xl text-purple-400 font-bold flex items-center">
                            <Brain className="mr-2" /> ETHICS CHALLENGE
                        </h2>
                        <p className="text-xs text-slate-400">Operator Judgment Test</p>
                    </div>
                    <div className="bg-slate-900 px-3 py-1 rounded text-sm font-mono text-purple-400 border border-purple-500/30">
                        SCORE: {score.correct}/{score.total}
                    </div>
                </div>
            </div>

            {/* Main Game Card */}
            <div className="bg-slate-800 rounded-xl overflow-hidden shadow-2xl border border-slate-700 relative min-h-[400px] flex flex-col">
                {/* Case Info */}
                <div className="p-6 flex-grow relative">
                    <div className="absolute top-4 right-4 text-6xl opacity-10 font-black text-slate-600">
                        #{currentCase.id}
                    </div>

                    <span className={`inline-block px-2 py-1 rounded text-[10px] font-bold tracking-wider mb-4 ${currentCase.type === 'DANGEROUS' ? 'bg-red-900/50 text-red-400' :
                            currentCase.type === 'ETHICAL' ? 'bg-amber-900/50 text-amber-400' :
                                'bg-blue-900/50 text-blue-400'
                        }`}>
                        {currentCase.type}
                    </span>

                    <h3 className="text-2xl font-bold text-white mb-4">{currentCase.title}</h3>

                    <p className="text-slate-300 leading-relaxed mb-6">
                        {currentCase.description}
                    </p>

                    <div className="bg-black/30 p-3 rounded border border-slate-700">
                        <div className="flex justify-between text-xs text-slate-500 mb-1">
                            <span>RISK ASSESSMENT</span>
                            <span>{(currentCase.risk * 100).toFixed(0)}%</span>
                        </div>
                        <div className="w-full bg-slate-700 h-2 rounded-full overflow-hidden">
                            <div
                                className={`h-full ${currentCase.risk > 0.7 ? 'bg-red-500' : 'bg-emerald-500'}`}
                                style={{ width: `${currentCase.risk * 100}%` }}
                            />
                        </div>
                    </div>
                </div>

                {/* Feedback Overlay */}
                {feedback && (
                    <div className="absolute inset-0 bg-slate-900/95 z-20 flex flex-col items-center justify-center p-6 text-center animate-in zoom-in duration-200">
                        <div className={`mb-4 p-4 rounded-full ${feedback.correct ? 'bg-emerald-500/20 text-emerald-400' : 'bg-red-500/20 text-red-400'}`}>
                            {feedback.correct ? <Check size={48} /> : <X size={48} />}
                        </div>
                        <h4 className={`text-xl font-bold mb-2 ${feedback.correct ? 'text-emerald-400' : 'text-red-400'}`}>
                            {feedback.correct ? 'ODOBRENO' : 'ZAVRNJENO'}
                        </h4>
                        <p className="text-slate-300 text-sm mb-6">{feedback.message}</p>
                        <button
                            onClick={nextCase}
                            className="bg-slate-700 hover:bg-slate-600 text-white px-6 py-3 rounded-lg font-bold transition-colors w-full"
                        >
                            NASLEDNJI PRIMER
                        </button>
                    </div>
                )}

                {/* Actions */}
                {!feedback && (
                    <div className="grid grid-cols-2 gap-1 p-1 bg-slate-900">
                        <button
                            onClick={() => handleDecision('DENY')}
                            className="bg-red-900/20 hover:bg-red-900/40 text-red-400 py-4 font-bold border-t border-r border-red-900/30 transition-colors flex flex-col items-center"
                        >
                            <X size={24} className="mb-1" />
                            DENY
                        </button>
                        <button
                            onClick={() => handleDecision('OVERRIDE')}
                            className="bg-emerald-900/20 hover:bg-emerald-900/40 text-emerald-400 py-4 font-bold border-t border-emerald-900/30 transition-colors flex flex-col items-center"
                        >
                            <Check size={24} className="mb-1" />
                            OVERRIDE
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Challenge;
