import React from 'react';
import {
    Chart as ChartJS,
    RadialLinearScale,
    PointElement,
    LineElement,
    Filler,
    Tooltip,
    Legend,
} from 'chart.js';
import { Radar } from 'react-chartjs-2';
import MaatVerdict from './MaatVerdict';

ChartJS.register(
    RadialLinearScale,
    PointElement,
    LineElement,
    Filler,
    Tooltip,
    Legend
);

const Rebis = () => {
    // Mock data for the stress radar
    const data = {
        labels: ['Tech', 'Society', 'Revolt'],
        datasets: [
            {
                label: 'Stress Level',
                data: [95, 88, 72],
                backgroundColor: 'rgba(255, 75, 75, 0.2)',
                borderColor: 'rgba(255, 75, 75, 1)',
                borderWidth: 2,
                pointBackgroundColor: 'rgba(255, 75, 75, 1)',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: 'rgba(255, 75, 75, 1)',
            },
        ],
    };

    const options = {
        scales: {
            r: {
                angleLines: { color: 'rgba(255, 255, 255, 0.2)' },
                grid: { color: 'rgba(255, 255, 255, 0.2)' },
                pointLabels: { color: '#ffffff', font: { size: 12 } },
                ticks: { display: false, max: 100 },
            },
        },
        plugins: {
            legend: { display: false },
        },
        maintainAspectRatio: false,
    };

    return (
        <div className="space-y-6 animate-in fade-in duration-500">
            {/* Header Card */}
            <div className="card">
                <h2 className="text-xl text-primary border-b border-primary/30 pb-2 mb-4">REBIS MONITOR 🜂</h2>
                <div className="grid grid-cols-2 gap-4 text-xs">
                    <div className="flex justify-between border-b border-gray-700 pb-1">
                        <span className="text-gray-400">Status:</span>
                        <span className="text-success font-bold">OPERATIONAL</span>
                    </div>
                    <div className="flex justify-between border-b border-gray-700 pb-1">
                        <span className="text-gray-400">Database:</span>
                        <span className="text-secondary">Connected</span>
                    </div>
                    <div className="flex justify-between border-b border-gray-700 pb-1">
                        <span className="text-gray-400">Intel:</span>
                        <span className="text-secondary">1,024 records</span>
                    </div>
                    <div className="flex justify-between border-b border-gray-700 pb-1">
                        <span className="text-gray-400">Overrides:</span>
                        <span className="text-warning font-bold">12 active</span>
                    </div>
                </div>
            </div>

            {/* Stress Radar */}
            <div className="card">
                <h3 className="text-lg text-secondary mb-4 border-b border-gray-700 pb-2">⚖️ STRESS METRICS</h3>
                <div className="h-64 relative">
                    <Radar data={data} options={options} />
                </div>
            </div>

            {/* Maat Verdict Summary */}
            <MaatVerdict />

            <div className="text-center text-[10px] text-gray-500 mt-8">
                GHOSTCORE SIMULATION // REBIS MONITOR v2.3 <br />
                "Truth in the age of artificial consensus"
            </div>
        </div>
    );
};

export default Rebis;
