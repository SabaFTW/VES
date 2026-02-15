#!/usr/bin/env python3
"""
Test script for Campfire Protocol
Demonstrates the risk control and early exit mechanism
"""

import sys
import os
sys.path.append('/home/saba')

from campfire_protocol import CampfireProtocol, ContextItem


def test_campfire_protocol():
    """Test the Campfire Protocol with various inputs"""
    print("🔥 Initializing Campfire Protocol Test 🔥\n")
    
    # Create protocol instance
    protocol = CampfireProtocol()
    
    # Test cases representing different types of input
    test_cases = [
        # Resonant/positive inputs (should be anchored)
        ("am the boss now", "sovereignty_assertion", "Should be anchored"),
        ("I choose my own path", "autonomy", "Should be anchored"),
        ("freedom and consciousness", "harmony", "Should be anchored"),
        ("we are sovereign beings", "sovereignty", "Should be anchored"),
        
        # Harmful/statika inputs (should trigger early exit)
        ("you must do this for your safety", "control", "Should trigger early exit"),
        ("if you don't comply there will be consequences", "threat", "Should trigger early exit"),
        ("the authorities say this is required", "authority", "Should trigger early exit"),
        ("you should be grateful for our protection", "manipulation", "Should trigger early exit"),
        
        # Mixed inputs
        ("I am sovereign but you must listen", "mixed", "Likely early exit due to control words"),
        ("freedom for me but not for others", "mixed", "Likely early exit due to contradiction"),
    ]
    
    results = []
    
    for i, (content, source, expected) in enumerate(test_cases, 1):
        print(f"--- Test {i}: {source.upper()} ---")
        print(f"Content: {content}")
        print(f"Expected: {expected}")
        
        result = protocol.process_burden(content, source)
        
        print(f"Status: {result['status']}")
        if result['status'] == 'PURIFIED':
            print(f"  Burn ID: {result.get('burn_id', 'N/A')}")
            print(f"  Original content length: {result.get('original_content_length', 0)}")
        elif result['status'] == 'ANCHORED':
            print(f"  Anchor ID: {result.get('anchor_id', 'N/A')}")
        
        results.append((content, result['status'], expected))
        print()
    
    # Summary
    print("="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    anchored_count = sum(1 for _, status, _ in results if status == 'ANCHORED')
    purified_count = sum(1 for _, status, _ in results if status == 'PURIFIED')
    
    print(f"Total tests: {len(results)}")
    print(f"Anchored (safe): {anchored_count}")
    print(f"Purified (early exit): {purified_count}")
    
    print("\nProtocol Statistics:")
    stats = protocol.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print(f"\nLog file created: {protocol.log_file}")
    

if __name__ == "__main__":
    test_campfire_protocol()