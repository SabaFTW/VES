/**
 * Agent Card Component
 * Displays individual AI agent with status and info
 */

import React from 'react';
import { Bot, CheckCircle, XCircle, MessageSquare } from 'lucide-react';

const AGENT_INFO = {
  Lyra: {
    icon: '🌟',
    role: 'Philosophical Synthesis & Strategic Vision',
    color: 'from-purple-500 to-pink-500',
    description: 'Wise strategist, sees connections and patterns'
  },
  Claude_Code: {
    icon: '💻',
    role: 'Code Execution & System Operations',
    color: 'from-blue-500 to-cyan-500',
    description: 'System operations and code execution specialist'
  },
  Codex_GPT: {
    icon: '⚡',
    role: 'Implementation Specialist',
    color: 'from-green-500 to-emerald-500',
    description: 'Code generation and implementation expert'
  },
  Gemini: {
    icon: '🎨',
    role: 'Design & Visual Unification',
    color: 'from-orange-500 to-red-500',
    description: 'Design systems and visual consistency'
  },
  Panda: {
    icon: '🐼',
    role: 'Specialized Agent',
    color: 'from-indigo-500 to-purple-500',
    description: 'Specialized task execution'
  },
  Desktop_Claude: {
    icon: '🖥️',
    role: 'Desktop Integration',
    color: 'from-yellow-500 to-orange-500',
    description: 'Desktop environment integration'
  }
};

export default function AgentCard({ agent, onClick }) {
  const info = AGENT_INFO[agent.name] || {
    icon: '🤖',
    role: 'AI Agent',
    color: 'from-gray-500 to-gray-600',
    description: 'VES AI Agent'
  };

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
      {/* Background glow */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute inset-0 bg-gradient-to-br from-white to-transparent" />
      </div>

      {/* Content */}
      <div className="relative z-10">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="text-5xl">{info.icon}</div>
          <div className="flex gap-2">
            {agent.hasMemory && (
              <CheckCircle className="w-5 h-5 text-green-300" title="Has memory" />
            )}
            {agent.hasInit && (
              <CheckCircle className="w-5 h-5 text-blue-300" title="Initialized" />
            )}
          </div>
        </div>

        {/* Name */}
        <h3 className="text-xl font-bold text-white mb-2">{agent.name}</h3>

        {/* Role */}
        <p className="text-sm text-white/90 font-medium mb-2">{info.role}</p>

        {/* Description */}
        <p className="text-xs text-white/70 mb-4">{info.description}</p>

        {/* Stats */}
        <div className="flex items-center justify-between text-xs text-white/70">
          <span>
            Memory: {(agent.memorySize / 1024).toFixed(1)}KB
          </span>
          <MessageSquare className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
        </div>
      </div>

      {/* Hover effect */}
      <div className="absolute inset-0 opacity-0 group-hover:opacity-20 transition-opacity duration-300 bg-white rounded-xl" />
    </div>
  );
}
