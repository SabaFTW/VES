/**
 * Agent Console - Chat with VES AI Agents
 * Multi-agent chat interface with memory and context
 */

import React, { useState, useEffect } from 'react';
import { useVESStore } from '../store/vesStore';
import AgentCard from '../components/AgentCard';
import { Send, ArrowLeft, Sparkles, Brain } from 'lucide-react';

export default function AgentConsole() {
  const { agents, agentsLoading, setCurrentView, selectedAgent, setSelectedAgent } = useVESStore();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  // Load agent memory when selected
  useEffect(() => {
    if (selectedAgent) {
      // TODO: Load actual conversation history from MEMORY.json
      setMessages([
        {
          role: 'system',
          content: `Connected to ${selectedAgent.name}. This agent specializes in their designated role.`,
          timestamp: Date.now()
        }
      ]);
    }
  }, [selectedAgent]);

  const handleSendMessage = () => {
    if (!input.trim()) return;

    // Add user message
    const userMessage = {
      role: 'user',
      content: input,
      timestamp: Date.now()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');

    // Simulate agent response (in real version, this would call the agent)
    setTimeout(() => {
      const agentMessage = {
        role: 'assistant',
        content: `This is a simulated response from ${selectedAgent?.name}. In the full version, this would connect to the actual agent via the CONSTELLATION_BRIDGE routing system.`,
        timestamp: Date.now()
      };
      setMessages(prev => [...prev, agentMessage]);
    }, 1000);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-indigo-900 to-gray-900">
      {/* Header */}
      <header className="border-b border-white/10 backdrop-blur-lg bg-black/20">
        <div className="container mx-auto px-6 py-6">
          <div className="flex items-center gap-4">
            <button
              onClick={() => {
                setCurrentView('dashboard');
                setSelectedAgent(null);
              }}
              className="p-2 rounded-lg bg-white/5 hover:bg-white/10 transition-colors"
            >
              <ArrowLeft className="w-5 h-5 text-white" />
            </button>
            <div className="flex items-center gap-3">
              <div className="text-3xl">🤖</div>
              <div>
                <h1 className="text-2xl font-bold text-white">Agent Constellation</h1>
                <p className="text-sm text-white/60">
                  {selectedAgent ? `Chatting with ${selectedAgent.name}` : 'Select an agent to begin'}
                </p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-12">
        {!selectedAgent ? (
          // Agent Selection Grid
          <div>
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
              <Sparkles className="w-6 h-6 text-cyan-400" />
              Available Agents
            </h2>

            {agentsLoading ? (
              <div className="text-center py-12 text-white/60">
                Loading agents...
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {agents.map((agent) => (
                  <AgentCard
                    key={agent.name}
                    agent={agent}
                    onClick={() => setSelectedAgent(agent)}
                  />
                ))}
              </div>
            )}
          </div>
        ) : (
          // Chat Interface
          <div className="max-w-4xl mx-auto">
            <div className="bg-white/5 backdrop-blur-lg rounded-xl border border-white/10 overflow-hidden">
              {/* Chat Messages */}
              <div className="h-[500px] overflow-y-auto p-6 space-y-4">
                {messages.map((msg, idx) => (
                  <div
                    key={idx}
                    className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[80%] rounded-lg p-4 ${
                        msg.role === 'user'
                          ? 'bg-gradient-to-br from-cyan-500 to-blue-500 text-white'
                          : msg.role === 'system'
                          ? 'bg-yellow-500/20 border border-yellow-500/30 text-yellow-200'
                          : 'bg-white/10 text-white'
                      }`}
                    >
                      {msg.role === 'assistant' && (
                        <div className="flex items-center gap-2 mb-2">
                          <Brain className="w-4 h-4 text-cyan-400" />
                          <span className="text-xs text-cyan-400 font-bold">
                            {selectedAgent.name}
                          </span>
                        </div>
                      )}
                      <p className="text-sm">{msg.content}</p>
                      <p className="text-xs opacity-60 mt-2">
                        {new Date(msg.timestamp).toLocaleTimeString()}
                      </p>
                    </div>
                  </div>
                ))}
              </div>

              {/* Input Area */}
              <div className="border-t border-white/10 p-4 bg-black/20">
                <div className="flex gap-2">
                  <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                    placeholder={`Message ${selectedAgent.name}...`}
                    className="flex-1 px-4 py-3 rounded-lg bg-white/5 border border-white/10 text-white placeholder-white/40 focus:outline-none focus:ring-2 focus:ring-cyan-500"
                  />
                  <button
                    onClick={handleSendMessage}
                    disabled={!input.trim()}
                    className="px-6 py-3 rounded-lg bg-gradient-to-r from-cyan-500 to-blue-500 text-white font-bold hover:from-cyan-600 hover:to-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                  >
                    <Send className="w-5 h-5" />
                  </button>
                </div>
                <p className="text-xs text-white/40 mt-2">
                  💡 Tip: In full version, this connects to CONSTELLATION_BRIDGE for intelligent routing
                </p>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
