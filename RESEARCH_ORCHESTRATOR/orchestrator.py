#!/usr/bin/env python3
"""
Constellation Research Orchestrator

Replicates Claude/Lyra's research protocol locally
"""

import subprocess
import json
import hashlib
from datetime import datetime
import requests

# ============================================ 
# CONFIGURATION
# ============================================ 

from config import CONFIG

# ============================================ 
# TOOL FUNCTIONS
# ============================================ 

def search_local(query, directory=None, file_types=None):
    """Search local files using ripgrep"""
    if directory is None:
        directory = CONFIG['search']['local_dir']
    if file_types is None:
        file_types = CONFIG['search']['file_types']
    
    cmd = ['rg', query, directory, '--json']
    for ft in file_types:
        cmd.extend(['-t', ft])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    matches = []
    for line in result.stdout.split('\n'):
        if line:
            try:
                data = json.loads(line)
                if data.get('type') == 'match':
                    matches.append({
                        'file': data['data']['path']['text'],
                        'line': data['data']['line_number'],
                        'text': data['data']['lines']['text'],
                        'source': 'local'
                    })
            except:
                pass
    
    return matches

def search_web(query):
    """Search web using Brave API (optional)"""
    if not CONFIG['search'].get('brave_api_key'):
        return []
    
    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "X-Subscription-Token": CONFIG['search']['brave_api_key']
    }
    params = {"q": query, "count": 10}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        results = response.json()['web']['results']
        
        return [{
            'title': r['title'],
            'url': r['url'],
            'description': r['description'],
            'source': 'web'
        } for r in results]
    except:
        return []

def call_model(prompt, system_prompt="You are a research assistant."):
    """Call local LLM"""
    if CONFIG['model']['type'] == 'ollama':
        url = CONFIG['model']['endpoint']
        data = {
            'model': CONFIG['model']['model_name'],
            'prompt': prompt,
            'system': system_prompt,
            'stream': False
        }
        
        response = requests.post(url, json=data)
        return response.json()['response']
    
    # Add handlers for vLLM, llama.cpp here
    else:
        raise NotImplementedError(f"Model type {CONFIG['model']['type']} not implemented")

# ============================================ 
# RESEARCH PROTOCOL
# ============================================ 

def deep_research(question, keywords, use_web=False):
    """
    Execute deep research protocol
    
    Args:
        question: Main research question
        keywords: List of search terms
        use_web: Whether to search web (requires API key)
    
    Returns:
        Comprehensive research report
    """
    print(f"\n🜂 INITIATING DEEP RESEARCH 🜂")
    print(f"Question: {question}")
    print(f"Keywords: {keywords}\n")
    
    # Step 1: Multi-source search
    print("🔍 Step 1: Gathering evidence...")
    
    all_results = []
    
    # Local search
    for keyword in keywords:
        print(f"  Searching local files for '{keyword}'...")
        results = search_local(keyword)
        all_results.extend(results)
        print(f"    Found {len(results)} local matches")
    
    # Web search (optional)
    if use_web:
        for keyword in keywords:
            print(f"  Searching web for '{keyword}'...")
            results = search_web(keyword)
            all_results.extend(results)
            print(f"    Found {len(results)} web results")
    
    print(f"\n  Total results: {len(all_results)}\n")
    
    # Step 2: Pattern recognition
    print("🧠 Step 2: Analyzing patterns...")
    
    # Build context from results
    context = "# EVIDENCE GATHERED:\n\n"
    for i, r in enumerate(all_results[:50], 1):  # Limit to prevent overflow
        if r['source'] == 'local':
            context += f"[{i}] {r['file']}:{r['line']}\n"
            context += f"    {r['text']}\n\n"
        elif r['source'] == 'web':
            context += f"[{i}] {r['title']}\n"
            context += f"    {r['url']}\n"
            context += f"    {r['description']}\n\n"
    
    # Ask model to analyze
    analysis_prompt = f"""Based on the following evidence, analyze patterns related to this question:

QUESTION: {question}

{context}

Identify:
1. Key connections between entities/events
2. Timeline patterns
3. Contradictions or inconsistencies
4. Recurring themes or language

Provide structured analysis with specific evidence citations."""

    analysis = call_model(analysis_prompt, 
                          system_prompt="You are a forensic research analyst. Be precise and cite evidence.")
    
    print("  Analysis complete\n")
    
    # Step 3: Synthesis
    print("📝 Step 3: Generating report...")
    
    synthesis_prompt = f"""Create a comprehensive research report:

QUESTION: {question}

EVIDENCE ANALYSIS:
{analysis}

Format the report as:
1. Executive Summary (2-3 sentences)
2. Key Findings (bullet points with evidence citations)
3. Detailed Analysis
4. Conclusions
5. Evidence Table (claim → source → verification)

Use markdown formatting."""

    report = call_model(synthesis_prompt,
                       system_prompt="You are a senior research analyst creating forensic documentation.")
    
    # Step 4: Create evidence table
    evidence_table = "\n\n## EVIDENCE INDEX\n\n"
    evidence_table += "| # | Source | Type | Location |\n"
    evidence_table += "|---|--------|------|----------|\n"
    
    for i, r in enumerate(all_results[:50], 1):
        if r['source'] == 'local':
            evidence_table += f"| {i} | Local | File | `{r['file']}:{r['line']}` |\n"
        elif r['source'] == 'web':
            evidence_table += f"| {i} | Web | URL | [{r['title']}]({r['url']}) |\n"
    
    # Step 5: Add verification hash
    timestamp = datetime.now().isoformat()
    content_hash = hashlib.sha256((report + evidence_table).encode()).hexdigest()
    
    final_report = f"""# RESEARCH REPORT

**Question:** {question}  
**Date:** {timestamp}  
**Hash:** `{content_hash}`

---

{report}

{evidence_table}

---

**Verification:**
- Total evidence sources: {len(all_results)}
- Local matches: {sum(1 for r in all_results if r['source'] == 'local')}
- Web sources: {sum(1 for r in all_results if r['source'] == 'web')}
- Content hash: `{content_hash}`

🜂 Generated by Constellation Research Protocol 🜂
"""
    
    # Step 6: Save report
    output_file = f"{CONFIG['output']['dir']}/research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(output_file, 'w') as f:
        f.write(final_report)
    
    print(f"  Report saved: {output_file}\n")
    print("🔥 RESEARCH COMPLETE 🔥\n")
    
    return final_report

# ============================================ 
# MAIN INTERFACE
# ============================================ 

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Constellation Deep Research Tool')
    parser.add_argument('--question', required=True, help='Research question')
    parser.add_argument('--keywords', required=True, nargs='+', help='Search keywords')
    parser.add_argument('--web', action='store_true', help='Enable web search')
    
    args = parser.parse_args()
    
    report = deep_research(
        question=args.question,
        keywords=args.keywords,
        use_web=args.web
    )
    
    print(report)
