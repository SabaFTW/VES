/**
 * VES Agent API Service
 * Connects to VES Agent running on localhost:8420
 * Provides file system access and system info
 */

const VES_AGENT_URL = 'http://localhost:8420';

export class VESAgentService {
  /**
   * Check VES Agent health
   */
  static async health() {
    try {
      const response = await fetch(`${VES_AGENT_URL}/health`);
      if (!response.ok) throw new Error('VES Agent unhealthy');
      return await response.json();
    } catch (error) {
      console.error('VES Agent health check failed:', error);
      return { status: 'offline', error: error.message };
    }
  }

  /**
   * Scan VES directory structure
   */
  static async scan() {
    try {
      const response = await fetch(`${VES_AGENT_URL}/scan`);
      if (!response.ok) throw new Error('Scan failed');
      return await response.json();
    } catch (error) {
      console.error('VES scan failed:', error);
      throw error;
    }
  }

  /**
   * List directory contents
   * @param {string} path - Path relative to VES root
   */
  static async list(path = '') {
    try {
      const url = path
        ? `${VES_AGENT_URL}/list?path=${encodeURIComponent(path)}`
        : `${VES_AGENT_URL}/list`;
      const response = await fetch(url);
      if (!response.ok) throw new Error('List failed');
      return await response.json();
    } catch (error) {
      console.error(`VES list failed for path: ${path}`, error);
      throw error;
    }
  }

  /**
   * Read file contents
   * @param {string} path - Path relative to VES root
   */
  static async read(path) {
    try {
      const response = await fetch(
        `${VES_AGENT_URL}/read?path=${encodeURIComponent(path)}`
      );
      if (!response.ok) throw new Error('Read failed');
      return await response.json();
    } catch (error) {
      console.error(`VES read failed for path: ${path}`, error);
      throw error;
    }
  }

  /**
   * Get VES system status
   * Checks all 6 major subsystems
   */
  static async getSystemStatus() {
    try {
      const systems = [
        'CONSTELLATION_BRIDGE',
        'RESEARCH_ORCHESTRATOR',
        'GHOSTCORE',
        'AGENTS',
        'ACTIVE_PROJECTS',
        'CODEX'
      ];

      const statusPromises = systems.map(async (system) => {
        try {
          const exists = await this.list(system);
          return {
            name: system,
            status: 'online',
            path: system,
            itemCount: exists?.files?.length || 0
          };
        } catch (error) {
          return {
            name: system,
            status: 'offline',
            error: error.message
          };
        }
      });

      const results = await Promise.all(statusPromises);
      return results;
    } catch (error) {
      console.error('Failed to get system status:', error);
      throw error;
    }
  }

  /**
   * Load agent memory
   * @param {string} agentName - Name of agent (e.g., 'Lyra')
   */
  static async loadAgentMemory(agentName) {
    try {
      const path = `AGENTS/${agentName}/MEMORY.json`;
      const data = await this.read(path);
      return JSON.parse(data.content);
    } catch (error) {
      console.error(`Failed to load memory for ${agentName}:`, error);
      return null;
    }
  }

  /**
   * Load agent initialization
   * @param {string} agentName - Name of agent
   */
  static async loadAgentInit(agentName) {
    try {
      const path = `AGENTS/${agentName}/INIT.md`;
      const data = await this.read(path);
      return data.content;
    } catch (error) {
      console.error(`Failed to load INIT for ${agentName}:`, error);
      return null;
    }
  }

  /**
   * Get all available agents
   */
  static async getAgents() {
    try {
      const agentsDir = await this.list('AGENTS');
      const agentNames = agentsDir?.directories || [];

      const agentPromises = agentNames.map(async (name) => {
        const init = await this.loadAgentInit(name);
        const memory = await this.loadAgentMemory(name);
        return {
          name,
          hasInit: !!init,
          hasMemory: !!memory,
          init: init?.substring(0, 200), // Preview
          memorySize: memory ? JSON.stringify(memory).length : 0
        };
      });

      return await Promise.all(agentPromises);
    } catch (error) {
      console.error('Failed to get agents:', error);
      return [];
    }
  }
}

export default VESAgentService;
