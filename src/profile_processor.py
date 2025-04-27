"""
Profile Processor Module - Handles scraping detailed data for specific user profiles
"""

import logging
from typing import List, Dict, Any

from .api_client import ApiClient

logger = logging.getLogger(__name__)

class ProfileProcessor:
    """
    Handles the logic for scraping detailed data for specific user profiles.
    """
    
    def __init__(self, api_client: ApiClient, results_per_profile: int = 1):
        """
        Initializes the ProfileProcessor.
        
        Args:
            api_client (ApiClient): Instance of the ApiClient for making API calls.
            results_per_profile (int): Number of results to fetch per profile (usually 1 for profile data).
        """
        self.api_client = api_client
        self.results_per_profile = results_per_profile
        
    def get_profile_data(self, usernames: List[str]) -> List[Dict[str, Any]]:
        """
        Retrieves detailed profile data for a list of usernames using the TikTok Profile Scraper API.
        This API provides complete profile data including followers ("fans") and likes ("heart").
        
        Args:
            usernames (List[str]): A list of TikTok usernames to scrape.
            
        Returns:
            List[Dict[str, Any]]: A list of raw profile data items from the API.
        """
        if not usernames:
            logger.warning("No usernames provided to get_profile_data")
            return []
            
        logger.info(f"Retrieving profile data for {len(usernames)} usernames: {usernames[:5]}...")
        
        try:
            # Use the ApiClient to get detailed profile data using the TikTok Profile Scraper API
            # This API provides followers ("fans") and likes ("heart") data
            profile_results = self.api_client.get_detailed_profiles(
                usernames=usernames
            )
            
            if not profile_results:
                logger.warning(f"No profile data retrieved for usernames: {usernames[:5]}...")
                return []
                
            logger.info(f"Successfully retrieved {len(profile_results)} profile data items.")
            return profile_results
            
        except Exception as e:
            logger.error(f"Error retrieving profile data for usernames {usernames[:5]}...: {e}")
            return []

# Example usage (for testing purposes)
if __name__ == '__main__':
    import os
    from .config_manager import ConfigManager
    from .api_client import ApiClient
    
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
    profile_processor = ProfileProcessor(api_client)
    
    # Test profile processing
    test_usernames = ["tiktok", "google"] # Example usernames
    print(f"\nGetting profile data for usernames: {test_usernames}")
    profiles_data = profile_processor.get_profile_data(test_usernames)
    
    if profiles_data:
        print(f"Retrieved {len(profiles_data)} profile items.")
        print("\nFirst profile data item:")
        for key, value in profiles_data[0].items():
            # Limit printing long values
            if isinstance(value, str) and len(value) > 100:
                print(f"{key}: {value[:100]}...")
            else:
                print(f"{key}: {value}")
    else:
        print("No profile data retrieved.")
