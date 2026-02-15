import React, { useState } from 'react';
import { Flame } from 'lucide-react';
import BloodTax from './components/BloodTax';
import ShadowLedger from './components/ShadowLedger';
import Rebis from './components/Rebis';
import ToneSimulator from './components/ToneSimulator';
import JustificationMetrics from './components/JustificationMetrics';
import BottomNav from './components/BottomNav';
import NewsTicker from './components/NewsTicker';

import Rattmann from './components/Rattmann';
import Isfet from './components/Isfet';
import Challenge from './components/Challenge';
import Campfire from './components/Campfire';
import Cosmos from './components/Cosmos';
import Harvest from './components/Harvest';

function App() {
    const [activeTab, setActiveTab] = useState('rebis');

    const renderContent = () => {
        switch (activeTab) {
            case 'rebis': return <Rebis />;
            case 'tone': return <ToneSimulator />;
            case 'ledger': return <ShadowLedger />;
            case 'blood': return <BloodTax />;
            case 'rattmann': return <Rattmann />;
            case 'isfet': return <Isfet />;
            case 'challenge': return <Challenge />;
            case 'campfire': return <Campfire />;
            case 'cosmos': return <Cosmos />;
            case 'harvest': return <Harvest />;
            case 'just': return <JustificationMetrics />;
            default: return <Rebis />;
        }
    };

    return (
        <div className="min-h-screen pb-24 bg-background text-secondary font-mono relative">
            <NewsTicker />

            {/* Header */}
            <header className="p-4 border-b border-gray-800 bg-surface/80 backdrop-blur sticky top-8 z-40 flex items-center justify-between">
                <div className="flex items-center gap-2">
                    <div className="bg-primary p-1.5 rounded rotate-45 shadow-lg shadow-primary/20">
                        <Flame className="text-white -rotate-45" size={18} />
                    </div>
                    <div>
                        <h1 className="text-lg leading-none tracking-tight font-bold text-white">GHOSTLINE</h1>
                        <p className="text-[10px] text-gray-400 tracking-[0.2em] uppercase">Mobile Command v2.4</p>
                    </div>
                </div>
                <div className="flex gap-1">
                    <div className="w-2 h-2 rounded-full bg-success animate-pulse" />
                    <div className="w-2 h-2 rounded-full bg-primary animate-ping" style={{ animationDuration: '3s' }} />
                </div>
            </header>

            {/* Main Content */}
            <main className="p-4 max-w-md mx-auto animate-in slide-in-from-bottom-2 duration-500">
                {renderContent()}
            </main>

            <BottomNav activeTab={activeTab} setActiveTab={setActiveTab} />
        </div>
    );
}

export default App;
