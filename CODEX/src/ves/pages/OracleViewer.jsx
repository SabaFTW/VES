/**
 * Oracle Viewer - Cosmic Oracle Pattern Discovery
 * Real-time pattern visualization and knowledge search
 */

import React, { useState, useEffect } from 'react';
import { useVESStore } from '../store/vesStore';
import cosmicOracle from '../services/cosmicOracle';
import { Search, ArrowLeft, Zap, GitBranch, Activity } from 'lucide-react';

export default function OracleViewer() {
  const { setCurrentView } = useVESStore();
  const [oracleStatus, setOracleStatus] = useState('unknown');
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [patterns, setPatterns] = useState({ nodes: [], edges: [] });
  const [isSearching, setIsSearching] = useState(false);

  useEffect(() => {
    // Check Oracle health
    const checkHealth = async () => {
      const health = await cosmicOracle.health();
      setOracleStatus(health.status === 'offline' ? 'offline' : 'online');
    };

    checkHealth();

    // Connect to Oracle for real-time updates
    cosmicOracle.connect();

    // Subscribe to pattern updates
    cosmicOracle.onPatternUpdate((data) => {
      console.log('🔮 Pattern update:', data);
      // Update patterns in real-time
    });

    return () => {
      // Don't disconnect on unmount - keep connection alive
    };
  }, []);

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;

    setIsSearching(true);
    const results = await cosmicOracle.search(searchQuery);
    setSearchResults(results.results || []);
    setIsSearching(false);
  };

  const loadPatterns = async () => {
    const data = await cosmicOracle.getPatterns();
    setPatterns(data);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
      {/* Header */}
      <header className="border-b border-white/10 backdrop-blur-lg bg-black/20">
        <div className="container mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <button
                onClick={() => setCurrentView('dashboard')}
                className="p-2 rounded-lg bg-white/5 hover:bg-white/10 transition-colors"
              >
                <ArrowLeft className="w-5 h-5 text-white" />
              </button>
              <div className="flex items-center gap-3">
                <div className="text-3xl">🔮</div>
                <div>
                  <h1 className="text-2xl font-bold text-white">Cosmic Oracle</h1>
                  <p className="text-sm text-white/60">Pattern Discovery & Knowledge Graph</p>
                </div>
              </div>
            </div>

            {/* Status Badge */}
            <div className="flex items-center gap-2 px-4 py-2 rounded-lg bg-white/5">
              <Activity className="w-4 h-4 text-purple-400" />
              <span className="text-sm text-white/80">Oracle:</span>
              <span
                className={`text-sm font-bold ${
                  oracleStatus === 'online' ? 'text-green-400' : 'text-red-400'
                }`}
              >
                {oracleStatus.toUpperCase()}
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-12">
        {/* Search Section */}
        <div className="max-w-4xl mx-auto mb-12">
          <div className="bg-white/5 backdrop-blur-lg rounded-xl border border-white/10 p-6">
            <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
              <Search className="w-5 h-5 text-cyan-400" />
              Search VES Knowledge
            </h2>

            <div className="flex gap-2 mb-4">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                placeholder="Search patterns, memories, research..."
                className="flex-1 px-4 py-3 rounded-lg bg-white/5 border border-white/10 text-white placeholder-white/40 focus:outline-none focus:ring-2 focus:ring-purple-500"
              />
              <button
                onClick={handleSearch}
                disabled={isSearching || !searchQuery.trim()}
                className="px-6 py-3 rounded-lg bg-gradient-to-r from-purple-500 to-pink-500 text-white font-bold hover:from-purple-600 hover:to-pink-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
              >
                {isSearching ? 'Searching...' : 'Search'}
              </button>
            </div>

            {/* Search Results */}
            {searchResults.length > 0 && (
              <div className="space-y-2">
                <p className="text-sm text-white/60 mb-2">
                  Found {searchResults.length} results
                </p>
                {searchResults.map((result, idx) => (
                  <div
                    key={idx}
                    className="p-3 rounded-lg bg-white/5 border border-white/10 hover:border-purple-500/30 transition-all"
                  >
                    <p className="text-sm text-white">{result.text || result.content}</p>
                    {result.source && (
                      <p className="text-xs text-white/40 mt-1">{result.source}</p>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Pattern Discovery */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Pattern Stats */}
          <div className="bg-white/5 backdrop-blur-lg rounded-xl border border-white/10 p-6">
            <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
              <GitBranch className="w-5 h-5 text-green-400" />
              Pattern Network
            </h3>

            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 rounded-lg bg-gradient-to-br from-purple-500/20 to-pink-500/20 border border-purple-500/30">
                <div>
                  <p className="text-sm text-white/60">Total Patterns</p>
                  <p className="text-2xl font-bold text-white">{patterns.nodes?.length || 0}</p>
                </div>
                <Zap className="w-8 h-8 text-purple-400" />
              </div>

              <div className="flex items-center justify-between p-4 rounded-lg bg-gradient-to-br from-cyan-500/20 to-blue-500/20 border border-cyan-500/30">
                <div>
                  <p className="text-sm text-white/60">Connections</p>
                  <p className="text-2xl font-bold text-white">{patterns.edges?.length || 0}</p>
                </div>
                <GitBranch className="w-8 h-8 text-cyan-400" />
              </div>

              <button
                onClick={loadPatterns}
                className="w-full px-4 py-3 rounded-lg bg-gradient-to-r from-green-500 to-emerald-500 text-white font-bold hover:from-green-600 hover:to-emerald-600 transition-all"
              >
                Load Pattern Graph
              </button>
            </div>
          </div>

          {/* Pattern Visualization Placeholder */}
          <div className="bg-white/5 backdrop-blur-lg rounded-xl border border-white/10 p-6">
            <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
              <Activity className="w-5 h-5 text-cyan-400" />
              Live Visualization
            </h3>

            <div className="aspect-square rounded-lg bg-gradient-to-br from-purple-500/10 to-cyan-500/10 border border-white/10 flex items-center justify-center">
              <div className="text-center">
                <div className="text-6xl mb-4">🔮</div>
                <p className="text-white/60 text-sm">
                  Pattern graph visualization
                  <br />
                  (D3.js/Vis.js integration coming)
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Info Box */}
        {oracleStatus === 'offline' && (
          <div className="mt-6 p-4 rounded-lg bg-yellow-500/10 border border-yellow-500/30 text-yellow-200">
            <p className="text-sm">
              ⚠️ Cosmic Oracle is offline. Start it with:{' '}
              <code className="bg-black/30 px-2 py-1 rounded">
                docker-compose up -d cosmic-oracle
              </code>
            </p>
          </div>
        )}
      </main>
    </div>
  );
}
