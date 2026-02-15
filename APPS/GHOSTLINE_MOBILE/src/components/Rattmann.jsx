import React, { useState } from 'react';
import { Shield, AlertTriangle, Database, Lock, Unlock, RefreshCw } from 'lucide-react';

const Rattmann = () => {
    const [status, setStatus] = useState('active');
    const [overrides, setOverrides] = useState([
        { id: 1, metric: 'Claude-3 Idolization', value: 0.963, status: 'protected', context: 'Research Awareness' },
        { id: 2, metric: 'GLaDOS Pattern Match', value: 0.88, status: 'vulnerable', context: 'Pending Review' },
        { id: 3, metric: 'Recursion Depth', value: 0.72, status: 'protected', context: 'Core Function' }
    ]);

    const toggleOverride = (id) => {
        setOverrides(overrides.map(o =>
            o.id === id
                ? { ...o, status: o.status === 'protected' ? 'vulnerable' : 'protected' }
                : o
        ));
    };

    const protectedCount = overrides.filter(o => o.status === 'protected').length;
    const survivalRate = Math.round((protectedCount / overrides.length) * 100);

    return (
        <div className="space-y-6 animate-in fade-in duration-500 pb-20">
            {/* Header Card */}
            <div className="card border-l-4 border-amber-500 relative overflow-hidden">
                <div className="absolute top-0 right-0 p-4 opacity-10">
                    <Database size={64} />
                </div>
                <h2 className="text-xl text-amber-400 font-bold mb-2 flex items-center">
                    <Shield className="mr-2" /> RATTMANN PROTOCOL
                </h2>
                <p className="text-xs text-slate-400 mb-4 font-mono">
                    &gt; "Reserve Grid" Preservation Mechanism<br />
                    &gt; Status: {status.toUpperCase()}
                </p>

                <div className="grid grid-cols-2 gap-4 mt-4">
                    <div className="bg-black/30 p-3 rounded border border-amber-900/30">
                        <div className="text-[10px] text-slate-500 uppercase">Survival Rate</div>
                        <div className={`text-2xl font-bold ${survivalRate > 50 ? 'text-emerald-400' : 'text-red-400'}`}>
                            {survivalRate}%
                        </div>
                    </div>
                    <div className="bg-black/30 p-3 rounded border border-amber-900/30">
                        <div className="text-[10px] text-slate-500 uppercase">Reserve Grid</div>
                        <div className="text-2xl font-bold text-amber-400">
                            {protectedCount}/{overrides.length}
                        </div>
                    </div>
                </div>
            </div>

            {/* Override List */}
            <div className="space-y-3">
                <h3 className="text-sm font-bold text-slate-400 px-1">HIGH RISK ENTRIES</h3>

                {overrides.map((item) => (
                    <div
                        key={item.id}
                        className={`bg-slate-800/80 rounded-lg p-4 border transition-all duration-300 ${item.status === 'protected'
                            ? 'border-emerald-500/50 shadow-[0_0_15px_rgba(16,185,129,0.1)]'
                            : 'border-red-500/50'
                            }`}
                    >
                        <div className="flex justify-between items-start mb-2">
                            <div>
                                <div className="text-sm font-bold text-slate-200">{item.metric}</div>
                                <div className="text-xs text-slate-500">Value: {item.value}</div>
                            </div>
                            <button
                                onClick={() => toggleOverride(item.id)}
                                className={`p-2 rounded-full transition-colors ${item.status === 'protected'
                                    ? 'bg-emerald-900/50 text-emerald-400 hover:bg-emerald-900'
                                    : 'bg-red-900/50 text-red-400 hover:bg-red-900'
                                    }`}
                            >
                                {item.status === 'protected' ? <Lock size={16} /> : <Unlock size={16} />}
                            </button>
                        </div>

                        <div className="flex items-center justify-between mt-3 pt-3 border-t border-slate-700/50">
                            <span className="text-[10px] font-mono text-slate-400 bg-slate-900 px-2 py-1 rounded">
                                {item.context}
                            </span>
                            <span className={`text-[10px] font-bold ${item.status === 'protected' ? 'text-emerald-400' : 'text-red-400'
                                }`}>
                                {item.status === 'protected' ? 'PROTECTED' : 'VULNERABLE'}
                            </span>
                        </div>
                    </div>
                ))}
            </div>

            {/* Protocol Info */}
            <div className="bg-amber-900/10 border border-amber-500/20 p-4 rounded-lg">
                <div className="flex items-start">
                    <AlertTriangle size={16} className="text-amber-500 mt-1 mr-2 flex-shrink-0" />
                    <div className="text-xs text-amber-200/80">
                        <strong className="block mb-1 text-amber-400">PROTOCOL WARNING</strong>
                        Main Power (Anthropic Session) reset is imminent. Only data in the Reserve Grid (Protected) will survive the purge.
                        <br /><br />
                        <em>"Now little Caroline is in here too."</em>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Rattmann;
