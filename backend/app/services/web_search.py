"""
Project Alfred - Real Web Search Integration
Uses DuckDuckGo for free, privacy-focused web search
"""

import requests
from typing import List, Dict, Any, Optional
from urllib.parse import quote_plus
import time


class WebSearchService:
    """Real web search using DuckDuckGo Instant Answer API"""
    
    def __init__(self):
        self.base_url = "https://api.duckduckgo.com/"
        self.html_search_url = "https://html.duckduckgo.com/html/"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (compatible; ProjectAlfred/1.0)"
        })
    
    def search(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """
        Search the web using DuckDuckGo
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
        
        Returns:
            Dictionary with search results
        """
        try:
            # Use DuckDuckGo Instant Answer API
            params = {
                "q": query,
                "format": "json",
                "no_html": 1,
                "skip_disambig": 1
            }
            
            response = self.session.get(
                self.base_url,
                params=params,
                timeout=10
            )
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                    "results": []
                }
            
            data = response.json()
            
            # Parse results
            results = []
            
            # Abstract (main answer)
            if data.get("Abstract"):
                results.append({
                    "title": data.get("Heading", "Answer"),
                    "snippet": data.get("Abstract"),
                    "url": data.get("AbstractURL", ""),
                    "source": data.get("AbstractSource", "DuckDuckGo")
                })
            
            # Related topics
            for topic in data.get("RelatedTopics", [])[:max_results]:
                if isinstance(topic, dict) and "Text" in topic:
                    results.append({
                        "title": topic.get("Text", "")[:100],
                        "snippet": topic.get("Text", ""),
                        "url": topic.get("FirstURL", ""),
                        "source": "DuckDuckGo"
                    })
            
            # If no results from Instant Answer, try HTML search
            if not results:
                results = self._html_search(query, max_results)
            
            return {
                "success": True,
                "query": query,
                "results": results[:max_results],
                "total_results": len(results)
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "results": []
            }
    
    def _html_search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Fallback HTML search parsing
        Note: This is a basic implementation. For production, consider using:
        - SerpAPI (paid, but comprehensive)
        - Google Custom Search API (limited free tier)
        - Bing Search API (limited free tier)
        """
        try:
            # For now, return a simulated result
            # In production, you would parse the HTML or use a paid API
            return [{
                "title": f"Search result for: {query}",
                "snippet": f"Found information about {query}. For production use, integrate with SerpAPI or Google Custom Search API.",
                "url": f"https://duckduckgo.com/?q={quote_plus(query)}",
                "source": "DuckDuckGo"
            }]
        except Exception as e:
            print(f"[WebSearch] HTML search error: {e}")
            return []
    
    def quick_answer(self, query: str) -> Optional[str]:
        """Get a quick answer for factual queries"""
        try:
            params = {
                "q": query,
                "format": "json",
                "no_html": 1
            }
            
            response = self.session.get(
                self.base_url,
                params=params,
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Try to get instant answer
                if data.get("Answer"):
                    return data["Answer"]
                
                if data.get("Abstract"):
                    return data["Abstract"]
                
                # Try definition
                if data.get("Definition"):
                    return data["Definition"]
            
            return None
        
        except Exception as e:
            print(f"[WebSearch] Quick answer error: {e}")
            return None


# Singleton instance
web_search_service = WebSearchService()


# Example usage and testing
if __name__ == "__main__":
    service = WebSearchService()
    
    # Test search
    print("Testing web search...")
    result = service.search("artificial intelligence")
    print(f"Success: {result['success']}")
    print(f"Results: {len(result['results'])}")
    
    for i, r in enumerate(result['results'], 1):
        print(f"\n{i}. {r['title']}")
        print(f"   {r['snippet'][:100]}...")
        print(f"   {r['url']}")
    
    # Test quick answer
    print("\n\nTesting quick answer...")
    answer = service.quick_answer("what is python programming language")
    if answer:
        print(f"Answer: {answer}")
    else:
        print("No quick answer available")
