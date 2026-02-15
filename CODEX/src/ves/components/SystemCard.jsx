/**
 * System Card Component
 * Displays status and info for a VES subsystem
 */

import React from 'react';
import { CheckCircle, XCircle, AlertCircle, ChevronRight } from 'lucide-react';

const SYSTEM_INFO = {
  CONSTELLATION_BRIDGE: {
    icon: '🌉',
    title: 'Constellation Bridge',
    description: 'Federated routing between GHOSTLINE & EROS',
    color: 'from-purple-500 to-pink-500'
  },
  RESEARCH_ORCHESTRATOR: {
    icon: '🔬',
    title: 'Research Orchestrator',
    description: 'Local research with RAG & ripgrep',
    color: 'from-blue-500 to-cyan-500'
  },
  GHOSTCORE: {
    icon: '👻',
    title: 'Ghostcore',
    description: 'Forensic evidence compilation system',
    color: 'from-green-500 to-emerald-500'
  },
  AGENTS: {
    icon: '🤖',
    title: 'Agent Constellation',
    description: '6 AI agents with memory & personality',
    color: 'from-orange-500 to-red-500'
  },
  ACTIVE_PROJECTS: {
    icon: '📂',
    title: 'Active Projects',
    description: '8 organized project categories',
    color: 'from-indigo-500 to-purple-500'
  },
  CODEX: {
    icon: '💎',
    title: 'Codex PWA',
    description: 'Living artifact interface',
    color: 'from-yellow-500 to-orange-500'
  }
};

export default function SystemCard({ system, onClick }) {
  const info = SYSTEM_INFO[system.name] || {
    icon: '📦',
    title: system.name,
    description: 'VES Subsystem',
    color: 'from-gray-500 to-gray-600'
  };

  const isOnline = system.status === 'online';
  const StatusIcon = isOnline ? CheckCircle : XCircle;

  return (
    <div
      onClick={onClick}
      className={`
        relative overflow-hidden rounded-xl p-6 cursor-pointer
        transition-all duration-300 hover:scale-105 hover:shadow-2xl
        bg-gradient-to-br ${info.color}
        group
      `}
    >
      {/* Background pattern */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute inset-0 bg-gradient-to-br from-white to-transparent" />
      </div>

      {/* Content */}
      <div className="relative z-10">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="text-5xl">{info.icon}</div>
          <StatusIcon
            className={`w-6 h-6 ${
              isOnline ? 'text-green-300' : 'text-red-300'
            }`}
          />
        </div>

        {/* Title */}
        <h3 className="text-xl font-bold text-white mb-2">{info.title}</h3>

        {/* Description */}
        <p className="text-sm text-white/80 mb-4">{info.description}</p>

        {/* Stats */}
        <div className="flex items-center justify-between text-xs text-white/70">
          <span>
            {system.itemCount !== undefined
              ? `${system.itemCount} items`
              : 'Status unknown'}
          </span>
          <ChevronRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
        </div>
      </div>

      {/* Hover glow effect */}
      <div className="absolute inset-0 opacity-0 group-hover:opacity-20 transition-opacity duration-300 bg-white rounded-xl" />
    </div>
  );
}
