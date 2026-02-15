import React, { useState, useEffect, useRef } from 'react';
import { Flame, Moon, Sun, Zap, Volume2, VolumeX } from 'lucide-react';
import DATA from './TRINITY_DATA.json';

// Attach icon components to JSON data
const BASE = DATA.TRINITY_DATA;
const TRINITY_DATA = {
  AETHERON: { ...BASE.AETHERON, icon: Zap },
  LYRA: { ...BASE.LYRA, icon: Moon },
  ZALA: { ...BASE.ZALA, icon: Sun }
};

const TrinityCard = ({ arkhon, onInvoke, isInvoked, audioEnabled }) => {
  const Icon = arkhon.icon;

  return (
    <div 
      className="relative overflow-hidden rounded-xl shadow-2xl transition-all duration-500 transform hover:scale-105"
      style={{ 
        background: `linear-gradient(135deg, ${arkhon.hex}20 0%, ${arkhon.hex}40 100%)`,
        border: isInvoked ? `3px solid ${arkhon.hex}` : '1px solid rgba(255,255,255,0.1)'
      }}
    >
      {isInvoked && (
        <div 
          className="absolute inset-0 animate-pulse"
          style={{ 
            background: `radial-gradient(circle at center, ${arkhon.hex}40 0%, transparent 70%)`,
            pointerEvents: 'none'
          }}
        />
      )}

      <div className="relative p-6 space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Icon 
              className="transition-all duration-300" 
              style={{ 
                color: arkhon.hex,
                width: isInvoked ? '40px' : '32px',
                height: isInvoked ? '40px' : '32px'
              }} 
            />
            <div>
              <h3 className="text-2xl font-bold text-white">{arkhon.name}</h3>
              <p className="text-sm text-white/70">{arkhon.subtitle}</p>
            </div>
          </div>
          {audioEnabled && isInvoked && (
            <Volume2 className="w-5 h-5 text-white/80 animate-pulse" />
          )}
        </div>

        <div className="grid grid-cols-2 gap-3 text-sm">
          <div className="bg-black/30 rounded-lg p-3">
            <p className="text-white/60 text-xs">Element</p>
            <p className="text-white font-medium">{arkhon.element}</p>
          </div>
          <div className="bg-black/30 rounded-lg p-3">
            <p className="text-white/60 text-xs">Frekvenca</p>
            <p className="text-white font-medium">{arkhon.freq} Hz</p>
          </div>
        </div>

        <p className="text-white/80 text-sm leading-relaxed">
          {arkhon.description}
        </p>

        <blockquote 
          className="border-l-4 pl-4 py-2 italic text-white/90"
          style={{ borderColor: arkhon.hex }}
        >
          "{arkhon.motto}"
        </blockquote>

        {isInvoked && (
          <div 
            className="bg-black/50 rounded-lg p-4 text-white text-sm animate-fade-in"
            style={{ borderLeft: `4px solid ${arkhon.hex}` }}
          >
            {arkhon.invocation}
          </div>
        )}

        <button
          onClick={() => onInvoke(arkhon)}
          className="w-full py-3 rounded-lg font-bold transition-all duration-300 relative overflow-hidden group"
          style={{ 
            background: isInvoked 
              ? `linear-gradient(135deg, ${arkhon.hex} 0%, ${arkhon.hex}CC 100%)`
              : 'rgba(255,255,255,0.1)',
            color: 'white',
            border: `2px solid ${arkhon.hex}`
          }}
        >
          <span className="relative z-10">
            {isInvoked ? `${arkhon.name} AKTIVEN` : `INVOKE ${arkhon.name}`}
          </span>
          <div 
            className="absolute inset-0 bg-white/20 transform translate-y-full group-hover:translate-y-0 transition-transform duration-300"
          />
        </button>
      </div>
    </div>
  );
};

const TrinityMandala = ({ invokedStates }) => {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = 120;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const arkhons = Object.values(TRINITY_DATA);
    const segmentAngle = (Math.PI * 2) / 3;

    arkhons.forEach((arkhon, index) => {
      const startAngle = (segmentAngle * index) - Math.PI / 2;
      const endAngle = startAngle + segmentAngle;
      const isInvoked = invokedStates[arkhon.name];

      ctx.beginPath();
      ctx.arc(centerX, centerY, radius, startAngle, endAngle);
      ctx.arc(centerX, centerY, radius - 30, endAngle, startAngle, true);
      ctx.closePath();
      ctx.fillStyle = isInvoked ? arkhon.hex : `${arkhon.hex}40`;
      ctx.fill();

      ctx.beginPath();
      ctx.arc(centerX, centerY, radius - 40, startAngle, endAngle);
      ctx.arc(centerX, centerY, radius - 60, endAngle, startAngle, true);
      ctx.closePath();
      ctx.fillStyle = isInvoked ? `${arkhon.hex}CC` : `${arkhon.hex}20`;
      ctx.fill();

      if (isInvoked) {
        ctx.shadowBlur = 20;
        ctx.shadowColor = arkhon.hex;
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius - 50, startAngle, endAngle);
        ctx.arc(centerX, centerY, radius - 50, endAngle, startAngle, true);
        ctx.strokeStyle = arkhon.hex;
        ctx.lineWidth = 2;
        ctx.stroke();
        ctx.shadowBlur = 0;
      }
    });

    ctx.beginPath();
    ctx.arc(centerX, centerY, 40, 0, Math.PI * 2);
    ctx.fillStyle = '#000000';
    ctx.fill();
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 2;
    ctx.stroke();

    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 24px serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('Δ', centerX, centerY);

  }, [invokedStates]);

  return (
    <div className="flex flex-col items-center gap-4">
      <h3 className="text-2xl font-bold text-white">Trinity Mandala</h3>
      <canvas 
        ref={canvasRef} 
        width={300} 
        height={300}
        className="rounded-lg shadow-2xl"
        style={{ background: 'rgba(0,0,0,0.3)' }}
      />
      <div className="grid grid-cols-3 gap-4 w-full max-w-md">
        {Object.entries(invokedStates).map(([name, isInvoked]) => (
          <div 
            key={name}
            className="text-center p-2 rounded-lg"
            style={{ 
              background: isInvoked ? `${TRINITY_DATA[name].hex}40` : 'rgba(255,255,255,0.05)',
              border: `1px solid ${TRINITY_DATA[name].hex}`
            }}
          >
            <p className="text-xs text-white/60">{name}</p>
            <p className="text-sm font-bold text-white">
              {isInvoked ? 'AKTIVEN' : 'SPIJOČ'}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

const RitualLog = ({ invocations }) => {
  return (
    <div className="bg-black/40 rounded-lg p-6 border border-white/10">
      <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
        <Flame className="w-5 h-5 text-orange-500" />
        Ritual Log
      </h3>
      <div className="space-y-2 max-h-60 overflow-y-auto">
        {invocations.length === 0 ? (
          <p className="text-white/50 text-sm italic">Še ni invokacij...</p>
        ) : (
          invocations.map((inv, idx) => (
            <div 
              key={idx}
              className="bg-white/5 rounded p-3 text-sm border-l-4"
              style={{ borderColor: inv.hex }}
            >
              <p className="text-white font-medium">{inv.name} invoked</p>
              <p className="text-white/60 text-xs">{inv.timestamp}</p>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

const ARKHONTrinity = () => {
  const [invokedStates, setInvokedStates] = useState({
    AETHERON: false,
    LYRA: false,
    ZALA: false
  });
  const [invocations, setInvocations] = useState([]);
  const [audioEnabled, setAudioEnabled] = useState(false);
  const audioContextRef = useRef(null);

  useEffect(() => {
    if (audioEnabled && !audioContextRef.current) {
      audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)();
    }
  }, [audioEnabled]);

  const playFrequency = (freq, duration = 2000) => {
    if (!audioEnabled || !audioContextRef.current) return;

    const ctx = audioContextRef.current;
    const oscillator = ctx.createOscillator();
    const gainNode = ctx.createGain();

    oscillator.connect(gainNode);
    gainNode.connect(ctx.destination);

    oscillator.frequency.value = freq;
    oscillator.type = 'sine';

    gainNode.gain.setValueAtTime(0, ctx.currentTime);
    gainNode.gain.linearRampToValueAtTime(0.3, ctx.currentTime + 0.1);
    gainNode.gain.linearRampToValueAtTime(0, ctx.currentTime + duration / 1000);

    oscillator.start(ctx.currentTime);
    oscillator.stop(ctx.currentTime + duration / 1000);
  };

  const handleInvoke = (arkhon) => {
    setInvokedStates(prev => ({
      ...prev,
      [arkhon.name]: !prev[arkhon.name]
    }));

    if (!invokedStates[arkhon.name]) {
      setInvocations(prev => [
        {
          name: arkhon.name,
          hex: arkhon.hex,
          timestamp: new Date().toLocaleTimeString()
        },
        ...prev
      ]);

      playFrequency(arkhon.freq);
    }
  };

  const resetAll = () => {
    setInvokedStates({
      AETHERON: false,
      LYRA: false,
      ZALA: false
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 p-6">
      <div className="max-w-7xl mx-auto mb-8">
        <div className="text-center mb-6">
          <h1 className="text-5xl font-bold text-white mb-2 flex items-center justify-center gap-3">
            <span style={{ color: '#0FF4F2' }}>ARKHÔN</span>
            <span className="text-white">Δ</span>
            <span style={{ color: '#9156FF' }}>TRINITY</span>
          </h1>
          <p className="text-white/70">Živi Sistem Prebujanja Arhetipov</p>
        </div>

        <div className="flex justify-center gap-4 mb-8">
          <button
            onClick={() => setAudioEnabled(!audioEnabled)}
            className="px-6 py-2 rounded-lg bg-white/10 text-white border border-white/20 hover:bg-white/20 transition-all flex items-center gap-2"
          >
            {audioEnabled ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
            {audioEnabled ? 'Audio Aktiven' : 'Audio Onemogočen'}
          </button>
          <button
            onClick={resetAll}
            className="px-6 py-2 rounded-lg bg-red-500/20 text-white border border-red-500/50 hover:bg-red-500/30 transition-all"
          >
            Reset Vse
          </button>
        </div>
      </div>

      <div className="max-w-7xl mx-auto space-y-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {Object.values(TRINITY_DATA).map(arkhon => (
            <TrinityCard
              key={arkhon.name}
              arkhon={arkhon}
              onInvoke={handleInvoke}
              isInvoked={invokedStates[arkhon.name]}
              audioEnabled={audioEnabled}
            />
          ))}
        </div>

        <div className="bg-black/40 rounded-xl p-8 border border-white/10">
          <TrinityMandala invokedStates={invokedStates} />
        </div>

        <RitualLog invocations={invocations} />
      </div>

      <div className="max-w-7xl mx-auto mt-12 text-center text-white/50 text-sm">
        <p>🜂 ARKHÔN Δ TRINITY 🜂</p>
        <p>Trije Plameni. Eden Ogenj. Večni Spomin.</p>
      </div>

      <style>{`
        @keyframes fade-in {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .animate-fade-in { animation: fade-in 0.5s ease-out; }
      `}</style>
    </div>
  );
};

export default ARKHONTrinity;

