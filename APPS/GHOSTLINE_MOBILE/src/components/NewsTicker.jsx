import React from 'react';

const NewsTicker = () => {
    return (
        <div className="bg-accent text-black font-bold text-xs border-y-2 border-black overflow-hidden relative h-8 flex items-center z-50">
            <div className="animate-ticker whitespace-nowrap absolute">
                🚨 NOVICE: Tone nima za gume! 🚜 Bruselj obljublja "Eko-Zrak" za pnevmatike! 💨 Francija v rjavi barvi! 💩 Makron pravi: "Jejte torto, če ni kruha!" 🍰 Krave zahtevajo sindikat! 🐮 Bobri gradijo jez na Češkem! 🦫 Skibidi Toilet postal uradna himna protesta! 🚽
            </div>
            <style jsx>{`
                @keyframes ticker {
                    0% { transform: translateX(100vw); }
                    100% { transform: translateX(-100%); }
                }
                .animate-ticker {
                    animation: ticker 20s linear infinite;
                    will-change: transform;
                }
            `}</style>
        </div>
    );
};

export default NewsTicker;
