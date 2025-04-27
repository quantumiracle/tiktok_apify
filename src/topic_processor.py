"""
Topic Processor Module - Handles searching TikTok by topic (hashtag)
"""

import logging
from typing import List, Dict, Any, Set

from .api_client import ApiClient

logger = logging.getLogger(__name__)

class TopicProcessor:
    """
    Handles the logic for searching TikTok based on topics (hashtags)
    and identifying relevant user profiles.
    """
    
    def __init__(self, api_client: ApiClient, results_per_hashtag: int = 50):
        """
        Initializes the TopicProcessor.
        
        Args:
            api_client (ApiClient): Instance of the ApiClient for making API calls.
            results_per_hashtag (int): Number of video results to fetch per hashtag.
        """
        self.api_client = api_client
        self.results_per_hashtag = results_per_hashtag
        
    def get_profiles_from_topic(self, topic: str) -> Set[str]:
        """
        Searches a topic (hashtag) and extracts unique author usernames.
        
        Args:
            topic (str): The topic (hashtag) to search for.
            
        Returns:
            Set[str]: A set of unique author usernames found for the topic.
        """
        logger.info(f"Processing topic (hashtag): {topic}")
        unique_usernames = set()
        
        try:
            # Search for videos using the hashtag
            video_results = self.api_client.search_by_hashtag(
                hashtag=topic,
                results_per_page=self.results_per_hashtag
            )
            
            if not video_results:
                logger.warning(f"No video results found for hashtag: {topic}")
                return unique_usernames
                
            # Extract unique author usernames from video results
            for item in video_results:
                author_meta = item.get("authorMeta")
                if author_meta and isinstance(author_meta, dict):
                    username = author_meta.get("name") # Assuming 'name' is the username field
                    if username:
                        unique_usernames.add(username)
                        
            logger.info(f"Found {len(unique_usernames)} unique authors for topic: {topic}")
            
        except Exception as e:
            logger.error(f"Error processing topic {topic}: {e}")
            
        return unique_usernames

# Example usage (for testing purposes)
if __name__ == '__main__':
    import os
    from .config_manager import ConfigManager
    
    # Setup basic logging
    logging.basicConfig(level=logging.INFO)
    
    # Load config
    config_manager = ConfigManager()
    api_token = config_manager.get("apify_api_token")
    if not api_token:
        print("Please set the APIFY_API_TOKEN environment variable or add it to config.json")
        exit(1)
        
    # Initialize components
    api_client = ApiClient(api_token)
    topic_processor = TopicProcessor(api_client, results_per_hashtag=10) # Limit results for test
    
    # Test topic processing
    test_topic = "technology"
    print(f"\nGetting profiles for topic: {test_topic}")
    profiles = topic_processor.get_profiles_from_topic(test_topic)
    print(f"Found profiles: {profiles}")
