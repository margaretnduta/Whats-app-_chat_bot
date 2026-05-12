"""
Web Scraper Module
Responsible for scraping https://click2skill.com/ and caching the data
"""

import json
import os
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from config import Config


class WebScraper:
    """
    Scrapes and caches website content for the chatbot context.
    Implements caching to minimize API calls and improve performance.
    """
    
    # Headers to avoid being blocked by the website
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        " (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    def __init__(self, target_url=Config.TARGET_WEBSITE, cache_file=Config.CACHE_FILE):
        """
        Initialize the scraper
        
        Args:
            target_url: URL to scrape
            cache_file: Path to cache file for storing scraped data
        """
        self.target_url = target_url
        self.cache_file = cache_file
        self._ensure_cache_directory()
    
    def _ensure_cache_directory(self):
        """Create cache directory if it doesn't exist"""
        cache_dir = os.path.dirname(self.cache_file)
        if cache_dir and not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
    
    def _is_cache_valid(self):
        """
        Check if cached data is still valid based on expiry time
        
        Returns:
            bool: True if cache exists and is still valid
        """
        if not os.path.exists(self.cache_file):
            return False
        
        file_mod_time = datetime.fromtimestamp(os.path.getmtime(self.cache_file))
        expiry_time = file_mod_time + timedelta(minutes=Config.CACHE_EXPIRY_MINUTES)
        
        return datetime.now() < expiry_time
    
    def _load_from_cache(self):
        """
        Load scraped data from cache file
        
        Returns:
            dict: Cached data or None if cache doesn't exist
        """
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"❌ Error reading cache: {e}")
        
        return None
    
    def _save_to_cache(self, data):
        """
        Save scraped data to cache file
        
        Args:
            data: Dictionary containing scraped content
        """
        try:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"❌ Error writing to cache: {e}")
    
    def scrape_website(self, force_refresh=False):
        """
        Scrape website content with caching
        
        Args:
            force_refresh: If True, bypass cache and fetch fresh data
        
        Returns:
            str: Scraped content as text, or cached content if available
        """
        # Return cached data if valid and not forcing refresh
        if not force_refresh and self._is_cache_valid():
            cached_data = self._load_from_cache()
            if cached_data:
                print("✅ Using cached data (valid)")
                return cached_data.get("content", "")
        
        print("🔄 Fetching fresh data from website...")
        
        try:
            # Fetch the website with timeout
            response = requests.get(
                self.target_url,
                headers=self.HEADERS,
                timeout=10
            )
            response.raise_for_status()
            
            # Parse HTML content
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Extract text content (excluding scripts and styles)
            for script in soup(["script", "style"]):
                script.decompose()
            
            text = soup.get_text(separator="\n", strip=True)
            
            # Clean up excessive whitespace
            lines = [line.strip() for line in text.split("\n") if line.strip()]
            content = "\n".join(lines)
            
            # Cache the content
            cache_data = {
                "content": content,
                "timestamp": datetime.now().isoformat(),
                "url": self.target_url,
            }
            self._save_to_cache(cache_data)
            
            print(f"✅ Successfully scraped content ({len(content)} characters)")
            return content
        
        except requests.RequestException as e:
            print(f"❌ Error scraping website: {e}")
            
            # Try to return cached data as fallback
            cached_data = self._load_from_cache()
            if cached_data:
                print("⚠️  Returning cached data as fallback")
                return cached_data.get("content", "")
            
            return ""
    
    def get_relevant_context(self, query, content, max_length=3000):
        """
        Extract relevant portions of content based on the user's query.
        This reduces the context sent to OpenAI, saving on API costs.
        
        Args:
            query: User's question
            content: Full scraped content
            max_length: Maximum characters to return
        
        Returns:
            str: Relevant content snippet
        """
        # Split content into paragraphs
        paragraphs = content.split("\n\n")
        
        # Keywords from the query
        query_words = set(query.lower().split())
        
        # Score paragraphs based on keyword matches
        scored_paragraphs = []
        for para in paragraphs:
            para_lower = para.lower()
            score = sum(1 for word in query_words if word in para_lower)
            if score > 0:
                scored_paragraphs.append((score, para))
        
        # Sort by relevance (highest score first)
        scored_paragraphs.sort(reverse=True, key=lambda x: x[0])
        
        # Combine relevant paragraphs up to max_length
        result = ""
        for _, para in scored_paragraphs:
            if len(result) + len(para) < max_length:
                result += para + "\n\n"
            else:
                break
        
        return result if result else content[:max_length]
    
    def clear_cache(self):
        """Clear the cache file"""
        try:
            if os.path.exists(self.cache_file):
                os.remove(self.cache_file)
                print("✅ Cache cleared")
        except IOError as e:
            print(f"❌ Error clearing cache: {e}")


# Global scraper instance
_scraper = None


def get_scraper():
    """Get or create the global scraper instance"""
    global _scraper
    if _scraper is None:
        _scraper = WebScraper()
    return _scraper


def get_scraped_content(force_refresh=False):
    """
    Convenience function to get scraped content
    
    Args:
        force_refresh: Force fetch fresh data
    
    Returns:
        str: Scraped website content
    """
    return get_scraper().scrape_website(force_refresh=force_refresh)
