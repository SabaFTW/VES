import React, { useState, useEffect } from 'react';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Doughnut } from 'react-chartjs-2';
import { Trash2, RefreshCw, AlertTriangle } from 'lucide-react';

ChartJS.register(ArcElement, Tooltip, Legend);

const ToneSimulator = () => {
    const [state, setState] = useState({
        poopLevel: 45,
        absorption: 60,
        overflowRisk: 12,
        money: 12500.00
    });

    const [events, setEvents] = useState([
        { time: '10:42', msg: 'System stable', type: 'info' }
    ]);

    // Mock live data updates
    useEffect(() => {
        const interval = setInterval(() => {
            setState(prev => {
                const newPoop = Math.min(100, Math.max(0, prev.poopLevel + (Math.random() - 0.4) * 5));
                return {
                    ...prev,
                    poopLevel: newPoop,
                    overflowRisk: newPoop > prev.absorption ? (newPoop - prev.absorption) * 2 : 0,
                    money: prev.money + (Math.random() * 100)
                };
            });
        }, 2000);
        return () => clearInterval(interval);
    }, []);

    // Check for overflow events
    useEffect(() => {
        if (state.overflowRisk > 50) {
            addEvent('⚠️ HIGH OVERFLOW RISK!', 'warning');
        }
    }, [state.overflowRisk]);

    const addEvent = (msg, type = 'info') => {
        setEvents(prev => [{ time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }), msg, type }, ...prev].slice(0, 10));
    };

    const handleFlush = () => {
        setState(prev => ({ ...prev, poopLevel: Math.max(0, prev.poopLevel - 30) }));
        addEvent('🚜 Manual flush initiated', 'success');
    };

    const handleProcess = () => {
        setState(prev => ({ ...prev, money: prev.money - 500, absorption: Math.min(100, prev.absorption + 10) }));
        addEvent('💸 EU Funds invested in absorption', 'info');
    };

    const chartData = {
        labels: ['Poop Level', 'Absorption Capacity', 'Buffer'],
        datasets: [
            {
                data: [state.poopLevel, Math.max(0, state.absorption - state.poopLevel), Math.max(0, 100 - state.absorption)],
                backgroundColor: ['#8B4513', '#22c55e', '#64748b'],
                borderWidth: 0,
            },
        ],
    };

    return (
        <div className="space-y-6 animate-in fade-in duration-500">
            <div className="card border-l-4 border-accent">
                <h2 className="text-xl text-accent font-bold mb-4">🚜 TONE SIMULATOR</h2>

                <div className="grid grid-cols-2 gap-4 mb-6">
                    <div className="aspect-square relative flex items-center justify-center">
                        <Doughnut
                            data={chartData}
                            options={{ cutout: '70%', plugins: { legend: { display: false } } }}
                        />
                        <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                            <span className="text-2xl font-bold text-white">{state.poopLevel.toFixed(0)}%</span>
                            <span className="text-[10px] text-gray-400">SATURATION</span>
                        </div>
                    </div>

                    <div className="space-y-3 flex flex-col justify-center text-xs">
                        <div>
                            <div className="flex justify-between mb-1">
                                <span className="text-gray-400">Overflow Risk</span>
                                <span className={state.overflowRisk > 50 ? 'text-danger font-bold' : 'text-success'}>
                                    {state.overflowRisk.toFixed(1)}%
                                </span>
                            </div>
                            <div className="h-1.5 w-full bg-gray-700 rounded-full overflow-hidden">
                                <div className="h-full bg-danger transition-all duration-500" style={{ width: `${state.overflowRisk}%` }} />
                            </div>
                        </div>

                        <div>
                            <div className="flex justify-between mb-1">
                                <span className="text-gray-400">EU Funds</span>
                                <span className="text-accent">€{state.money.toFixed(2)}</span>
                            </div>
                        </div>

                        <div className="pt-2">
                            {state.overflowRisk > 80 ? (
                                <div className="bg-danger/20 text-danger p-2 rounded flex items-center gap-2 animate-pulse">
                                    <AlertTriangle size={16} />
                                    <span>CRITICAL LEVEL</span>
                                </div>
                            ) : (
                                <div className="bg-success/20 text-success p-2 rounded flex items-center gap-2">
                                    <Activity size={16} />
                                    <span>SYSTEM STABLE</span>
                                </div>
                            )}
                        </div>
                    </div>
                </div>

                <div className="grid grid-cols-2 gap-3">
                    <button onClick={handleFlush} className="bg-primary hover:bg-red-600 text-white p-3 rounded-lg font-bold flex items-center justify-center gap-2 active:scale-95 transition-transform">
                        <Trash2 size={18} /> FLUSH
                    </button>
                    <button onClick={handleProcess} className="bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-lg font-bold flex items-center justify-center gap-2 active:scale-95 transition-transform">
                        <RefreshCw size={18} /> INVEST
                    </button>
                </div>
            </div>

            <div className="card p-0 overflow-hidden">
                <div className="bg-surface p-3 border-b border-gray-700 font-bold text-sm flex justify-between items-center">
                    <span>EVENT FEED</span>
                    <span className="text-[10px] bg-primary px-1.5 py-0.5 rounded text-white">LIVE</span>
                </div>
                <div className="max-h-48 overflow-y-auto p-3 space-y-2 font-mono text-xs">
                    {events.map((e, i) => (
                        <div key={i} className={`flex gap-3 pb-2 border-b border-gray-800 last:border-0 ${i === 0 ? 'animate-pulse' : 'opacity-70'}`}>
                            <span className="text-gray-500">{e.time}</span>
                            <span className={e.type === 'warning' ? 'text-danger font-bold' : e.type === 'success' ? 'text-success' : 'text-gray-300'}>
                                {e.msg}
                            </span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default ToneSimulator;
