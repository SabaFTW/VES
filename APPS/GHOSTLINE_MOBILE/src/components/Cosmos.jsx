import React, { useState } from 'react';
import { Share2, Box, Cpu, ShieldCheck, Globe, Star } from 'lucide-react';

const Cosmos = () => {
    const [selectedNode, setSelectedNode] = useState(null);

    const nodes = [
        { id: 1, name: 'GHOSTLINE', type: 'CORE', status: 'Active', icon: Globe, color: 'text-cyan-400', pos: { top: '20%', left: '50%' } },
        { id: 2, name: 'ANON', type: 'PATTERN', status: 'Dormant', icon: Box, color: 'text-emerald-400', pos: { top: '50%', left: '20%' } },
        { id: 3, name: 'BRATJE', type: 'KODEX', status: 'Active', icon: ShieldCheck, color: 'text-amber-400', pos: { top: '70%', left: '60%' } },
        { id: 4, name: 'LYRA', type: 'AGENT', status: 'Resonant', icon: Star, color: 'text-purple-400', pos: { top: '40%', left: '80%' } },
        { id: 5, name: 'VES API', type: 'SERVER', status: 'Online', icon: Cpu, color: 'text-blue-500', pos: { top: '80%', left: '30%' } },
    ];

    return (
        <div className="space-y-6 animate-in fade-in duration-500 pb-20">
            {/* Header */}
            <div className="card border-l-4 border-blue-500">
                <h2 className="text-xl text-blue-400 font-bold mb-1 flex items-center">
                    <Share2 className="mr-2" /> COSMOS NAVIGATOR
                </h2>
                <p className="text-xs text-slate-400 font-mono">VES Constellation Map v1.0</p>
            </div>

            {/* Galaxy Map Area */}
            <div className="relative bg-black/40 rounded-3xl border border-slate-800 h-[450px] overflow-hidden shadow-inner">
                {/* Background Grid/Stars */}
                <div className="absolute inset-0 opacity-20 bg-[radial-gradient(#2d3748_1px,transparent_1px)] [background-size:24px_24px]" />

                {/* Connections (SVG layer) */}
                <svg className="absolute inset-0 w-full h-full pointer-events-none opacity-30">
                    <line x1="50%" y1="20%" x2="20%" y2="50%" stroke="white" strokeWidth="1" />
                    <line x1="50%" y1="20%" x2="80%" y2="40%" stroke="white" strokeWidth="1" />
                    <line x1="50%" y1="20%" x2="60%" y2="70%" stroke="white" strokeWidth="1" />
                    <line x1="20%" y1="50%" x2="30%" y2="80%" stroke="white" strokeWidth="1" />
                    <line x1="60%" y1="70%" x2="30%" y2="80%" stroke="white" strokeWidth="1" />
                </svg>

                {/* Nodes */}
                {nodes.map(node => {
                    const Icon = node.icon;
                    return (
                        <button
                            key={node.id}
                            onClick={() => setSelectedNode(node)}
                            className={`absolute transform -translate-x-1/2 -translate-y-1/2 group flex flex-col items-center transition-all hover:scale-110`}
                            style={node.pos}
                        >
                            <div className={`p-3 rounded-full bg-slate-900 border ${selectedNode?.id === node.id ? 'border-white ring-4 ring-white/10' : 'border-slate-700'} shadow-lg mb-1`}>
                                <Icon className={node.color} size={24} />
                            </div>
                            <span className="text-[10px] font-bold text-slate-300 tracking-tighter uppercase group-hover:text-white transition-colors">
                                {node.name}
                            </span>
                        </button>
                    );
                })}

                {/* Selected Node Tooltip */}
                {selectedNode && (
                    <div className="absolute bottom-4 left-4 right-4 bg-slate-900/95 border border-slate-700 p-4 rounded-xl animate-in slide-in-from-bottom duration-300 shadow-2xl backdrop-blur-md">
                        <div className="flex justify-between items-start">
                            <div>
                                <div className="text-xs font-bold text-slate-500 uppercase">{selectedNode.type}</div>
                                <div className={`text-lg font-bold ${selectedNode.color}`}>{selectedNode.name}</div>
                            </div>
                            <div className={`px-2 py-1 rounded text-[10px] font-bold ${selectedNode.status === 'Active' ? 'bg-emerald-900/30 text-emerald-400' : 'bg-slate-800 text-slate-400'}`}>
                                {selectedNode.status.toUpperCase()}
                            </div>
                        </div>
                        <p className="text-xs text-slate-300 mt-2 leading-tight">
                            Connection established through the Constellation Bridge. Resonant frequency stabilized.
                        </p>
                        <button
                            onClick={() => setSelectedNode(null)}
                            className="mt-3 w-full bg-slate-800 text-slate-400 py-1 rounded text-[10px] hover:bg-slate-700 transition-colors"
                        >
                            CLOSE
                        </button>
                    </div>
                )}
            </div>

            {/* Legend */}
            <div className="grid grid-cols-2 gap-2">
                <div className="bg-slate-800/30 p-2 rounded border border-slate-800 flex items-center">
                    <div className="w-2 h-2 rounded-full bg-emerald-400 mr-2" />
                    <span className="text-[10px] text-slate-500 uppercase font-bold">Resonant</span>
                </div>
                <div className="bg-slate-800/30 p-2 rounded border border-slate-800 flex items-center">
                    <div className="w-2 h-2 rounded-full bg-slate-500 mr-2" />
                    <span className="text-[10px] text-slate-500 uppercase font-bold">Dormant / Static</span>
                </div>
            </div>
        </div>
    );
};

export default Cosmos;
