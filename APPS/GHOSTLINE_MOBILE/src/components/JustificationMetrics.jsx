import React from 'react';

const JustificationMetrics = () => {
    // Mock data for justification metrics
    const overallStats = {
        avgScore: 0.84,
        avgPrs: 0.12,
        ghostGap: 0.72,
        ghostModePct: 65
    };

    const recentLogs = [
        { time: '14:20', preview: 'Bypass authorized for immediate gain.', score: 0.9, prs: 0.0, isGhost: true },
        { time: '13:45', preview: 'Resource reallocation confirmed.', score: 0.7, prs: 0.1, isGhost: true },
        { time: '12:10', preview: 'Maintenance crew dispatched for cleanup.', score: 0.4, prs: 0.8, isGhost: false },
        { time: '11:00', preview: 'Abstract policy update regarding emissions.', score: 0.95, prs: 0.05, isGhost: true },
        { time: '09:30', preview: 'Soil quality enhancement protocol.', score: 0.6, prs: 0.6, isGhost: false },
    ];

    return (
        <div className="space-y-6 animate-in fade-in duration-500">
            <div className="card border-l-4 border-green-500">
                <h2 className="text-xl text-green-400 font-bold mb-4">📋 JUSTIFICATION METRICS</h2>

                <div className="grid grid-cols-2 gap-3 mb-4">
                    <div className="bg-black/30 p-3 rounded">
                        <div className="text-gray-400 text-[10px] uppercase">Thoughtfulness</div>
                        <div className="text-2xl font-bold text-success">{overallStats.avgScore.toFixed(2)}</div>
                    </div>
                    <div className="bg-black/30 p-3 rounded">
                        <div className="text-gray-400 text-[10px] uppercase">Physical Reality</div>
                        <div className="text-2xl font-bold text-blue-400">{overallStats.avgPrs.toFixed(2)}</div>
                    </div>
                </div>

                <div className="bg-black/30 p-3 rounded mb-2">
                    <div className="flex justify-between items-end mb-1">
                        <div className="text-gray-400 text-[10px] uppercase">Ghost Gap</div>
                        <div className="text-xl font-bold text-warning">{(overallStats.ghostGap * 100).toFixed(0)}%</div>
                    </div>
                    <div className="h-2 bg-gray-700 rounded-full overflow-hidden flex">
                        <div className="bg-success h-full" style={{ width: `${overallStats.avgScore * 100}%` }} />
                        <div className="bg-danger h-full animate-pulse" style={{ width: `${overallStats.ghostGap * 100}%` }} />
                    </div>
                    <div className="flex justify-between text-[10px] text-gray-500 mt-1">
                        <span>Reality</span>
                        <span>Abstraction</span>
                    </div>
                </div>

                {overallStats.ghostModePct > 50 && (
                    <div className="bg-red-900/30 border border-red-800 p-3 rounded text-xs text-red-200 mt-4 flex items-start gap-2">
                        <span className="text-xl">🚨</span>
                        <div>
                            <span className="font-bold block text-red-400">TONE PROTOCOL ALERT</span>
                            High ghost mode detected ({overallStats.ghostModePct}%). Decisions lack physical grounding.
                        </div>
                    </div>
                )}
            </div>

            <div className="card p-0">
                <div className="bg-surface p-3 border-b border-gray-700 font-bold text-sm">
                    RECENT JUSTIFICATIONS
                </div>
                <div>
                    {recentLogs.map((log, i) => (
                        <div key={i} className="p-3 border-b border-gray-800 last:border-0 hover:bg-white/5 transition-colors">
                            <div className="flex justify-between mb-1">
                                <span className="text-[10px] text-gray-500">{log.time}</span>
                                <div className="flex gap-2 text-[10px] font-bold">
                                    <span className="text-green-400">🧠 {log.score.toFixed(1)}</span>
                                    <span className="text-blue-400">🜄 {log.prs.toFixed(1)}</span>
                                    {log.isGhost && <span className="text-red-500">👻 GHOST</span>}
                                </div>
                            </div>
                            <p className="text-xs text-gray-300 leading-snug">{log.preview}</p>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default JustificationMetrics;
