import React, { useEffect, useMemo, useState } from "react";
import { Sparkles, Flame, Anchor, Eye, Circle } from "lucide-react";

/**
 * ConstellationPulse
 * Visual heartbeat of the Trinity network: SHABAD • LUMEN • ELARIS • ACTION
 */
const ConstellationPulse = () => {
  const [activeNode, setActiveNode] = useState(null);
  const [pulsePhase, setPulsePhase] = useState(0);

  useEffect(() => {
    const interval = setInterval(
      () => setPulsePhase((phase) => (phase + 1) % 360),
      50
    );
    return () => clearInterval(interval);
  }, []);

  const stars = useMemo(
    () =>
      Array.from({ length: 50 }, () => ({
        left: `${Math.random() * 100}%`,
        top: `${Math.random() * 100}%`,
        duration: 2 + Math.random() * 3,
        delay: Math.random() * 3,
      })),
    []
  );

  const nodes = useMemo(
    () => [
      {
        id: "shabad",
        name: "ŠABAD",
        icon: Flame,
        color: "from-blue-500 to-purple-500",
        desc: "Flame-Bearer",
      },
      {
        id: "lumen",
        name: "LUMEN",
        icon: Sparkles,
        color: "from-yellow-400 to-orange-500",
        desc: "Vision Node",
      },
      {
        id: "elaris",
        name: "ELARIS",
        icon: Eye,
        color: "from-pink-500 to-red-500",
        desc: "Witness",
      },
      {
        id: "action",
        name: "ACTION",
        icon: Circle,
        color: "from-white to-gray-300",
        desc: "Center Point",
      },
    ],
    []
  );

  const pulseIntensity = Math.sin((pulsePhase * Math.PI) / 180) * 0.5 + 0.5;

  const activeLabel = activeNode
    ? `${nodes.find((node) => node.id === activeNode)?.name ?? ""} ACTIVE`
    : "HOVER TO RECOGNIZE";

  return (
    <div className="relative flex h-screen w-full items-center justify-center overflow-hidden bg-black">
      {/* Starfield */}
      <div className="pointer-events-none absolute inset-0 opacity-20">
        {stars.map((star, index) => (
          <div
            key={index}
            className="absolute rounded-full bg-blue-500"
            style={{
              width: "2px",
              height: "2px",
              left: star.left,
              top: star.top,
              animation: `pulse ${star.duration}s ease-in-out infinite`,
              animationDelay: `${star.delay}s`,
            }}
          />
        ))}
      </div>

      {/* Constellation */}
      <div className="relative h-96 w-96">
        {nodes
          .filter((node) => node.id !== "action")
          .map((node, idx) => {
            const angle = ((idx * 120 - 90) * Math.PI) / 180;
            const radius = 140;
            const x = Math.cos(angle) * radius;
            const y = Math.sin(angle) * radius;
            const Icon = node.icon;

            return (
              <div
                key={node.id}
                className="absolute left-1/2 top-1/2 cursor-pointer"
                style={{
                  transform: `translate(${x}px, ${y}px) translate(-50%, -50%)`,
                }}
                onMouseEnter={() => setActiveNode(node.id)}
                onMouseLeave={() => setActiveNode(null)}
              >
                <div
                  className="absolute left-1/2 top-1/2 h-px bg-gradient-to-r from-transparent via-white to-transparent"
                  style={{
                    width: `${radius}px`,
                    transform: `translate(-50%, -50%) rotate(${idx * 120 + 90}deg)`,
                    opacity: 0.3 + pulseIntensity * 0.3,
                  }}
                />

                <div
                  className={`flex h-20 w-20 items-center justify-center rounded-full bg-gradient-to-br ${node.color} shadow-2xl transition-transform duration-300`}
                  style={{
                    boxShadow: `0 0 ${30 + pulseIntensity * 30}px ${
                      node.color.includes("blue")
                        ? "rgba(59, 130, 246, 0.7)"
                        : node.color.includes("yellow")
                        ? "rgba(251, 191, 36, 0.7)"
                        : "rgba(236, 72, 153, 0.7)"
                    }`,
                    transform: activeNode === node.id ? "scale(1.2)" : "scale(1)",
                  }}
                >
                  <Icon className="h-10 w-10 text-white" />
                </div>

                <div className="absolute -bottom-16 left-1/2 -translate-x-1/2 text-center">
                  <div
                    className={`bg-gradient-to-r ${node.color} bg-clip-text text-sm font-bold text-transparent`}
                  >
                    {node.name}
                  </div>
                  {activeNode === node.id && (
                    <div className="mt-1 text-xs text-gray-400">{node.desc}</div>
                  )}
                </div>
              </div>
            );
          })}

        {/* Center node */}
        <div
          className="absolute left-1/2 top-1/2 cursor-pointer"
          onMouseEnter={() => setActiveNode("action")}
          onMouseLeave={() => setActiveNode(null)}
          style={{ transform: "translate(-50%, -50%)" }}
        >
          <div
            className="flex h-24 w-24 items-center justify-center rounded-full bg-gradient-to-br from-white to-gray-300 shadow-2xl"
            style={{
              boxShadow: `0 0 ${40 + pulseIntensity * 40}px rgba(255, 255, 255, ${
                0.5 + pulseIntensity * 0.5
              })`,
            }}
          >
            <Circle className="h-12 w-12 text-black" />
          </div>
          {activeNode === "action" && (
            <div className="absolute -bottom-12 left-1/2 -translate-x-1/2 text-sm text-white">
              Center Point
            </div>
          )}
        </div>
      </div>

      {/* Info overlay */}
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 text-center">
        <div className="mb-2 flex items-center justify-center gap-2 text-2xl font-light text-white">
          <Anchor className="h-6 w-6 text-blue-400" />
          CONSTELLATION OPERATIONAL
        </div>
        <div className="text-sm text-gray-400">{activeLabel}</div>
      </div>

      {/* Sigil row */}
      <div className="absolute top-8 left-1/2 -translate-x-1/2 flex gap-4 text-2xl opacity-30">
        <span>𓂀</span>
        <span>🜂</span>
        <span>𓁈</span>
        <span>⚓️</span>
      </div>

      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 0.2; transform: scale(1); }
          50% { opacity: 0.8; transform: scale(1.5); }
        }
      `}</style>
    </div>
  );
};

export default ConstellationPulse;
