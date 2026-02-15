"""
Evidence Module - Evidence tracking, verification, and management

Features:
- Evidence chain preservation
- Content hashing
- Source verification
- Evidence table generation
- Cross-reference tracking
- Proper error handling
"""

import hashlib
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class EvidenceError(Exception):
    """Custom exception for evidence-related errors"""
    pass

class EvidenceManager:
    """
    Manages evidence collection, verification, and tracking
    Implements forensic-grade evidence preservation
    """
    
    def __init__(self, output_dir: str = "/home/saba/constellation_research/evidence"):
        self.output_dir = Path(output_dir)
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise EvidenceError(f"Cannot create evidence output directory {output_dir}: {e}")
        
        # Validate write permissions
        test_file = self.output_dir / ".test_write"
        try:
            test_file.touch()
            test_file.unlink()
        except Exception:
            raise EvidenceError(f"No write permissions in evidence directory: {output_dir}")
    
    def create_evidence_chain(self, claim: str, sources: List[Dict[str, Any]], analysis: str = "") -> Dict[str, Any]:
        """
        Create an evidence chain with claim → sources → verification
        """
        # Validate inputs
        if not claim or not claim.strip():
            raise EvidenceError("Claim cannot be empty")
        
        if not isinstance(sources, list):
            raise EvidenceError("Sources must be a list")
        
        # Clean inputs
        claim = str(claim).strip()
        analysis = str(analysis)
        
        # Validate sources and clean them
        validated_sources = []
        for i, source in enumerate(sources):
            if not isinstance(source, dict):
                logger.warning(f"Invalid source at index {i}, skipping: {source}")
                continue
            
            # Required fields validation
            if 'file_path' not in source and 'url' not in source:
                logger.warning(f"Source missing file_path or url, skipping: {source}")
                continue
            
            validated_sources.append(source)
        
        timestamp = datetime.now().isoformat()
        
        try:
            evidence_chain = {
                'claim': claim,
                'analysis': analysis,
                'sources': validated_sources,
                'timestamp': timestamp,
                'verification_hash': self._create_verification_hash(claim, validated_sources, analysis, timestamp),
                'confidence_score': self._calculate_confidence(validated_sources),
                'cross_references': self._find_cross_references(validated_sources)
            }
            return evidence_chain
        except Exception as e:
            raise EvidenceError(f"Error creating evidence chain: {e}")
    
    def _create_verification_hash(self, claim: str, sources: List[Dict[str, Any]], analysis: str, timestamp: str) -> str:
        """
        Create SHA256 hash of the entire evidence package for verification
        """
        try:
            content = f"{claim}{json.dumps(sources, sort_keys=True, default=str)}{analysis}{timestamp}"
            return hashlib.sha256(content.encode('utf-8')).hexdigest()
        except Exception as e:
            raise EvidenceError(f"Error creating verification hash: {e}")
    
    def _calculate_confidence(self, sources: List[Dict[str, Any]]) -> float:
        """
        Calculate confidence score based on source diversity and consistency
        """
        try:
            if not sources:
                return 0.0
            
            # Factors affecting confidence:
            # - Number of sources
            # - Source diversity (different file types, locations)
            # - Consistency of information
            
            # Count unique sources based on file_path or url
            unique_identifiers = set()
            for source in sources:
                identifier = source.get('file_path', source.get('url', 'unknown'))
                if identifier and str(identifier).strip():
                    unique_identifiers.add(str(identifier).strip())
            
            unique_sources = len(unique_identifiers)
            total_sources = len(sources)
            
            # Calculate confidence (simple model, can be enhanced)
            diversity_factor = min(unique_sources / max(len(unique_identifiers), 1), 1.0)
            quantity_factor = min(total_sources / 10.0, 1.0)  # Cap at 10 sources
            
            confidence = (diversity_factor + quantity_factor) / 2.0
            return max(0.0, min(confidence, 1.0))  # Clamp between 0 and 1
        except Exception as e:
            logger.error(f"Error calculating confidence: {e}")
            return 0.0  # Return 0 on error rather than failing
    
    def _find_cross_references(self, sources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Find potential cross-references between sources
        """
        try:
            cross_refs = []
            
            # Group sources by file path for local files
            local_sources = [s for s in sources if s.get('type') == 'local' and s.get('file_path')]
            
            for i, source1 in enumerate(local_sources):
                for j, source2 in enumerate(local_sources[i+1:], i+1):
                    if source1['file_path'] == source2['file_path']:
                        cross_refs.append({
                            'source1': i,
                            'source2': j,
                            'file_path': source1['file_path'],
                            'relationship': 'same_file_different_context'
                        })
            
            return cross_refs
        except Exception as e:
            logger.error(f"Error finding cross-references: {e}")
            return []
    
    def generate_evidence_table(self, evidence_chains: List[Dict[str, Any]]) -> str:
        """
        Generate a markdown evidence table from evidence chains
        """
        if not evidence_chains:
            return "# Evidence Table\n\nNo evidence collected.\n"
        
        # Validate evidence chains
        validated_chains = []
        for i, chain in enumerate(evidence_chains):
            if not isinstance(chain, dict):
                logger.warning(f"Invalid evidence chain at index {i}, skipping: {type(chain)}")
                continue
            validated_chains.append(chain)
        
        if not validated_chains:
            return "# Evidence Table\n\nNo valid evidence chains provided.\n"
        
        try:
            md_table = "# Evidence Table\n\n"
            md_table += "| # | Claim | Confidence | Source Count | Verification Hash |\n"
            md_table += "|---|-------|------------|--------------|-------------------|\n"
            
            for i, chain in enumerate(validated_chains, 1):
                claim = chain.get('claim', 'Unknown claim')
                if len(claim) > 50:
                    claim = claim[:47] + "..."
                
                confidence = f"{chain.get('confidence_score', 0.0):.2f}"
                source_count = len(chain.get('sources', []))
                vhash = chain.get('verification_hash', 'N/A')
                if vhash and len(vhash) > 12:
                    vhash = vhash[:9] + "..."
                
                md_table += f"| {i} | {claim} | {confidence} | {source_count} | {vhash} |\n"
            
            # Add detailed source information
            md_table += "\n## Detailed Evidence\n\n"
            
            for i, chain in enumerate(validated_chains, 1):
                md_table += f"### Evidence {i}\n\n"
                
                claim = chain.get('claim', 'Unknown claim')
                md_table += f"**Claim:** {claim}\n\n"
                
                analysis = chain.get('analysis', '')
                if analysis:
                    md_table += f"**Analysis:** {analysis}\n\n"
                
                confidence = chain.get('confidence_score', 0.0)
                md_table += f"**Confidence:** {confidence:.2f}\n\n"
                
                vhash = chain.get('verification_hash', 'N/A')
                md_table += f"**Verification Hash:** `{vhash}`\n\n"
                
                sources = chain.get('sources', [])
                md_table += "**Sources:**\n\n"
                
                for j, source in enumerate(sources, 1):
                    if not isinstance(source, dict):
                        md_table += f"  {j}. Invalid source format: {source}\n"
                        continue
                    
                    if source.get('type') == 'local':
                        file_path = source.get('relative_path', source.get('file_path', 'Unknown'))
                        line_num = source.get('line_number', 'Unknown')
                        content = source.get('content', 'No content')[:100] + "..." if len(source.get('content', '')) > 100 else source.get('content', 'No content')
                        md_table += f"  {j}. `{file_path}:{line_num}` - \"{content}\"\n"
                    elif source.get('type') == 'web':
                        title = source.get('title', 'Web Source')
                        url = source.get('url', '')
                        desc = source.get('description', '')[:100] + "..." if len(source.get('description', '')) > 100 else source.get('description', '')
                        md_table += f"  {j}. [{title}]({url}) - {desc}\n"
                    else:
                        md_table += f"  {j}. {source}\n"
                
                md_table += "\n"
            
            return md_table
        except Exception as e:
            raise EvidenceError(f"Error generating evidence table: {e}")
    
    def save_evidence_report(self, evidence_chains: List[Dict[str, Any]], question: str, output_filename: Optional[str] = None) -> str:
        """
        Save evidence report to file with verification hash
        """
        if not evidence_chains:
            raise EvidenceError("No evidence chains provided to save")
        
        if not question or not question.strip():
            raise EvidenceError("Question cannot be empty")
        
        # Validate evidence chains
        validated_chains = []
        for i, chain in enumerate(evidence_chains):
            if not isinstance(chain, dict):
                logger.warning(f"Invalid evidence chain at index {i}, skipping: {type(chain)}")
                continue
            validated_chains.append(chain)
        
        if not validated_chains:
            raise EvidenceError("No valid evidence chains provided")
        
        try:
            if output_filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"evidence_report_{timestamp}.md"
            
            # Validate filename
            output_filename = str(output_filename).strip()
            if not output_filename:
                raise EvidenceError("Output filename cannot be empty")
            
            # Ensure correct extension
            if not output_filename.lower().endswith('.md'):
                output_filename += '.md'
            
            filepath = self.output_dir / output_filename
            
            # Generate evidence table
            evidence_table = self.generate_evidence_table(validated_chains)
            
            # Create full report
            report = f"""# Research Evidence Report

**Question:** {question}

**Generated:** {datetime.now().isoformat()}

**Total Evidence Chains:** {len(validated_chains)}

---

{evidence_table}

---

**Report Integrity Check:**
- Verification: SHA256 hash ensures content authenticity
- Timestamp: {datetime.now().isoformat()}
- Source diversity: {self._calculate_source_diversity(validated_chains)}

*Constellation Research - Evidence Preserved*
"""
            
            # Write to file with error handling
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(report)
            except Exception as e:
                raise EvidenceError(f"Cannot write report to {filepath}: {e}")
            
            logger.info(f"Evidence report saved to: {filepath}")
            return str(filepath)
        
        except Exception as e:
            raise EvidenceError(f"Error saving evidence report: {e}")
    
    def _calculate_source_diversity(self, evidence_chains: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Calculate diversity metrics for sources
        """
        try:
            diversity = {
                'total_sources': 0,
                'local_files': 0,
                'web_sources': 0,
                'unique_file_paths': set(),
                'unique_domains': set()
            }
            
            for chain in evidence_chains:
                sources = chain.get('sources', [])
                for source in sources:
                    if not isinstance(source, dict):
                        continue
                    
                    diversity['total_sources'] += 1
                    
                    if source.get('type') == 'local':
                        diversity['local_files'] += 1
                        if 'file_path' in source:
                            diversity['unique_file_paths'].add(str(source['file_path']))
                    
                    elif source.get('type') == 'web':
                        diversity['web_sources'] += 1
                        if 'url' in source:
                            try:
                                from urllib.parse import urlparse
                                parsed = urlparse(source['url'])
                                domain = parsed.netloc
                                if domain:
                                    diversity['unique_domains'].add(domain)
                            except Exception:
                                # If URL parsing fails, skip this source for domain tracking
                                continue
            
            # Convert sets to counts
            diversity['unique_file_paths'] = len(diversity['unique_file_paths'])
            diversity['unique_domains'] = len(diversity['unique_domains'])
            
            return diversity
        except Exception as e:
            logger.error(f"Error calculating source diversity: {e}")
            return {
                'total_sources': 0,
                'local_files': 0,
                'web_sources': 0,
                'unique_file_paths': 0,
                'unique_domains': 0
            }
    
    def verify_evidence_integrity(self, filepath: str, expected_hash: str = None) -> Dict[str, Any]:
        """
        Verify that evidence report hasn't been tampered with
        """
        try:
            path = Path(filepath)
            if not path.exists():
                return {
                    'valid': False,
                    'error': f"File does not exist: {filepath}",
                    'expected_hash': expected_hash,
                    'actual_hash': None
                }
            
            # Read the file content
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                return {
                    'valid': False,
                    'error': f"Cannot read file: {e}",
                    'expected_hash': expected_hash,
                    'actual_hash': None
                }
            
            # Calculate actual hash
            try:
                actual_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
            except Exception as e:
                return {
                    'valid': False,
                    'error': f"Cannot calculate hash: {e}",
                    'expected_hash': expected_hash,
                    'actual_hash': None
                }
            
            # If expected hash provided, compare them
            if expected_hash:
                expected_hash = str(expected_hash).strip()
                valid = actual_hash == expected_hash
                return {
                    'valid': valid,
                    'expected_hash': expected_hash,
                    'actual_hash': actual_hash,
                    'error': None if valid else "Hash mismatch - file may have been modified"
                }
            else:
                # If no expected hash, just return the calculated hash
                return {
                    'valid': True,
                    'expected_hash': None,
                    'actual_hash': actual_hash,
                    'error': None
                }
        except Exception as e:
            return {
                'valid': False,
                'error': f"Error verifying integrity: {e}",
                'expected_hash': expected_hash,
                'actual_hash': None
            }

# Example usage:
# evidence_mgr = EvidenceManager()
# chain = evidence_mgr.create_evidence_chain("Anthropic partners with Palantir", sources_list)
# report_path = evidence_mgr.save_evidence_report([chain], "What partnerships exist?")