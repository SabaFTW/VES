#!/usr/bin/env python3
"""
Debug script to test VES API connection
"""
import urllib.request
import json

def debug_ves_connection():
    print("Testing VES API connection...")
    
    try:
        print("1. Fetching identities from VES API...")
        with urllib.request.urlopen('http://localhost:8000/api/v1/identities') as response:
            data = json.loads(response.read().decode())
        print(f"   Success! Retrieved {data['count']} identities")
        
        print("2. Fetching states from VES API...")
        with urllib.request.urlopen('http://localhost:8000/api/v1/states') as response:
            states_data = json.loads(response.read().decode())
        print(f"   Success! Retrieved {states_data['count']} states")
        
        # Check for Lyra and Sabad specifically
        lyra_found = any(identity['node_name'] == 'Lyra' for identity in data['identities'])
        sabad_found = any(identity['node_name'] == 'Sabad' for identity in data['identities'])
        lyralower_found = any(identity['node_name'] == 'lyra' for identity in data['identities'])
        sabadlower_found = any(identity['node_name'] == 'sabad' for identity in data['identities'])
        
        print(f"3. Checking for key identities...")
        print(f"   Lyra found: {lyra_found or lyralower_found}")
        print(f"   Sabad found: {sabad_found or sabadlower_found}")
        
        if lyra_found or lyralower_found:
            print("   Lyra confirmed in VES!")
        if sabad_found or sabadlower_found:
            print("   Sabad confirmed in VES!")
            
        # Print a few identities to verify
        print(f"4. Sample identities from VES:")
        for identity in data['identities'][:5]:
            print(f"   - {identity['node_name']} ({identity['connection_type']})")
            
        return True
        
    except Exception as e:
        print(f"Error connecting to VES API: {e}")
        return False

if __name__ == "__main__":
    success = debug_ves_connection()
    if success:
        print("\n✅ VES API Connection: SUCCESS")
        print("The unified system can connect to VES CORE database!")
    else:
        print("\n❌ VES API Connection: FAILED")