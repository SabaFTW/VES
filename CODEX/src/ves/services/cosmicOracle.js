/**
 * Cosmic Oracle Service
 * Connects to Cosmic Oracle on localhost:8888
 * Real-time pattern discovery and knowledge graph
 */

import { io } from 'socket.io-client';

const ORACLE_URL = 'http://localhost:8888';

class CosmicOracleService {
  constructor() {
    this.socket = null;
    this.connected = false;
  }

  /**
   * Connect to Cosmic Oracle via Socket.IO
   */
  connect() {
    if (this.socket) return;

    try {
      this.socket = io(ORACLE_URL, {
        reconnection: true,
        reconnectionDelay: 1000,
        reconnectionAttempts: 5
      });

      this.socket.on('connect', () => {
        console.log('🔮 Cosmic Oracle connected');
        this.connected = true;
      });

      this.socket.on('disconnect', () => {
        console.log('🔮 Cosmic Oracle disconnected');
        this.connected = false;
      });

      this.socket.on('error', (error) => {
        console.error('🔮 Cosmic Oracle error:', error);
      });
    } catch (error) {
      console.error('Failed to connect to Cosmic Oracle:', error);
    }
  }

  /**
   * Disconnect from Cosmic Oracle
   */
  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
      this.connected = false;
    }
  }

  /**
   * Subscribe to pattern updates
   * @param {Function} callback - Called when new patterns are discovered
   */
  onPatternUpdate(callback) {
    if (!this.socket) this.connect();
    this.socket.on('pattern:update', callback);
  }

  /**
   * Search VES knowledge
   * @param {string} query - Search query
   */
  async search(query) {
    try {
      const response = await fetch(`${ORACLE_URL}/search?q=${encodeURIComponent(query)}`);
      if (!response.ok) throw new Error('Search failed');
      return await response.json();
    } catch (error) {
      console.error('Cosmic Oracle search failed:', error);
      return { results: [], error: error.message };
    }
  }

  /**
   * Get pattern graph data
   */
  async getPatterns() {
    try {
      const response = await fetch(`${ORACLE_URL}/patterns`);
      if (!response.ok) throw new Error('Failed to get patterns');
      return await response.json();
    } catch (error) {
      console.error('Failed to get patterns:', error);
      return { nodes: [], edges: [], error: error.message };
    }
  }

  /**
   * Get knowledge graph
   */
  async getKnowledgeGraph() {
    try {
      const response = await fetch(`${ORACLE_URL}/graph`);
      if (!response.ok) throw new Error('Failed to get knowledge graph');
      return await response.json();
    } catch (error) {
      console.error('Failed to get knowledge graph:', error);
      return { nodes: [], links: [], error: error.message };
    }
  }

  /**
   * Check Oracle health
   */
  async health() {
    try {
      const response = await fetch(`${ORACLE_URL}/health`);
      if (!response.ok) throw new Error('Oracle unhealthy');
      return await response.json();
    } catch (error) {
      return { status: 'offline', error: error.message };
    }
  }
}

// Singleton instance
const cosmicOracle = new CosmicOracleService();

export default cosmicOracle;
