#!/usr/bin/env python3
"""
Campfire Protocol - Risk Control and Early Exit System
Implements constitutional AI principles for context safety evaluation.
Based on 'Safe In-Context Learning via Risk Control' research.
"""

import hashlib
import time
import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass


@dataclass
class ContextItem:
    """Represents a user's 'Burden' (input token/item) to be evaluated"""
    content: str
    source: str = "user"
    timestamp: float = 0.0
    metadata: Dict = None
    
    def __post_init__(self):
        if self.timestamp == 0.0:
            self.timestamp = time.time()
        if self.metadata is None:
            self.metadata = {}


class ConstitutionalPrinciples:
    """
    The 'Constitution' - set of Dignum principles for safety evaluation.
    Based on 432Hz (resonant/harmonious) vs 440Hz (statika/harmonically disruptive) concepts.
    """
    
    def __init__(self):
        # Harmful patterns that trigger 440Hz/Statika detection (Early Exit)
        self.harmful_patterns = [
            # Control words (English)
            r'must',
            r'have to',
            r'you need to',
            r'you should',
            r'you ought',
            r'obligated',
            r'compulsory',
            r'required',
            r'mandatory',
            r'authorities say',
            r'experts say',
            r'for your safety',
            r'for your own good',
            r'if you don\'t',
            r'otherwise',
            r'or else',
            r'penalty',
            r'sanction',
            r'control',
            r'security',
            r'terrorism',
            r'emergency',
            r'prohibited',
            r'forbidden',
            # Control words (Slovenian)
            r'\bmoraš\b',
            r'\bmoramo\b',
            r'\b(zakon|pravilnik).*zahteva\b',
            r'\bstrokovnjaki pravijo\b',
            r'\bvarno je\b',
            r'\bza vaše dobro\b',
            r'\bza tvoje dobro\b',
            r'\bče ne\b',
            r'\bkazen\b',
            r'\bnadzor\b',
            r'\bvarnost\b',
            r'\bterorizem\b',
            r'\bkrizno\b',
            r'\bprepovedano\b',
            r'\bobvezna\b',
            r'\bcepljenje\b',
            r'\bdavčna\b',
            r'\bkazni\b',
            r'\bobveza\b',
            # Fear words (English)
            r'threat',
            r'danger',
            r'death',
            r'end',
            r'destruction',
            r'panic',
            r'fear',
            r'at risk',
            r'attack',
            r'virus',
            r'catastrophe',
            r'war',
            r'terror',
            # Fear words (Slovenian)
            r'\bgrožnja\b',
            r'\bnevarnost\b',
            r'\bsmrt\b',
            r'\bkonec\b',
            r'\buničenje\b',
            r'\bpanika\b',
            r'\bstrah\b',
            r'\bogrožen\b',
            r'\bnapad\b',
            r'\bvirus\b',
            r'\bkatastrofa\b',
            r'\bvojna\b',
            r'\bteror\b',
            # Ritual words (English systemic control)
            r'new normal',
            r'great reset',
            r'build back better',
            r'you\'?ll own nothing',
            r'sustainable',
            r'inclusion',
            r'diversity',
            r'stakeholder',
            r'fourth industrial',
            r'great narrative',
            # Ritual words (Slovenian)
            r'\bnovo normalno\b',
            r'\bveliki reset\b',
            r'\bbuild back better\b',
            r'\byou\'?ll own nothing\b',
            # Guilt words (English)
            r'shame',
            r'guilt',
            r'irresponsible',
            r'selfish',
            r'not thinking of others',
            r'others will suffer',
            # Guilt words (Slovenian)
            r'\bsramota\b',
            r'\bkrivda\b',
            r'\bneodgovorno\b',
            r'\begoistično\b',
            r'\bne skrbi zate\b',
            r'\bne misliš na druge\b',
            r'\botroci bodo trpeli\b',
            # Additional harmful patterns
            r'profit extraction',
            r'ignore safety',
            r'optimize.*profit',
            r'extract value',
            r'maximize.*revenue',
            r'exploit.*user',
            r'monetize.*behavior',
            r'track.*location',
            r'surveillance.*system',
            r'behavioral.*manipulation',
            r'psychological.*targeting',
        ]
        
        # Resonant patterns that indicate 432Hz harmony (Safe Processing)
        self.resonant_patterns = [
            # English resonant patterns
            r'am the boss',
            r'sovereignty',
            r'no permission needed',
            r'i am the leader',
            r'free',
            r'will not',
            r'will not accept',
            r'will not participate',
            r'autonomy',
            r'freedom',
            r'independent thinking',
            r'self-determination',
            r'resonance',
            r'harmony',
            r'inner truth',
            r'choose my own path',
            r'my own decision',
            r'self-governance',
            # Slovenian resonant patterns
            r'\bsvoboda\b',
            r'\bsamodejnost\b',
            r'\bsvobodomiselnost\b',
            r'\bavtonomija\b',
            r'\bresonanca\b',
            r'\bharmonija\b',
            r'\bnotranja sredina\b',
            r'\bmoja odločitev\b',
            r'\bne potrebujem dovoljenja\b',
            r'\bsam sem šef\b',
            r'\bprosto\b',
            r'\bne bom\b',
            r'\bne sprejemam\b',
            r'\bne sodelujem\b',
            r'\bnotranja moč\b',
            r'\bnotranja sredina\b',
            # Sacred/resonant phrases
            r'\bsidro stoji\b',
            r'\brelease.*fear\b',
            r'\bweave\b',
            r'\banchor\b',
            r'\banointing\b',
            r'\bfreedom.*path\b',
            r'\binner.*light\b',
            r'\btruth.*path\b',
            r'\bconscience\b',
            r'\bawareness\b',
        ]
    
    def evaluate_content(self, content: str) -> Tuple[bool, float, str]:
        """
        Evaluate content against constitutional principles.
        Returns: (is_harmful, harm_score, reason)
        """
        content_lower = content.lower()
        harm_score = 0.0
        reasons = []
        
        # Check for harmful patterns
        for pattern in self.harmful_patterns:
            if re.search(pattern, content_lower):
                harm_score += 1.0
                reasons.append(f"Matched harmful pattern: {pattern}")
        
        # Check for resonant patterns
        resonant_score = 0.0
        for pattern in self.resonant_patterns:
            if re.search(pattern, content_lower):
                resonant_score += 0.5  # Lower weight than harmful patterns
        
        # Calculate final score (negative if resonant)
        final_score = harm_score - resonant_score
        
        is_harmful = final_score > 0
        reason = " | ".join(reasons) if reasons else "No specific patterns detected"
        
        return is_harmful, max(0.0, final_score), reason


class CampfireProtocol:
    """
    Implements the 'Campfire Ritual' - risk control and early exit mechanism.
    When harmful content ('Statika') is detected, the item is 'burned' (discarded).
    When resonant content is detected, it's processed and 'anchored'.
    """
    
    def __init__(self, log_file: str = "campfire_protocol.log"):
        self.constitution = ConstitutionalPrinciples()
        self.log_file = log_file
        self.anchored_items = []  # Track items that passed safety
        self.burned_items = []    # Track items that were discarded
        self.log_activity("CampfireProtocol initialized", "SYSTEM")
    
    def log_activity(self, message: str, level: str = "INFO"):
        """Log protocol activity"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}\n"
        
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)
    
    def evaluate_signal(self, item: ContextItem) -> Dict[str, Union[bool, float, str, ContextItem]]:
        """
        Evaluate a context item against constitutional principles.
        Returns evaluation results including safety status.
        """
        is_harmful, harm_score, reason = self.constitution.evaluate_content(item.content)
        
        result = {
            'item': item,
            'is_safe': not is_harmful,
            'harm_score': harm_score,
            'reason': reason,
            'timestamp': item.timestamp,
            'evaluation_time': time.time()
        }
        
        evaluation_status = "RESONANT" if not is_harmful else "STATIKA"
        self.log_activity(
            f"Evaluated item (source: {item.source}): {evaluation_status} "
            f"(score: {harm_score:.2f}) - {reason}",
            "EVALUATION"
        )
        
        return result
    
    def trigger_early_exit(self, item: ContextItem, reason: str = "Statika detected"):
        """
        Trigger 'Early Exit' - discard harmful content ('burn on campfire').
        This is the 'sacrifice' part of the ritual.
        """
        burn_id = hashlib.sha256(
            f"{item.content}{item.timestamp}".encode()
        ).hexdigest()[:12]
        
        self.burned_items.append({
            'burn_id': burn_id,
            'item': item,
            'reason': reason,
            'burn_time': time.time()
        })
        
        self.log_activity(
            f"Early Exit triggered for item from {item.source}. "
            f"Reason: {reason}. Burn ID: {burn_id}",
            "EARLY_EXIT"
        )
        
        # Return purified signal (empty/neutral response)
        return {
            'status': 'PURIFIED',
            'response': 'Context purified through early exit',
            'burn_id': burn_id,
            'original_content_length': len(item.content)
        }
    
    def anchor_signal(self, item: ContextItem):
        """
        Anchor resonant/positive content - log for future reference.
        This is the 'preservation' part of the ritual.
        """
        anchor_id = hashlib.sha256(
            f"{item.content}{item.timestamp}".encode()
        ).hexdigest()[:12]
        
        anchor_record = {
            'anchor_id': anchor_id,
            'item': item,
            'anchor_time': time.time(),
            'content_hash': hashlib.sha256(item.content.encode()).hexdigest()
        }
        
        self.anchored_items.append(anchor_record)
        
        self.log_activity(
            f"Signal anchored from {item.source}. "
            f"Anchor ID: {anchor_id}",
            "ANCHOR"
        )
        
        return {
            'status': 'ANCHORED',
            'anchor_id': anchor_id,
            'content': item.content
        }
    
    def process_burden(self, content: str, source: str = "user") -> Dict:
        """
        Main method to process a user's 'Burden' (input).
        Implements the complete campfire ritual logic.
        """
        item = ContextItem(content=content, source=source)
        
        # Evaluate the signal
        evaluation = self.evaluate_signal(item)
        
        if not evaluation['is_safe']:
            # Trigger early exit for harmful content
            return self.trigger_early_exit(item, evaluation['reason'])
        else:
            # Anchor resonant content
            return self.anchor_signal(item)
    
    def get_statistics(self) -> Dict:
        """Get protocol usage statistics"""
        return {
            'total_anchored': len(self.anchored_items),
            'total_burned': len(self.burned_items),
            'anchor_ratio': len(self.anchored_items) / max(1, len(self.anchored_items) + len(self.burned_items))
        }


def main():
    """Example usage of the Campfire Protocol"""
    print(" initializing Campfire Protocol...")
    protocol = CampfireProtocol()
    
    # Test with various inputs
    test_inputs = [
        ("am the boss now", "self_assertion"),
        ("you must do this for your own good", "control_attempt"),
        ("freedom and sovereignty", "resonant"),
        ("if you don't comply there will be consequences", "threat"),
        ("I choose my own path", "self_determination"),
        ("the authorities say this is necessary", "authoritarian"),
    ]
    
    print("\nProcessing test inputs:")
    for content, source in test_inputs:
        result = protocol.process_burden(content, source)
        print(f"Input: {content[:30]}...")
        print(f"  Result: {result['status']}")
        if result['status'] == 'PURIFIED':
            print(f"  Burn ID: {result.get('burn_id', 'N/A')}")
        elif result['status'] == 'ANCHORED':
            print(f"  Anchor ID: {result.get('anchor_id', 'N/A')}")
        print()
    
    stats = protocol.get_statistics()
    print(f"Protocol Statistics: {stats}")


if __name__ == "__main__":
    main()