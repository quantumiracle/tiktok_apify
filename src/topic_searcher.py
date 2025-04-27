"""
Topic Searcher Module - Implements search functionality for TikTok topics and hashtags
"""

import asyncio
import logging
import re
from urllib.parse import quote

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('topic_searcher')

class TopicSearcher:
    """
    Implements search functionality for finding TikTok influencers by topic/hashtag
    """
    
    def __init__(self, browser_manager):
        """
        Initialize the topic searcher with a browser manager
        
        Args:
            browser_manager (BrowserManager): Instance of BrowserManager for browser control
        """
        self.browser_manager = browser_manager
        self.base_url = "https://www.tiktok.com"
        self.search_results = []
        self.max_results = self.browser_manager.config.get('results_limit', 100)
    
    async def search_by_hashtag(self, hashtag):
        """
        Search TikTok by hashtag
        
        Args:
            hashtag (str): Hashtag to search for (without # symbol)
            
        Returns:
            list: List of profile URLs found
        """
        # Ensure hashtag doesn't have # prefix
        clean_hashtag = hashtag.strip().lstrip('#')
        search_url = f"{self.base_url}/tag/{quote(clean_hashtag)}"
        
        logger.info(f"Searching for hashtag: #{clean_hashtag}")
        
        # Navigate to hashtag page
        page = await self.browser_manager.navigate(search_url)
        
        # Handle login popup if it appears
        await self.browser_manager.handle_login_popup()
        
        # Scroll to load more content
        await self.browser_manager.scroll_page(scrolls=5)
        
        # Extract creator profiles from the hashtag page
        return await self._extract_profiles_from_page()
    
    async def search_by_keyword(self, keyword):
        """
        Search TikTok by keyword
        
        Args:
            keyword (str): Keyword to search for
            
        Returns:
            list: List of profile URLs found
        """
        search_url = f"{self.base_url}/search?q={quote(keyword)}"
        
        logger.info(f"Searching for keyword: {keyword}")
        
        # Navigate to search page
        page = await self.browser_manager.navigate(search_url)
        
        # Handle login popup if it appears
        await self.browser_manager.handle_login_popup()
        
        # Click on "Users" tab to filter for user profiles
        try:
            await page.click('text="Users"')
            await asyncio.sleep(2)
        except Exception as e:
            logger.warning(f"Could not click Users tab: {e}")
        
        # Scroll to load more content
        await self.browser_manager.scroll_page(scrolls=5)
        
        # Extract creator profiles from the search page
        return await self._extract_profiles_from_page()
    
    async def search_by_topic(self, topic):
        """
        Search TikTok by topic (tries both hashtag and keyword search)
        
        Args:
            topic (str): Topic to search for
            
        Returns:
            list: List of profile URLs found
        """
        logger.info(f"Searching for topic: {topic}")
        
        # Try hashtag search first
        hashtag_results = await self.search_by_hashtag(topic)
        
        # Then try keyword search
        keyword_results = await self.search_by_keyword(topic)
        
        # Combine and deduplicate results
        all_results = hashtag_results + keyword_results
        unique_results = list(dict.fromkeys(all_results))
        
        logger.info(f"Found {len(unique_results)} unique profiles for topic '{topic}'")
        
        return unique_results[:self.max_results]
    
    async def _extract_profiles_from_page(self):
        """
        Extract profile URLs from the current page
        
        Returns:
            list: List of profile URLs
        """
        profile_urls = []
        
        try:
            # Extract profile links using various selectors that might contain profile links
            selectors = [
                'a[href^="/@"]',  # Profile links typically start with /@username
                'a[data-e2e="user-card-avatar"]',
                'a[data-e2e="user-link"]'
            ]
            
            for selector in selectors:
                elements = await self.browser_manager.page.query_selector_all(selector)
                
                for element in elements:
                    href = await element.get_attribute('href')
                    
                    if href and href.startswith('/@'):
                        full_url = f"{self.base_url}{href}"
                        if full_url not in profile_urls:
                            profile_urls.append(full_url)
            
            logger.info(f"Extracted {len(profile_urls)} profile URLs")
            
        except Exception as e:
            logger.error(f"Error extracting profile URLs: {e}")
        
        return profile_urls
    
    async def get_top_influencers(self, topic, limit=None):
        """
        Get top influencers for a specific topic
        
        Args:
            topic (str): Topic to search for
            limit (int, optional): Maximum number of influencers to return
            
        Returns:
            list: List of profile URLs for top influencers
        """
        if limit is None:
            limit = self.max_results
        
        # Search for profiles by topic
        profiles = await self.search_by_topic(topic)
        
        # Limit results
        return profiles[:limit]
    
    async def get_multiple_topics(self, topics):
        """
        Get influencers for multiple topics
        
        Args:
            topics (list): List of topics to search for
            
        Returns:
            dict: Dictionary mapping topics to lists of profile URLs
        """
        results = {}
        
        for topic in topics:
            profiles = await self.get_top_influencers(topic)
            results[topic] = profiles
            
            # Add delay between topics to avoid rate limiting
            await asyncio.sleep(self.browser_manager.request_delay * 2)
        
        return results
