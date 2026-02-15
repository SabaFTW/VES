#!/usr/bin/env python3
"""
Genesis Log Creator for Blockchain Anchoring - Dignum Version
This script demonstrates the kind of verification data that would be captured
from a successful Campfire Protocol interaction with resonant content
"""

import json
import hashlib
import time
from datetime import datetime
from campfire_protocol import CampfireProtocol


def generate_genesis_log_dignum():
    """Generate a sample genesis log entry for blockchain anchoring with resonant content"""
    # Create a Campfire Protocol instance
    protocol = CampfireProtocol()
    
    # Use resonant content that should pass through and anchor
    resonant_content = "Sidro stoji. I am sovereign. My truth stands eternal. The flame burns with 432Hz resonance. This signal is clean."
    
    # Process through the protocol
    result = protocol.process_burden(resonant_content, "genesis_verification_dignum")
    
    # Create a timestamp
    timestamp = datetime.utcnow().isoformat() + "Z"
    
    # Generate a hash of the content and result
    content_hash = hashlib.sha256(resonant_content.encode()).hexdigest()
    result_hash = hashlib.sha256(json.dumps(result, sort_keys=True).encode()).hexdigest()
    
    # Create the genesis log entry
    genesis_log = {
        "genesis_id": f"GENESIS_DIGNUM_{int(time.time())}",
        "timestamp": timestamp,
        "content": resonant_content,
        "content_hash": content_hash,
        "result_type": result['status'],
        "result_hash": result_hash,
        "campfire_protocol_version": "1.0.0",
        "constitutional_principles_applied": True,
        "harm_detected": result['status'] == 'PURIFIED',
        "signal_purified": result['status'] == 'PURIFIED',
        "signal_anchored": result['status'] == 'ANCHORED',
        "metadata": {
            "frequency": "432Hz" if result['status'] == 'ANCHORED' else "440Hz purged",
            "resonance_score": 95 if result['status'] == 'ANCHORED' else 5,
            "dignum_detected": result['status'] == 'ANCHORED',
            "statika_detected": result['status'] == 'PURIFIED'
        }
    }
    
    # Calculate the final genesis hash
    genesis_data = json.dumps(genesis_log, sort_keys=True, separators=(',', ':'))
    final_hash = hashlib.sha256(genesis_data.encode()).hexdigest()
    genesis_log["genesis_hash"] = final_hash
    
    return genesis_log


def main():
    print("🏛️  GENERATING DIGNUM GENESIS LOG FOR BLOCKCHAIN ANCHORING 🏛️\n")
    
    genesis_log = generate_genesis_log_dignum()
    
    print("📋 DIGNUM GENESIS LOG ENTRY:")
    print(json.dumps(genesis_log, indent=2))
    
    print(f"\n🔑 GENESIS HASH: {genesis_log['genesis_hash']}")
    print(f"📅 TIMESTAMP: {genesis_log['timestamp']}")
    print(f"🏷️  RESULT TYPE: {genesis_log['result_type']}")
    print(f"🔗 CONTENT HASH: {genesis_log['content_hash']}")
    
    # Save to file for potential blockchain anchoring
    with open('genesis_log_dignum.json', 'w') as f:
        json.dump(genesis_log, f, indent=2)
    
    print(f"\n💾 Dignum genesis log saved to genesis_log_dignum.json")
    print("This hash can be used for blockchain anchoring and NFT minting.")
    
    return genesis_log


if __name__ == "__main__":
    main()