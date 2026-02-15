"""
Web Search Module - Optional web search functionality

Uses Brave Search API for web results
"""

import requests
from typing import List, Dict, Any, Optional

def search_web(query: str, api_key: Optional[str], num_results: int = 10) -> List[Dict[str, Any]]:
    """
    Search web using Brave API (optional)
    
    Args:
        query: Search query
        api_key: Brave API key (required)
        num_results: Number of results to return
    
    Returns:
        List of search results
    """
    if not api_key:
        return []
    
    try:
        url = "https://api.search.brave.com/res/v1/web/search"
        headers = {
            "X-Subscription-Token": api_key
        }
        params = {
            "q": query,
            "count": num_results
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            results = response.json()
            if 'web' in results and 'results' in results['web']:
                brave_results = []
                for item in results['web']['results']:
                    brave_results.append({
                        'title': item.get('title', ''),
                        'url': item.get('url', ''),
                        'description': item.get('description', ''),
                        'source': 'web',
                        'type': 'brave'
                    })
                return brave_results
        return []
    except Exception:
        return []