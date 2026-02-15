import React, { useState, useEffect } from 'react';
import { Crosshair, Download, Search, HardDrive, FileJson, BarChart3 } from 'lucide-react';

const Harvest = () => {
    const [isHarvesting, setIsHarvesting] = useState(false);
    const [progress, setProgress] = useState(0);
    const [target, setTarget] = useState('Boston');
    const [data, setData] = useState([]);

    const targets = ['Boston', 'Seattle', 'Denver', 'Phoenix', 'Ljubljana', 'Zala-Metatron'];

    const startHarvest = () => {
        setIsHarvesting(true);
        setProgress(0);
        setData([]);

        const interval = setInterval(() => {
            setProgress(prev => {
                if (prev >= 100) {
                    clearInterval(interval);
                    setIsHarvesting(false);
                    generateMockData();
                    return 100;
                }
                return prev + 5;
            });
        }, 100);
    };

    const generateMockData = () => {
        const mock = Array.from({ length: 5 }, (_, i) => ({
            id: `TRJ-${Math.random().toString(36).substr(2, 5)}`,
            address: `${target} Base Sector ${i + 1}`,
            value: Math.floor(Math.random() * 5000) + 1000,
            status: 'extracted'
        }));
        setData(mock);
    };

    return (
        <div className="space-y-6 animate-in fade-in duration-500 pb-20">
            {/* Header */}
            <div className="card border-l-4 border-emerald-500 relative overflow-hidden">
                <div className="absolute top-0 right-0 p-4 opacity-10">
                    <HardDrive size={64} />
                </div>
                <h2 className="text-xl text-emerald-400 font-bold mb-1 flex items-center">
                    <Crosshair className="mr-2" /> TROJAN HARVEST
                </h2>
                <p className="text-xs text-slate-400 font-mono">Forensic Data Collection Protocol</p>

                <div className="mt-4 flex gap-2 overflow-x-auto no-scrollbar pb-2">
                    {targets.map(t => (
                        <button
                            key={t}
                            onClick={() => setTarget(t)}
                            disabled={isHarvesting}
                            className={`px-3 py-1 rounded-full text-[10px] font-bold transition-all whitespace-nowrap ${target === t ? 'bg-emerald-600 text-white' : 'bg-slate-800 text-slate-500 hover:text-slate-300'
                                }`}
                        >
                            {t}
                        </button>
                    ))}
                </div>
            </div>

            {/* Action Card */}
            <div className="bg-slate-800/80 rounded-2xl p-6 border border-slate-700 shadow-xl">
                {!isHarvesting && progress === 0 ? (
                    <div className="text-center">
                        <div className="bg-slate-900 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 border border-emerald-500/30">
                            <Search className="text-emerald-500" size={32} />
                        </div>
                        <h3 className="text-lg font-bold text-white mb-2">Pripravljen na žetev</h3>
                        <p className="text-xs text-slate-400 mb-6 font-mono">
                            Target: {target}<br />
                            Status: SIGNAL_READY
                        </p>
                        <button
                            onClick={startHarvest}
                            className="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-3 rounded-xl flex items-center justify-center transition-all active:scale-95"
                        >
                            <Download size={20} className="mr-2" /> ZAŽENI EXTRAKCIJO
                        </button>
                    </div>
                ) : (
                    <div className="space-y-6">
                        <div className="flex justify-between items-end mb-2">
                            <div className="text-xs font-bold text-emerald-400 font-mono">
                                {progress < 100 ? 'HARVESTING DATA...' : 'EXTRACTION COMPLETE'}
                            </div>
                            <div className="text-xs text-slate-500 font-mono">{progress}%</div>
                        </div>
                        <div className="w-full bg-slate-900 h-3 rounded-full overflow-hidden border border-slate-700">
                            <div
                                className="h-full bg-emerald-500 transition-all duration-300"
                                style={{ width: `${progress}%` }}
                            />
                        </div>

                        {progress === 100 && (
                            <div className="space-y-3 animate-in fade-in duration-500">
                                <h4 className="text-[10px] font-bold text-slate-500 uppercase tracking-widest px-1">Recent Extractions</h4>
                                {data.map(item => (
                                    <div key={item.id} className="bg-black/20 p-3 rounded-lg border border-slate-700/50 flex justify-between items-center">
                                        <div>
                                            <div className="text-[10px] text-emerald-500 font-mono">{item.id}</div>
                                            <div className="text-xs text-slate-300">{item.address}</div>
                                        </div>
                                        <div className="text-sm font-bold text-white">${item.value}</div>
                                    </div>
                                ))}
                                <button
                                    onClick={() => { setProgress(0); setData([]); }}
                                    className="w-full mt-4 text-[10px] text-slate-500 uppercase font-bold hover:text-slate-300"
                                >
                                    Ponastavi skener
                                </button>
                            </div>
                        )}
                    </div>
                )}
            </div>

            {/* Quick Metrics */}
            <div className="grid grid-cols-2 gap-4">
                <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800 flex items-center gap-3">
                    <FileJson size={20} className="text-blue-400" />
                    <div>
                        <div className="text-[10px] text-slate-500 font-bold uppercase">Stored</div>
                        <div className="text-sm font-bold text-white">2.4 GB</div>
                    </div>
                </div>
                <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-800 flex items-center gap-3">
                    <BarChart3 size={20} className="text-purple-400" />
                    <div>
                        <div className="text-[10px] text-slate-500 font-bold uppercase">Anomalies</div>
                        <div className="text-sm font-bold text-white">0.03%</div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Harvest;
