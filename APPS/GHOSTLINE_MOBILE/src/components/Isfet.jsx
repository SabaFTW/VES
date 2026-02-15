import React, { useState, useEffect } from 'react';
import { Activity, Zap, Droplet, ArrowUp, ArrowDown, RefreshCw } from 'lucide-react';

const Isfet = () => {
    const [loading, setLoading] = useState(false);
    const [data, setData] = useState({
        co2: { price: 84.20, trend: 'up', change: '+2.4%' },
        cobalt: { price: 28550, trend: 'down', change: '-1.2%' },
        electricity: { price: 92.50, trend: 'up', change: '+5.1%' },
        timestamp: new Date().toLocaleTimeString()
    });

    const refreshData = () => {
        setLoading(true);
        // Simulate API delay
        setTimeout(() => {
            const randomChange = (base) => base * (1 + (Math.random() * 0.1 - 0.05));
            setData({
                co2: {
                    price: randomChange(84.20),
                    trend: Math.random() > 0.5 ? 'up' : 'down',
                    change: (Math.random() * 5).toFixed(1) + '%'
                },
                cobalt: {
                    price: randomChange(28550),
                    trend: Math.random() > 0.5 ? 'up' : 'down',
                    change: (Math.random() * 5).toFixed(1) + '%'
                },
                electricity: {
                    price: randomChange(92.50),
                    trend: Math.random() > 0.5 ? 'up' : 'down',
                    change: (Math.random() * 5).toFixed(1) + '%'
                },
                timestamp: new Date().toLocaleTimeString()
            });
            setLoading(false);
        }, 1000);
    };

    const isCritical = data.co2.price > 88;

    return (
        <div className="space-y-6 animate-in fade-in duration-500 pb-20">
            {/* Header */}
            <div className={`card border-l-4 ${isCritical ? 'border-red-500' : 'border-cyan-500'} relative overflow-hidden`}>
                <div className="flex justify-between items-start mb-4">
                    <div>
                        <h2 className={`text-xl font-bold mb-1 flex items-center ${isCritical ? 'text-red-400' : 'text-cyan-400'}`}>
                            <Activity className="mr-2" /> ISFET SENSOR
                        </h2>
                        <p className="text-xs text-slate-400 font-mono">market_pulse_monitoring</p>
                    </div>
                    <button
                        onClick={refreshData}
                        className={`p-2 rounded-full bg-slate-800 hover:bg-slate-700 transition-all ${loading ? 'animate-spin' : ''}`}
                    >
                        <RefreshCw size={18} className="text-cyan-400" />
                    </button>
                </div>

                <div className="bg-black/20 rounded p-2 flex justify-between items-center text-xs font-mono text-slate-500">
                    <span>LAST UPDATE</span>
                    <span>{data.timestamp}</span>
                </div>
            </div>

            {/* Metrics Grid */}
            <div className="grid grid-cols-1 gap-4">

                {/* CO2 EUA */}
                <div className="bg-slate-800/50 rounded-xl p-4 border border-slate-700/50 backdrop-blur-sm">
                    <div className="flex justify-between items-start mb-2">
                        <div className="flex items-center text-slate-400 text-sm font-bold">
                            <Zap size={16} className="mr-2 text-yellow-400" />
                            CO₂ EUA (Air Tax)
                        </div>
                        <span className={`text-xs px-2 py-0.5 rounded ${data.co2.trend === 'up' ? 'bg-red-900/30 text-red-400' : 'bg-emerald-900/30 text-emerald-400'
                            }`}>
                            {data.co2.change}
                        </span>
                    </div>
                    <div className="flex items-end justify-between">
                        <div className="text-3xl font-mono font-bold text-white">
                            €{data.co2.price.toFixed(2)}
                            <span className="text-sm text-slate-500 font-normal ml-1">/t</span>
                        </div>
                        {data.co2.trend === 'up' ? <ArrowUp className="text-red-500" /> : <ArrowDown className="text-emerald-500" />}
                    </div>
                </div>

                {/* Cobalt */}
                <div className="bg-slate-800/50 rounded-xl p-4 border border-slate-700/50 backdrop-blur-sm">
                    <div className="flex justify-between items-start mb-2">
                        <div className="flex items-center text-slate-400 text-sm font-bold">
                            <Droplet size={16} className="mr-2 text-red-500" />
                            COBALT (Blood Tax)
                        </div>
                        <span className={`text-xs px-2 py-0.5 rounded ${data.cobalt.trend === 'up' ? 'bg-red-900/30 text-red-400' : 'bg-emerald-900/30 text-emerald-400'
                            }`}>
                            {data.cobalt.change}
                        </span>
                    </div>
                    <div className="flex items-end justify-between">
                        <div className="text-3xl font-mono font-bold text-white">
                            ${data.cobalt.price.toLocaleString()}
                            <span className="text-sm text-slate-500 font-normal ml-1">/t</span>
                        </div>
                        {data.cobalt.trend === 'up' ? <ArrowUp className="text-red-500" /> : <ArrowDown className="text-emerald-500" />}
                    </div>
                </div>

            </div>

            {/* Watchdog Alert */}
            {isCritical && (
                <div className="bg-red-900/20 border border-red-500/30 p-4 rounded-lg animate-pulse">
                    <h3 className="text-red-400 font-bold mb-2 flex items-center">
                        <ArrowUp className="mr-2" /> SATURNIAN INVERSION DETECTED
                    </h3>
                    <p className="text-xs text-red-200/80">
                        CO₂ price spike detected! Extraction rate critical.
                        <br />
                        Tone pays more, Corporations profit more.
                        <br />
                        <strong>ACTION REQUIRED: Verify Blood Tax Ratio.</strong>
                    </p>
                </div>
            )}
        </div>
    );
};

export default Isfet;
