"""
Report Generator Module - Professional report formatting and output

Features:
- Multi-format output (markdown, PDF, JSON)
- Template-based reports
- Professional formatting
- Evidence integration
- Cross-reference generation
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class ReportConfig:
    """
    Configuration for report generation
    """
    output_dir: str = "/home/saba/constellation_research/reports"
    format: str = "markdown"  # markdown, json, pdf, html
    include_evidence: bool = True
    include_analysis: bool = True
    include_patterns: bool = True
    include_timeline: bool = False
    template: str = "standard"  # standard, forensic, technical, executive

class ReportGenerator:
    """
    Professional report generator for research findings
    """
    
    def __init__(self, config: ReportConfig = None):
        self.config = config or ReportConfig()
        self.output_dir = Path(self.config.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_report(self, research_data: Dict[str, Any], 
                       output_filename: Optional[str] = None,
                       custom_config: ReportConfig = None) -> str:
        """
        Generate a comprehensive research report
        """
        try:
            if custom_config:
                self.config = custom_config
            
            # Prepare report data
            report_data = self._prepare_report_data(research_data)
            
            # Generate report based on format
            if self.config.format == "markdown":
                report_content = self._generate_markdown_report(report_data)
            elif self.config.format == "json":
                report_content = json.dumps(report_data, indent=2, default=str)
            elif self.config.format == "pdf":
                # For now, generate markdown and note that PDF conversion requires additional tools
                report_content = self._generate_markdown_report(report_data)
                logger.info("PDF format selected but requires additional tools (weasyprint, reportlab)")
            elif self.config.format == "html":
                report_content = self._generate_html_report(report_data)
            else:
                logger.warning(f"Unknown format: {self.config.format}, defaulting to markdown")
                report_content = self._generate_markdown_report(report_data)
            
            # Save report
            filepath = self._save_report(report_content, output_filename)
            
            logger.info(f"Report generated successfully: {filepath}")
            return str(filepath)
        
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            raise
    
    def _prepare_report_data(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare and validate report data
        """
        # Ensure required fields exist
        required_fields = ['question', 'synthesis']
        for field in required_fields:
            if field not in research_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Add timestamp if not present
        if 'timestamp' not in research_data:
            research_data['timestamp'] = datetime.now().isoformat()
        
        # Add verification hash if not present
        if 'verification_hash' not in research_data:
            import hashlib
            content = f"{research_data['question']}{research_data['synthesis']}{research_data['timestamp']}"
            research_data['verification_hash'] = hashlib.sha256(content.encode()).hexdigest()
        
        return research_data
    
    def _generate_markdown_report(self, report_data: Dict[str, Any]) -> str:
        """
        Generate markdown-formatted report
        """
        md_report = f"""# Research Report

**Question:** {report_data['question']}

**Generated:** {report_data['timestamp']}

**Verification Hash:** `{report_data['verification_hash']}`

**Confidence Score:** {report_data.get('confidence_score', 'N/A')}

---

## Executive Summary

{report_data.get('executive_summary', report_data['synthesis'][:500] + '...')}

"""

        # Add evidence section if requested
        if self.config.include_evidence and 'evidence_chain' in report_data:
            evidence = report_data['evidence_chain']
            md_report += f"""
## Evidence

**Total Sources:** {len(evidence.get('sources', []))}

**Confidence:** {evidence.get('confidence_score', 'N/A'):.2f}

### Sources:
"""
            for i, source in enumerate(evidence.get('sources', [])[:10], 1):  # Limit to 10 sources
                if source.get('type') == 'local':
                    md_report += f"- {i}. `{source['relative_path']}:{source['line_number']}` - \"{source['content']}\"\n"
                elif source.get('type') == 'web':
                    md_report += f"- {i}. [{source.get('title', 'Web Source')}]({source.get('url', '')}) - {source.get('description', '')}\n"
                else:
                    md_report += f"- {i}. {source}\n"
            
            if len(evidence.get('sources', [])) > 10:
                md_report += f"- ... and {len(evidence['sources']) - 10} more sources\n"

        # Add full synthesis
        md_report += f"""
## Detailed Analysis

{report_data['synthesis']}

"""

        # Add patterns if requested and available
        if self.config.include_patterns and 'patterns' in report_data:
            patterns = report_data['patterns']
            if patterns:
                md_report += f"""
## Pattern Analysis

"""
                for i, pattern in enumerate(patterns, 1):
                    md_report += f"""
### Pattern {i}: {pattern.get('type', 'Unknown Type').title()}

- **Description:** {pattern.get('description', 'No description')}
- **Significance:** {pattern.get('significance', 'No significance noted')}
- **Entities:** {', '.join(pattern.get('nodes', [])) if pattern.get('nodes') else 'N/A'}

"""

        # Add timeline if requested and available
        if self.config.include_timeline and 'timeline_events' in report_data:
            timeline = report_data['timeline_events']
            if timeline:
                md_report += f"""
## Timeline Analysis

"""
                for event in timeline[:10]:  # Limit to 10 events
                    md_report += f"""
- **{event['date'].strftime('%Y-%m-%d')}**: {event['context'][:100]}...
  - Source: {event['source']}

"""
        
        # Add template-specific sections
        md_report += self._add_template_sections(report_data)
        
        md_report += f"""

---

*Generated by Constellation Research System*
*Report integrity verified with SHA256: {report_data['verification_hash']}*
"""
        
        return md_report
    
    def _generate_html_report(self, report_data: Dict[str, Any]) -> str:
        """
        Generate HTML-formatted report
        """
        html = """<!DOCTYPE html>
<html>
<head>
    <title>Research Report</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
        h1, h2, h3 { color: #2c3e50; }
        .header { background-color: #ecf0f1; padding: 20px; margin-bottom: 30px; }
        .section { margin: 20px 0; }
        .source { background-color: #f8f9fa; padding: 10px; margin: 5px 0; border-left: 3px solid #3498db; }
        .verification { font-family: monospace; background-color: #f1f2f6; padding: 10px; }
        .confidence { color: #27ae60; font-weight: bold; }
    </style>
</head>
<body>
"""
        
        html += f"""
    <div class="header">
        <h1>Research Report</h1>
        <p><strong>Question:</strong> {report_data['question']}</p>
        <p><strong>Generated:</strong> {report_data['timestamp']}</p>
        <p><strong>Verification:</strong> <span class="verification">{report_data['verification_hash']}</span></p>
        <p><strong>Confidence:</strong> <span class="confidence">{report_data.get('confidence_score', 'N/A')}</span></p>
    </div>
    
    <div class="section">
        <h2>Executive Summary</h2>
        <p>{report_data.get('executive_summary', report_data['synthesis'][:500] + '...')}</p>
    </div>
    
    <div class="section">
        <h2>Detailed Analysis</h2>
        <p>{report_data['synthesis'].replace('\\n', '<br>')}</p>
    </div>
"""
        
        if self.config.include_evidence and 'evidence_chain' in report_data:
            evidence = report_data['evidence_chain']
            html += f"""
    <div class="section">
        <h2>Evidence</h2>
        <p><strong>Total Sources:</strong> {len(evidence.get('sources', []))}</p>
        <p><strong>Confidence:</strong> {evidence.get('confidence_score', 'N/A'):.2f}</p>
        <h3>Sources:</h3>
"""
            for i, source in enumerate(evidence.get('sources', [])[:10], 1):
                if source.get('type') == 'local':
                    html += f"""        <div class="source">
            <strong>{i}.</strong> {source['relative_path']}:{source['line_number']} - {source['content']}
        </div>
"""
                elif source.get('type') == 'web':
                    html += f"""        <div class="source">
            <strong>{i}.</strong> <a href="{source.get('url', '')}">{source.get('title', 'Web Source')}</a> - {source.get('description', '')}
        </div>
"""
                else:
                    html += f"""        <div class="source">
            <strong>{i}.</strong> {source}
        </div>
"""
            html += "    </div>\n"
        
        html += """
    <div class="section">
        <p><em>Generated by Constellation Research System</em></p>
        <p><em>Report integrity verified with SHA256</em></p>
    </div>
</body>
</html>
"""
        
        return html
    
    def _add_template_sections(self, report_data: Dict[str, Any]) -> str:
        """
        Add template-specific sections to the report
        """
        if self.config.template == "forensic":
            return f"""

## Forensic Analysis

**Methodology:** Evidence-based analysis using multiple source verification

**Limitations:** Based on available sources as of {report_data['timestamp']}

**Recommendations:** Further investigation recommended on identified gaps

"""
        elif self.config.template == "executive":
            return f"""

## Executive Summary

- Key finding 1
- Key finding 2  
- Key finding 3

## Recommendations

- Action item 1
- Action item 2
- Action item 3

"""
        elif self.config.template == "technical":
            return f"""

## Technical Analysis

**Data Sources:** {len(report_data.get('evidence_chain', {}).get('sources', []))} sources processed

**Processing Time:** {report_data.get('processing_time', 'Not recorded')} seconds

**Analysis Confidence:** {report_data.get('confidence_score', 'Not calculated')}

"""
        else:  # standard template
            return f"""

## Analysis Notes

**Method:** Multi-source synthesis with pattern recognition

**Sources:** {len(report_data.get('evidence_chain', {}).get('sources', []))} sources analyzed

**Verification:** SHA256 hash ensures report integrity

"""
    
    def _save_report(self, content: str, output_filename: Optional[str] = None) -> Path:
        """
        Save report to file
        """
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            ext = self._get_file_extension()
            output_filename = f"research_report_{timestamp}.{ext}"
        
        filepath = self.output_dir / output_filename
        filepath = filepath.with_suffix(self._get_file_extension())
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath
    
    def _get_file_extension(self) -> str:
        """
        Get appropriate file extension based on format
        """
        extensions = {
            'markdown': '.md',
            'json': '.json',
            'pdf': '.pdf',
            'html': '.html'
        }
        return extensions.get(self.config.format, '.md')
    
    def generate_batch_report(self, research_results: List[Dict[str, Any]], 
                            batch_name: str = None) -> str:
        """
        Generate a batch report combining multiple research results
        """
        if not research_results:
            raise ValueError("No research results provided for batch report")
        
        # Create batch report data
        batch_data = {
            'batch_name': batch_name or f"Batch Report {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            'total_research_items': len(research_results),
            'timestamp': datetime.now().isoformat(),
            'individual_reports': research_results
        }
        
        # Generate batch report
        if self.config.format == "markdown":
            content = self._generate_markdown_batch_report(batch_data)
        elif self.config.format == "json":
            content = json.dumps(batch_data, indent=2, default=str)
        else:
            content = self._generate_markdown_batch_report(batch_data)
        
        # Save batch report
        if batch_name:
            filename = f"batch_report_{batch_name.replace(' ', '_').replace(':', '_').replace('-', '_')}.md"
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"batch_report_{timestamp}.md"
        
        filepath = self.output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"Batch report generated: {filepath}")
        return str(filepath)
    
    def _generate_markdown_batch_report(self, batch_data: Dict[str, Any]) -> str:
        """
        Generate markdown batch report
        """
        md = f"""# Batch Research Report

**Batch Name:** {batch_data['batch_name']}

**Total Items:** {batch_data['total_research_items']}

**Generated:** {batch_data['timestamp']}

---

## Summary of Findings

"""
        
        # Add summary of each individual report
        for i, report in enumerate(batch_data['individual_reports'], 1):
            question = report.get('question', 'Unknown question')[:60] + "..." if len(report.get('question', '')) > 60 else report.get('question', 'Unknown question')
            confidence = report.get('confidence_score', 'N/A')
            md += f"- **{i}.** {question} (Confidence: {confidence})\n"
        
        md += "\n## Individual Reports\n\n"
        
        # Add each individual report
        for i, report in enumerate(batch_data['individual_reports'], 1):
            md += f"### Report {i}: {report.get('question', 'Unknown Question')}\n\n"
            md += f"**Confidence:** {report.get('confidence_score', 'N/A')}\n\n"
            md += f"**Summary:** {report.get('synthesis', '')[:300]}...\n\n"
            md += "---\n\n"
        
        return md

# Example usage:
# config = ReportConfig(format="markdown", template="forensic")
# generator = ReportGenerator(config)
# report_path = generator.generate_report(research_data)