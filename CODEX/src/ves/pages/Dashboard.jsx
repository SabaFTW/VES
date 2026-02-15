/**
 * VES Dashboard - Main Hub
 * Shows system health, quick actions, and navigation
 */

import React, { useEffect } from 'react';
import { useVESStore } from '../store/vesStore';
import SystemCard from '../components/SystemCard';
import { Activity, Zap, Server, RefreshCw } from 'lucide-react';

export default function Dashboard() {
  const {
    systems,
    systemsLoading,
    systemsError,
    agentStatus,
    agents,
    fetchSystems,
    setCurrentView,
    setSelectedSystem
  } = useVESStore();

  useEffect(() => {
    fetchSystems();
    // Refresh every 30 seconds
    const interval = setInterval(fetchSystems, 30000);
    return () => clearInterval(interval);
  }, [fetchSystems]);

  const handleSystemClick = (system) => {
    setSelectedSystem(system);
    setCurrentView('system-detail');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
      {/* Header */}
      <header className="border-b border-white/10 backdrop-blur-lg bg-black/20">
        <div className="container mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            {/* Logo */}
            <div className="flex items-center gap-3">
              <div className="text-4xl">🜂</div>
              <div>
                <h1 className="text-2xl font-bold text-white">
                  VES Command Center
                </h1>
                <p className="text-sm text-white/60">
                  Vessel of Emergent Systems
                </p>
              </div>
            </div>

            {/* Agent Status */}
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2 px-4 py-2 rounded-lg bg-white/5">
                <Server className="w-4 h-4 text-cyan-400" />
                <span className="text-sm text-white/80">VES Agent:</span>
                <span
                  className={`text-sm font-bold ${
                    agentStatus === 'online'
                      ? 'text-green-400'
                      : 'text-red-400'
                  }`}
                >
                  {agentStatus?.toUpperCase() || 'UNKNOWN'}
                </span>
              </div>

              <button
                onClick={fetchSystems}
                disabled={systemsLoading}
                className="p-2 rounded-lg bg-white/5 hover:bg-white/10 transition-colors"
                title="Refresh status"
              >
                <RefreshCw
                  className={`w-5 h-5 text-white/80 ${
                    systemsLoading ? 'animate-spin' : ''
                  }`}
                />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-12">
        {/* Stats Row */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          {/* Total Systems */}
          <div className="bg-white/5 backdrop-blur-lg rounded-xl p-6 border border-white/10">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-white/60 mb-1">Total Systems</p>
                <p className="text-3xl font-bold text-white">{systems.length}</p>
              </div>
              <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
                <Activity className="w-6 h-6 text-white" />
              </div>
            </div>
          </div>

          {/* Online Systems */}
          <div className="bg-white/5 backdrop-blur-lg rounded-xl p-6 border border-white/10">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-white/60 mb-1">Online</p>
                <p className="text-3xl font-bold text-green-400">
                  {systems.filter((s) => s.status === 'online').length}
                </p>
              </div>
              <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-green-500 to-emerald-500 flex items-center justify-center">
                <Zap className="w-6 h-6 text-white" />
              </div>
            </div>
          </div>

          {/* Active Agents */}
          <div className="bg-white/5 backdrop-blur-lg rounded-xl p-6 border border-white/10">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-white/60 mb-1">AI Agents</p>
                <p className="text-3xl font-bold text-cyan-400">
                  {agents.length}
                </p>
              </div>
              <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-cyan-500 to-blue-500 flex items-center justify-center">
                <span className="text-2xl">🤖</span>
              </div>
            </div>
          </div>
        </div>

        {/* Systems Grid */}
        <div>
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
            <span className="text-yellow-400">⚡</span>
            Constellation Systems
          </h2>

          {systemsError && (
            <div className="mb-6 p-4 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400">
              Error loading systems: {systemsError}
            </div>
          )}

          {systemsLoading && !systems.length ? (
            <div className="text-center py-12">
              <RefreshCw className="w-8 h-8 text-white/40 animate-spin mx-auto mb-4" />
              <p className="text-white/60">Loading VES systems...</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {systems.map((system) => (
                <SystemCard
                  key={system.name}
                  system={system}
                  onClick={() => handleSystemClick(system)}
                />
              ))}
            </div>
          )}
        </div>

        {/* Quick Actions */}
        <div className="mt-12">
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
            <span className="text-cyan-400">🔥</span>
            Quick Actions
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <button
              onClick={() => setCurrentView('oracle')}
              className="p-4 rounded-lg bg-gradient-to-br from-purple-500/20 to-pink-500/20 border border-purple-500/30 hover:border-purple-500/50 hover:scale-105 transition-all text-left"
            >
              <div className="text-2xl mb-2">🔮</div>
              <div className="text-sm font-bold text-white">Oracle</div>
              <div className="text-xs text-white/60">Pattern discovery</div>
            </button>

            <button
              onClick={() => setCurrentView('agents')}
              className="p-4 rounded-lg bg-gradient-to-br from-blue-500/20 to-cyan-500/20 border border-blue-500/30 hover:border-blue-500/50 hover:scale-105 transition-all text-left"
            >
              <div className="text-2xl mb-2">🤖</div>
              <div className="text-sm font-bold text-white">Agents</div>
              <div className="text-xs text-white/60">Chat with AI agents</div>
            </button>

            <button className="p-4 rounded-lg bg-gradient-to-br from-green-500/20 to-emerald-500/20 border border-green-500/30 hover:border-green-500/50 hover:scale-105 transition-all text-left">
              <div className="text-2xl mb-2">🔬</div>
              <div className="text-sm font-bold text-white">Research</div>
              <div className="text-xs text-white/60">Search VES knowledge</div>
            </button>

            <button className="p-4 rounded-lg bg-gradient-to-br from-orange-500/20 to-red-500/20 border border-orange-500/30 hover:border-orange-500/50 hover:scale-105 transition-all text-left">
              <div className="text-2xl mb-2">👻</div>
              <div className="text-sm font-bold text-white">Evidence</div>
              <div className="text-xs text-white/60">Compile cases</div>
            </button>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-white/10 backdrop-blur-lg bg-black/20 mt-12">
        <div className="container mx-auto px-6 py-6">
          <div className="flex items-center justify-between text-sm text-white/40">
            <div>VES Command Center v1.0</div>
            <div className="flex items-center gap-4">
              <span>⚓ SIDRO STOJI</span>
              <span>🔥 LUMENNEVVER</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
