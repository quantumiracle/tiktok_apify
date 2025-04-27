"""
API Client Module - Handles interaction with the Apify API
"""

import logging
import time
from typing import Dict, List, Any, Optional, Union

from apify_client import ApifyClient

logger = logging.getLogger(__name__)

class ApiClient:
    """
    Manages interaction with the Apify API for TikTok data extraction.
    """
    
    def __init__(self, api_token: str, tiktok_actor_id: str = "clockworks/tiktok-scraper", 
                 profile_actor_id: str = "clockworks/tiktok-profile-scraper"):
        """
        Initializes the ApiClient with Apify credentials.
        
        Args:
            api_token (str): Apify API token for authentication
            tiktok_actor_id (str): ID of the Apify Actor to use for TikTok topic scraping
            profile_actor_id (str): ID of the Apify Actor to use for TikTok profile scraping
        """
        self.api_token = api_token
        self.tiktok_actor_id = tiktok_actor_id
        self.profile_actor_id = profile_actor_id
        self.client = ApifyClient(api_token)
        logger.info(f"Initialized ApiClient with topic actor ID: {tiktok_actor_id} and profile actor ID: {profile_actor_id}")
        
    def run_actor_with_input(self, actor_id: str, input_data: Dict[str, Any], wait_for_finish: bool = True, 
                            timeout_secs: int = 300) -> Optional[str]:
        """
        Runs an Apify Actor with the provided input.
        
        Args:
            actor_id (str): ID of the Actor to run
            input_data (Dict[str, Any]): Input data for the Actor
            wait_for_finish (bool): Whether to wait for the Actor run to finish
            timeout_secs (int): Maximum time to wait for the Actor run to finish
            
        Returns:
            Optional[str]: Run ID if successful, None otherwise
        """
        try:
            logger.info(f"Starting Actor run with input: {input_data}")
            run = self.client.actor(actor_id).call(run_input=input_data)
            
            if not wait_for_finish:
                return run.get("id")
                
            # Wait for the run to finish
            start_time = time.time()
            while True:
                run_info = self.client.run(run.get("id")).get()
                status = run_info.get("status")
                
                if status == "SUCCEEDED":
                    logger.info(f"Actor run succeeded. Run ID: {run.get('id')}")
                    return run.get("id")
                    
                elif status in ["FAILED", "ABORTED", "TIMED-OUT"]:
                    logger.error(f"Actor run failed with status: {status}")
                    return None
                    
                # Check timeout
                if time.time() - start_time > timeout_secs:
                    logger.warning(f"Timeout waiting for Actor run to finish after {timeout_secs} seconds")
                    return run.get("id")  # Return the ID anyway so caller can check status later
                    
                # Wait before checking again
                time.sleep(5)
                
        except Exception as e:
            logger.error(f"Error running Actor: {e}")
            return None
            
    def get_dataset_items(self, run_id: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Retrieves dataset items from a completed Actor run.
        
        Args:
            run_id (str): ID of the Actor run
            limit (Optional[int]): Maximum number of items to retrieve
            
        Returns:
            List[Dict[str, Any]]: List of dataset items
        """
        try:
            logger.info(f"Retrieving dataset items for run ID: {run_id}")
            
            # Get the default dataset ID for the run
            run_info = self.client.run(run_id).get()
            dataset_id = run_info.get("defaultDatasetId")
            
            if not dataset_id:
                logger.error(f"No default dataset found for run ID: {run_id}")
                return []
                
            # Get dataset items
            items = []
            options = {}
            if limit:
                options["limit"] = limit
                
            dataset_items = self.client.dataset(dataset_id).list_items(**options)
            # Access items directly from the ListPage object
            items.extend(dataset_items.items)
            
            logger.info(f"Retrieved {len(items)} dataset items")
            return items
            
        except Exception as e:
            logger.error(f"Error retrieving dataset items: {e}")
            return []
            
    def search_by_hashtag(self, hashtag: str, results_per_page: int = 100) -> List[Dict[str, Any]]:
        """
        Searches TikTok for videos with the specified hashtag using the TikTok Scraper API.
        
        Args:
            hashtag (str): Hashtag to search for (without the # symbol)
            results_per_page (int): Number of results to retrieve
            
        Returns:
            List[Dict[str, Any]]: List of video data items
        """
        input_data = {
            "hashtags": [hashtag],
            "resultsPerPage": results_per_page,
            "proxyCountryCode": "None",
            "shouldDownloadVideos": False
        }
        
        run_id = self.run_actor_with_input(self.tiktok_actor_id, input_data)
        if not run_id:
            return []
            
        return self.get_dataset_items(run_id)
        
    def get_profiles(self, usernames: List[str], results_per_profile: int = 1) -> List[Dict[str, Any]]:
        """
        Retrieves profile data for the specified TikTok usernames using the TikTok Scraper API.
        
        Args:
            usernames (List[str]): List of TikTok usernames
            results_per_profile (int): Number of results to retrieve per profile
            
        Returns:
            List[Dict[str, Any]]: List of profile data items
        """
        input_data = {
            "profiles": usernames,
            "resultsPerPage": results_per_profile,
            "proxyCountryCode": "None",
            "shouldDownloadVideos": False
        }
        
        run_id = self.run_actor_with_input(self.tiktok_actor_id, input_data)
        if not run_id:
            return []
            
        return self.get_dataset_items(run_id)
        
    def get_detailed_profiles(self, usernames: List[str]) -> List[Dict[str, Any]]:
        """
        Retrieves detailed profile data including followers and likes for the specified TikTok usernames
        using the TikTok Profile Scraper API.
        
        Args:
            usernames (List[str]): List of TikTok usernames
            
        Returns:
            List[Dict[str, Any]]: List of detailed profile data items
        """
        input_data = {
            "profiles": usernames,
            "resultsPerPage": 1,  # We only need basic profile info
            "shouldDownloadCovers": False,
            "shouldDownloadSlideshowImages": False,
            "shouldDownloadSubtitles": False,
            "shouldDownloadVideos": False
        }
        
        run_id = self.run_actor_with_input(self.profile_actor_id, input_data)
        if not run_id:
            return []
            
        return self.get_dataset_items(run_id)

# Example usage (for testing purposes)
if __name__ == '__main__':
    import os
    
    # Get API token from environment variable
    api_token = os.getenv("APIFY_API_TOKEN")
    if not api_token:
        print("Please set the APIFY_API_TOKEN environment variable")
        exit(1)
        
    # Initialize client
    client = ApiClient(api_token)
    
    # Test hashtag search
    print("Searching for hashtag 'food'...")
    results = client.search_by_hashtag("food", results_per_page=5)
    print(f"Found {len(results)} results")
    
    # Print first result
    if results:
        print("\nFirst result:")
        for key, value in results[0].items():
            print(f"{key}: {value}")
