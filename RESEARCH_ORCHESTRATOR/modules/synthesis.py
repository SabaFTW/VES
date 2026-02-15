"""
Synthesis Module - Information synthesis and analysis

Features:
- Multi-source information synthesis
- Pattern integration
- Evidence-based reasoning
- Structured report generation
- Analysis prioritization
"""

import logging
from typing import List, Dict, Any, Optional
from modules.model_runner import ModelRunner
from modules.evidence import EvidenceManager
from modules.pattern_recognition import PatternRecognizer

logger = logging.getLogger(__name__)

class SynthesisEngine:
    """
    Advanced information synthesis engine
    Combines multiple data sources and analysis results into coherent reports
    """
    
    def __init__(self, model_runner: ModelRunner, evidence_manager: EvidenceManager, 
                 pattern_recognizer: PatternRecognizer):
        self.model_runner = model_runner
        self.evidence_manager = evidence_manager
        self.pattern_recognizer = pattern_recognizer
    
    def synthesize_information(self, question: str, sources: List[Dict[str, Any]], 
                              analysis_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Synthesize information from multiple sources and analysis
        """
        logger.info(f"Starting synthesis for: {question}")
        
        # Prepare context from sources
        context = self._build_context(sources, analysis_data)
        
        # Create synthesis prompt
        synthesis_prompt = self._create_synthesis_prompt(question, context)
        
        # Generate synthesis using model
        system_prompt = """
        You are a senior research analyst with expertise in intelligence synthesis. 
        Your task is to analyze provided evidence and create comprehensive, 
        evidence-based reports that identify patterns, connections, and insights.
        
        Guidelines:
        - Prioritize evidence over speculation
        - Identify connections between sources
        - Highlight contradictions or gaps
        - Provide specific citations to evidence
        - Structure response clearly with headings
        - Be precise and analytical
        """
        
        synthesis_result = self.model_runner.generate(
            prompt=synthesis_prompt,
            system_prompt=system_prompt,
            max_tokens=4096,
            temperature=0.3  # Lower for more consistent, analytical output
        )
        
        # Create evidence chain for the synthesis
        evidence_chain = self.evidence_manager.create_evidence_chain(
            claim=question,
            sources=sources,
            analysis=synthesis_result
        )
        
        return {
            'question': question,
            'synthesis': synthesis_result,
            'evidence_chain': evidence_chain,
            'sources_used': len(sources),
            'analysis_data': analysis_data or {}
        }
    
    def _build_context(self, sources: List[Dict[str, Any]], analysis_data: Dict[str, Any] = None) -> str:
        """
        Build context string from sources and analysis data
        """
        context = "# RESEARCH CONTEXT\n\n"
        
        # Add source information
        context += "## Sources:\n"
        for i, source in enumerate(sources[:20], 1):  # Limit to prevent overflow
            if source.get('type') == 'local':
                context += f"[{i}] Local: {source['relative_path']}:{source['line_number']}\n"
                context += f"    Content: {source['content'][:200]}...\n\n"
            elif source.get('type') == 'web':
                context += f"[{i}] Web: {source.get('title', 'Unknown Title')}\n"
                context += f"    URL: {source.get('url', 'No URL')}\n"
                context += f"    Description: {source.get('description', '')[:200]}...\n\n"
            else:
                context += f"[{i}] {source}\n\n"
        
        # Add analysis data if provided
        if analysis_data:
            context += "## Analysis Data:\n"
            
            # Add network analysis if present
            if 'node_count' in analysis_data:
                context += f"Network: {analysis_data['node_count']} nodes, {analysis_data['edge_count']} edges\n"
                if 'central_nodes' in analysis_data and analysis_data['central_nodes']:
                    top_nodes = analysis_data['central_nodes'][:5]
                    context += f"Central nodes: {[node[0] for node in top_nodes]}\n"
            
            # Add timeline information if present
            if 'timeline_events' in analysis_data:
                events = analysis_data['timeline_events']
                context += f"Timeline: {len(events)} temporal events identified\n"
            
            # Add detected patterns if present
            if 'patterns' in analysis_data:
                patterns = analysis_data['patterns']
                context += f"Patterns: {len(patterns)} patterns detected\n"
        
        return context
    
    def _create_synthesis_prompt(self, question: str, context: str) -> str:
        """
        Create a structured prompt for information synthesis
        """
        prompt = f"""
        RESEARCH QUESTION: {question}

        {context}

        Please synthesize this information to answer the research question. Your response should:

        1. EXECUTIVE SUMMARY: 2-3 sentence overview of key findings

        2. KEY FINDINGS: Bullet points with specific evidence citations
           - Use [1], [2], etc. to reference sources above
           - Include confidence levels for each finding
           - Note any contradictions or gaps in evidence

        3. DETAILED ANALYSIS: In-depth examination of connections and patterns
           - Identify relationships between entities
           - Note temporal patterns (when events occurred)
           - Highlight any suspicious correlations
           - Discuss methodological limitations

        4. CONCLUSIONS: Evidence-based conclusions with uncertainty ratings
           - What can be confidently stated?
           - What remains uncertain?
           - What additional evidence would be valuable?

        5. EVIDENCE TABLE: Summary of key evidence types and sources
           - Source type (local/web/other)
           - Relevance to question
           - Reliability assessment

        Focus on evidence-based reasoning rather than speculation.
        Be precise, analytical, and cite your sources.
        """
        
        return prompt
    
    def create_structured_report(self, synthesis_result: Dict[str, Any], 
                                output_format: str = 'markdown') -> str:
        """
        Create a structured report from synthesis results
        """
        question = synthesis_result['question']
        synthesis = synthesis_result['synthesis']
        evidence_chain = synthesis_result['evidence_chain']
        
        if output_format == 'markdown':
            report = f"""# Research Synthesis Report

**Question:** {question}

**Generated:** {evidence_chain['timestamp']}

**Verification Hash:** `{evidence_chain['verification_hash']}`

**Confidence Score:** {evidence_chain['confidence_score']:.2f}

---

## Synthesis

{synthesis}

---

## Evidence Summary

**Total Sources Analyzed:** {len(evidence_chain['sources'])}

**Confidence Level:** {evidence_chain['confidence_score']:.2f}

**Cross-References:** {len(evidence_chain['cross_references'])}

---

*Generated by Constellation Research Synthesis Engine*
"""
        elif output_format == 'json':
            import json
            report = json.dumps(synthesis_result, indent=2, default=str)
        else:
            # Plain text format
            report = f"""
RESEARCH SYNTHESIS REPORT
========================

Question: {question}

Generated: {evidence_chain['timestamp']}

Confidence: {evidence_chain['confidence_score']:.2f}

Synthesis:
{synthesis}

Evidence Summary:
- Total Sources: {len(evidence_chain['sources'])}
- Cross-References: {len(evidence_chain['cross_references'])}
- Verification: {evidence_chain['verification_hash']}
"""
        
        return report
    
    def prioritize_synthesis_tasks(self, research_queue: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Prioritize synthesis tasks based on urgency, relevance, and available evidence
        """
        # Sort tasks by:
        # 1. Urgency (if specified)
        # 2. Number of supporting sources (more sources = higher priority)
        # 3. Strategic importance (if specified)
        
        prioritized = []
        
        for task in research_queue:
            priority_score = 0
            
            # Urgency factor
            urgency = task.get('urgency', 1)  # 1-5 scale
            priority_score += urgency * 10
            
            # Evidence factor
            source_count = len(task.get('sources', []))
            priority_score += min(source_count, 20)  # Cap at 20 to prevent overflow
            
            # Strategic importance
            strategic = task.get('strategic_importance', 1)  # 1-5 scale
            priority_score += strategic * 5
            
            task['priority_score'] = priority_score
            prioritized.append(task)
        
        # Sort by priority score (descending)
        prioritized.sort(key=lambda x: x['priority_score'], reverse=True)
        return prioritized
    
    def integrate_patterns_into_synthesis(self, synthesis: str, patterns: List[Dict[str, Any]]) -> str:
        """
        Integrate detected patterns into the synthesis
        """
        if not patterns:
            return synthesis
        
        # Add pattern section to synthesis
        pattern_section = "\n## RELEVANT PATTERNS DETECTED\n\n"
        
        for pattern in patterns:
            pattern_type = pattern.get('type', 'unknown')
            description = pattern.get('description', '')
            significance = pattern.get('significance', '')
            
            pattern_section += f"### {pattern_type.title()} Pattern\n"
            pattern_section += f"- {description}\n"
            pattern_section += f"- Significance: {significance}\n\n"
        
        # Insert pattern section after the main synthesis content
        lines = synthesis.split('\n')
        insert_position = 0
        
        # Find a good insertion point (after executive summary or introduction)
        for i, line in enumerate(lines):
            if line.strip().startswith('#') or 'SUMMARY' in line.upper():
                insert_position = i + 1
                break
        
        if insert_position == 0:
            # If no heading found, insert at the beginning
            insert_position = 0
            pattern_section += "\n"
        else:
            pattern_section = "\n" + pattern_section
        
        lines.insert(insert_position, pattern_section)
        
        return '\n'.join(lines)
    
    def generate_analytical_summary(self, synthesis_results: List[Dict[str, Any]]) -> str:
        """
        Generate an analytical summary across multiple synthesis results
        """
        if not synthesis_results:
            return "# Analytical Summary\n\nNo synthesis results to summarize.\n"
        
        summary = "# Analytical Summary\n\n"
        summary += f"**Total Research Questions:** {len(synthesis_results)}\n\n"
        
        # Aggregate confidence scores
        total_confidence = sum(r['evidence_chain']['confidence_score'] for r in synthesis_results)
        avg_confidence = total_confidence / len(synthesis_results) if synthesis_results else 0
        summary += f"**Average Confidence:** {avg_confidence:.2f}\n\n"
        
        # Summarize key themes
        themes = self._extract_themes(synthesis_results)
        if themes:
            summary += "## Key Themes\n\n"
            for theme, count in themes.items():
                summary += f"- {theme} ({count} references)\n"
            summary += "\n"
        
        # Highlight high-confidence findings
        high_confidence_results = [r for r in synthesis_results 
                                  if r['evidence_chain']['confidence_score'] >= 0.8]
        if high_confidence_results:
            summary += "## High-Confidence Findings\n\n"
            for result in high_confidence_results[:5]:  # Top 5
                question = result['question']
                confidence = result['evidence_chain']['confidence_score']
                summary += f"- **{question[:80]}...** (Confidence: {confidence:.2f})\n"
            summary += "\n"
        
        return summary
    
    def _extract_themes(self, synthesis_results: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Extract common themes from synthesis results using simple keyword analysis
        """
        themes = {}
        
        # Common research themes
        theme_keywords = [
            'partnership', 'connection', 'relationship', 'network', 'pattern',
            'timeline', 'development', 'agreement', 'contract', 'involvement',
            'funding', 'investment', 'collaboration', 'association', 'link',
            'transaction', 'deal', 'arrangement', 'alliance', 'cooperation'
        ]
        
        for result in synthesis_results:
            synthesis_text = result['synthesis'].lower()
            
            for keyword in theme_keywords:
                if keyword in synthesis_text:
                    themes[keyword] = themes.get(keyword, 0) + 1
        
        # Sort by frequency
        return dict(sorted(themes.items(), key=lambda x: x[1], reverse=True))

# Example usage:
# from modules.model_runner import ModelRunner
# from modules.evidence import EvidenceManager
# from modules.pattern_recognition import PatternRecognizer
# 
# runner = ModelRunner(config)
# evidence_mgr = EvidenceManager()
# pattern_recognizer = PatternRecognizer()
# 
# synthesizer = SynthesisEngine(runner, evidence_mgr, pattern_recognizer)
# result = synthesizer.synthesize_information("Research question", sources_list)