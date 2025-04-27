"""
Data Processor Module - Parses and normalizes raw API data
"""

import logging
import json
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class DataProcessor:
    """
    Processes raw API data into a structured format.
    """
    
    def __init__(self):
        """
        Initializes the DataProcessor.
        """
        pass
        
    def _safe_get(self, data: Dict[str, Any], path: List[str], default: Any = None) -> Any:
        """
        Safely gets a value from a nested dictionary using a path of keys.
        
        Args:
            data (Dict[str, Any]): The dictionary to extract data from.
            path (List[str]): A list of keys representing the path to the desired value.
            default (Any): The default value to return if the path doesn't exist.
            
        Returns:
            Any: The value at the specified path, or the default value if not found.
        """
        current = data
        for key in path:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current
        
    def process_profile_data(self, raw_profile_items: List[Dict[str, Any]], topic: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Processes raw profile data items from the Apify API into a structured format.
        
        Args:
            raw_profile_items (List[Dict[str, Any]]): List of raw profile data dicts from Apify.
            topic (Optional[str]): The topic/hashtag associated with these profiles.
            
        Returns:
            List[Dict[str, Any]]: List of processed and structured profile data.
        """
        processed_profiles = []
        if not raw_profile_items:
            return processed_profiles
            
        logger.info(f"Processing {len(raw_profile_items)} raw profile items.")
        
        # Debug: Log the first item's structure to understand the API response format
        if raw_profile_items and len(raw_profile_items) > 0:
            first_item = raw_profile_items[0]
            logger.debug(f"DEBUG - First profile item structure: {json.dumps(first_item, indent=2)}")
        
        for item in raw_profile_items:
            # Extract username from different possible locations
            username = None
            
            # Try to get username from authorMeta
            if "authorMeta" in item:
                username = self._safe_get(item, ["authorMeta", "name"])
            
            # If not found, try other possible locations
            if not username:
                username = (item.get("uniqueId") or 
                           item.get("nickname") or 
                           self._safe_get(item, ["userInfo", "user", "uniqueId"]))
                
            if not username:
                logger.warning(f"Could not extract username from item: {item.get('id', 'N/A')}")
                continue # Skip if no username
            
            profile_url = f"https://www.tiktok.com/@{username}" if username else None
            
            # For TikTok Profile Scraper API, followers are in "fans" and likes in "heart"
            # These are typically in the authorMeta section
            followers = 0
            likes = 0
            
            # Try to get followers and likes from authorMeta (Profile Scraper API)
            if "authorMeta" in item:
                followers = self._safe_get(item, ["authorMeta", "fans"], 0)
                likes = self._safe_get(item, ["authorMeta", "heart"], 0)
            
            # If not found in authorMeta, try direct properties (some API responses have them at top level)
            if followers == 0:
                followers = item.get("fans", 0)
            if likes == 0:
                likes = item.get("heart", 0)
                
            # If still not found, try diggCount for likes (TikTok Scraper API)
            if likes == 0:
                likes = item.get("diggCount", 0)
            
            # Bio might be under authorMeta or directly in item
            bio = None
            if "authorMeta" in item:
                bio = self._safe_get(item, ["authorMeta", "signature"])
            if not bio:
                bio = item.get("signature") or self._safe_get(item, ["userInfo", "signature"], "")
            
            # Extract additional fields from authorMeta
            following = 0
            friends = 0
            video_count = 0
            
            # Try to get additional fields from authorMeta (Profile Scraper API)
            if "authorMeta" in item:
                following = self._safe_get(item, ["authorMeta", "following"], 0)
                friends = self._safe_get(item, ["authorMeta", "friends"], 0)
                video_count = self._safe_get(item, ["authorMeta", "video"], 0)
            
            # If not found in authorMeta, try direct properties
            if following == 0:
                following = item.get("following", 0)
            if friends == 0:
                friends = item.get("friends", 0)
            if video_count == 0:
                video_count = item.get("video", 0)
            
            processed_profile = {
                "topic": topic,
                "username": username,
                "profile_url": profile_url,
                "followers": followers,
                "likes": likes,
                "following": following,
                "friends": friends,
                "video_count": video_count,
                "bio": bio or "", # Ensure bio is always a string
                "email": None, # To be filled by EmailExtractor
                "has_email": False # To be set by EmailExtractor/DataFilter
            }
            
            # Debug: Log the extracted data for this profile
            logger.debug(f"DEBUG - Extracted profile data for {username}: followers={followers}, likes={likes}")
            
            processed_profiles.append(processed_profile)
            
        logger.info(f"Successfully processed {len(processed_profiles)} profiles.")
        return processed_profiles
