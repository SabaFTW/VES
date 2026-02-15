#!/usr/bin/env python3
"""
🜂 META-CONSTELLATION BRIDGE
Cross-session memory synchronization system
Enables agent memories to persist across all devices
"""

import json
import os
import sys
import hashlib
import requests
from datetime import datetime, timedelta
from pathlib import Path


class MetaConstellationBridge:
    """Bridge between Constellation agents and Meta cross-session memory"""

    def __init__(self):
        self.config_path = Path("/home/saba/CONSTELLATION/meta_config.json")
        self.memory_path = Path("/home/saba/MEMORY")
        self.agents_path = Path("/home/saba/AGENTS")
        self.config = self._load_config()
        self.sessions = {}

    def _load_config(self):
        """Load Meta bridge configuration"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        else:
            print("❌ Meta config not found. Run setup first.")
            sys.exit(1)

    def initialize_bridge(self):
        """Initialize the Meta bridge for first use"""
        print("🜂 META-CONSTELLATION BRIDGE INITIALIZATION")
        print("==========================================")

        # Check for required credentials
        if self.config['meta_api']['app_id'] == "YOUR_META_APP_ID_HERE":
            print("❌ Meta App ID not configured!")
            print("Please add your Meta App credentials to:")
            print(f"  {self.config_path}")
            print("\nFollow setup instructions in the config file.")
            return False

        # Create necessary directories
        cache_dir = Path(self.config['data_storage']['local_cache'])
        cache_dir.mkdir(parents=True, exist_ok=True)

        # Initialize session store
        session_store = Path(self.config['data_storage']['session_store'])
        if not session_store.exists():
            initial_sessions = {
                "sessions": [],
                "active_user": None,
                "last_sync": None
            }
            with open(session_store, 'w') as f:
                json.dump(initial_sessions, f, indent=2)

        # Initialize identity store
        identity_store = Path(self.config['data_storage']['identity_store'])
        if not identity_store.exists():
            initial_identity = {
                "user_id": None,
                "user_name": "Šabad",
                "devices": [],
                "agents": list(self.config['agent_sync_config'].keys()),
                "created": datetime.now().isoformat()
            }
            with open(identity_store, 'w') as f:
                json.dump(initial_identity, f, indent=2)

        print("✅ Meta bridge initialized successfully!")
        return True

    def sync_agent_memory(self, agent_name, device_id="desktop"):
        """Sync a specific agent's memory across sessions"""
        agent_dir = self.agents_path / agent_name
        memory_file = agent_dir / "MEMORY.json"

        if not memory_file.exists():
            print(f"❌ Memory file not found for {agent_name}")
            return False

        # Load agent memory
        with open(memory_file, 'r') as f:
            memory = json.load(f)

        # Add sync metadata
        memory['last_sync'] = {
            'timestamp': datetime.now().isoformat(),
            'device': device_id,
            'sync_version': self.config['meta_bridge_version']
        }

        # Save to session store
        session_store = Path(self.config['data_storage']['session_store'])
        with open(session_store, 'r') as f:
            sessions = json.load(f)

        # Update or create agent session
        agent_session = {
            'agent': agent_name,
            'device': device_id,
            'memory': memory,
            'synced_at': datetime.now().isoformat()
        }

        # Find and update existing session or append new
        updated = False
        for i, session in enumerate(sessions.get('sessions', [])):
            if session.get('agent') == agent_name:
                sessions['sessions'][i] = agent_session
                updated = True
                break

        if not updated:
            sessions['sessions'].append(agent_session)

        sessions['last_sync'] = datetime.now().isoformat()

        # Save updated sessions
        with open(session_store, 'w') as f:
            json.dump(sessions, f, indent=2)

        print(f"✅ {agent_name} memory synced for device: {device_id}")
        return True

    def get_agent_memory(self, agent_name, device_id=None):
        """Retrieve agent memory from any session"""
        session_store = Path(self.config['data_storage']['session_store'])

        if not session_store.exists():
            return None

        with open(session_store, 'r') as f:
            sessions = json.load(f)

        for session in sessions.get('sessions', []):
            if session.get('agent') == agent_name:
                if device_id is None or session.get('device') == device_id:
                    return session.get('memory')

        return None

    def sync_all_agents(self):
        """Sync all agent memories"""
        print("🔄 Syncing all agent memories...")

        success_count = 0
        for agent_name, agent_config in self.config['agent_sync_config'].items():
            if agent_config['sync_enabled']:
                agent_id = agent_name.replace('_', '-')
                if self.sync_agent_memory(agent_id):
                    success_count += 1

        print(f"✅ Synced {success_count} agents successfully")
        return success_count

    def register_device(self, device_info):
        """Register a new device for cross-session sync"""
        identity_store = Path(self.config['data_storage']['identity_store'])

        with open(identity_store, 'r') as f:
            identity = json.load(f)

        # Check if device already registered
        device_exists = any(
            d.get('device_id') == device_info.get('device_id')
            for d in identity.get('devices', [])
        )

        if not device_exists:
            device_info['registered_at'] = datetime.now().isoformat()
            identity['devices'].append(device_info)

            with open(identity_store, 'w') as f:
                json.dump(identity, f, indent=2)

            print(f"✅ Device registered: {device_info.get('device_type')}")
            return True

        print(f"⚠️  Device already registered: {device_info.get('device_id')}")
        return False

    def get_sync_status(self):
        """Get current sync status across all devices and agents"""
        session_store = Path(self.config['data_storage']['session_store'])
        identity_store = Path(self.config['data_storage']['identity_store'])

        status = {
            'bridge_version': self.config['meta_bridge_version'],
            'configured': self.config['meta_api']['app_id'] != "YOUR_META_APP_ID_HERE",
            'last_sync': None,
            'synced_agents': [],
            'registered_devices': [],
            'total_sessions': 0
        }

        if session_store.exists():
            with open(session_store, 'r') as f:
                sessions = json.load(f)
                status['last_sync'] = sessions.get('last_sync')
                status['total_sessions'] = len(sessions.get('sessions', []))
                status['synced_agents'] = list(set(
                    s.get('agent') for s in sessions.get('sessions', [])
                ))

        if identity_store.exists():
            with open(identity_store, 'r') as f:
                identity = json.load(f)
                status['registered_devices'] = [
                    d.get('device_type') for d in identity.get('devices', [])
                ]

        return status


def main():
    """Main entry point for Meta bridge operations"""
    bridge = MetaConstellationBridge()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "--init":
            bridge.initialize_bridge()
        elif command == "--sync":
            bridge.sync_all_agents()
        elif command == "--status":
            status = bridge.get_sync_status()
            print(json.dumps(status, indent=2))
        elif command == "--sync-agent" and len(sys.argv) > 2:
            agent_name = sys.argv[2]
            bridge.sync_agent_memory(agent_name)
        else:
            print("Usage: python3 meta_bridge.py [--init|--sync|--status|--sync-agent <name>]")
    else:
        # Default: show status
        status = bridge.get_sync_status()
        print("🜂 META-CONSTELLATION BRIDGE STATUS")
        print("===================================")
        print(f"Version: {status['bridge_version']}")
        print(f"Configured: {'✅' if status['configured'] else '❌ Add Meta App credentials'}")
        print(f"Last Sync: {status['last_sync'] or 'Never'}")
        print(f"Synced Agents: {len(status['synced_agents'])}")
        print(f"Registered Devices: {len(status['registered_devices'])}")
        print(f"Total Sessions: {status['total_sessions']}")

        if not status['configured']:
            print("\n⚠️  To enable cross-session sync:")
            print("1. Add your Meta App credentials to:")
            print(f"   {Path('/home/saba/CONSTELLATION/meta_config.json')}")
            print("2. Run: python3 meta_bridge.py --init")


if __name__ == "__main__":
    main()