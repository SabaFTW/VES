/**
 * VES Global State Store (Zustand)
 * Manages application-wide state
 */

import { create } from 'zustand';
import VESAgentService from '../services/vesAgent';

export const useVESStore = create((set, get) => ({
  // VES Agent status
  agentStatus: 'unknown',
  agentHealth: null,

  // System status
  systems: [],
  systemsLoading: false,
  systemsError: null,

  // Available agents
  agents: [],
  agentsLoading: false,

  // Current view
  currentView: 'dashboard',
  selectedSystem: null,
  selectedAgent: null,

  // Theme
  isDarkMode: true,

  // Actions
  setCurrentView: (view) => set({ currentView: view }),
  setSelectedSystem: (system) => set({ selectedSystem: system }),
  setSelectedAgent: (agent) => set({ selectedAgent: agent }),
  toggleTheme: () => set((state) => ({ isDarkMode: !state.isDarkMode })),

  // Fetch VES Agent health
  checkAgentHealth: async () => {
    try {
      const health = await VESAgentService.health();
      set({
        agentStatus: health.status === 'offline' ? 'offline' : 'online',
        agentHealth: health
      });
    } catch (error) {
      set({
        agentStatus: 'offline',
        agentHealth: { error: error.message }
      });
    }
  },

  // Fetch system status
  fetchSystems: async () => {
    set({ systemsLoading: true, systemsError: null });
    try {
      const systems = await VESAgentService.getSystemStatus();
      set({ systems, systemsLoading: false });
    } catch (error) {
      set({
        systemsError: error.message,
        systemsLoading: false
      });
    }
  },

  // Fetch available agents
  fetchAgents: async () => {
    set({ agentsLoading: true });
    try {
      const agents = await VESAgentService.getAgents();
      set({ agents, agentsLoading: false });
    } catch (error) {
      console.error('Failed to fetch agents:', error);
      set({ agentsLoading: false });
    }
  },

  // Initialize store (call on app load)
  initialize: async () => {
    await get().checkAgentHealth();
    await get().fetchSystems();
    await get().fetchAgents();
  }
}));
