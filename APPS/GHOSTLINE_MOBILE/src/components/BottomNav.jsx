import React from 'react';
import { Flame, Activity, DollarSign, Scale, FileText, Shield, Zap, Brain } from 'lucide-react';

const BottomNav = ({ activeTab, setActiveTab }) => {
    const tabs = [
        { id: 'rebis', label: 'REBIS', icon: Flame },
        { id: 'tone', label: 'TONE', icon: Activity },
        { id: 'ledger', label: 'LEDGER', icon: DollarSign },
        { id: 'blood', label: 'BLOOD', icon: Scale },
        { id: 'rattmann', label: 'RATTMANN', icon: Shield },
        { id: 'isfet', label: 'ISFET', icon: Zap },
        { id: 'challenge', label: 'ETHICS', icon: Brain },
        { id: 'just', label: 'JUST', icon: FileText },
    ];

    return (
        <nav className="fixed bottom-0 left-0 right-0 bg-surface border-t border-gray-800 pb-safe z-50 overflow-x-auto no-scrollbar">
            <div className="flex items-center min-w-max px-2">
                {tabs.map((tab) => {
                    const Icon = tab.icon;
                    const isActive = activeTab === tab.id;
                    return (
                        <button
                            key={tab.id}
                            onClick={() => setActiveTab(tab.id)}
                            className={`flex flex-col items-center p-3 min-w-[70px] transition-colors ${isActive ? 'text-primary' : 'text-gray-500 hover:text-gray-300'
                                }`}
                        >
                            <Icon size={20} strokeWidth={isActive ? 2.5 : 2} />
                            <span className="text-[9px] font-bold mt-1 tracking-wider">{tab.label}</span>
                        </button>
                    );
                })}
            </div>
            <div className="h-4 w-full" />
        </nav>
    );
};

export default BottomNav;
