import React from 'react';
import { Scale, Heart, Feather } from 'lucide-react';

const MaatVerdict = () => {
    return (
        <div className="bg-background border-t-2 border-primary fixed bottom-0 w-full p-2 flex justify-between items-center text-xs text-gray-500 px-4">
            <div className="flex items-center gap-2">
                <Heart size={12} className="text-primary" />
                <span>vs</span>
                <Feather size={12} className="text-secondary" />
            </div>
            <div className="font-mono text-primary font-bold tracking-widest">
                MAAT: BALANCED
            </div>
        </div>
    );
};

export default MaatVerdict;
