#!/usr/bin/env python3
"""
Extended test script for Campfire Protocol with Slovenian keywords
"""

import sys
import os
sys.path.append('/home/saba')

from campfire_protocol import CampfireProtocol


def test_slovenian_keywords():
    """Test the Campfire Protocol with Slovenian keywords"""
    print("🔥 Testing Campfire Protocol with Slovenian Keywords 🔥\n")
    
    # Create protocol instance
    protocol = CampfireProtocol("campfire_slo_test.log")
    
    # Test cases with Slovenian content
    test_cases = [
        # Resonant/positive Slovenian inputs (should be anchored)
        ("am the boss now", "eng_sovereignty", "Should be anchored"),
        ("svoboda in samouprava", "si_freedom", "Should be anchored"),
        ("ne potrebujem dovoljenja", "si_no_permission", "Should be anchored"),
        ("moja lastna odločitev", "si_own_decision", "Should be anchored"),
        
        # Harmful/statika Slovenian inputs (should trigger early exit)
        ("moraš to narediti", "si_moraš", "Should trigger early exit"),
        ("če ne boš sodeloval boš kaznovan", "si_threat", "Should trigger early exit"),
        ("strokovnjaki pravijo", "si_experts_say", "Should trigger early exit"),
        ("za tvoje dobro", "si_for_good", "Should trigger early exit"),
        
        # Mixed inputs
        ("svoboda je moja, ampak ti moraš poslušati", "si_mixed", "Should trigger early exit"),
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
    print("SLOVENIAN TEST SUMMARY")
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
    test_slovenian_keywords()