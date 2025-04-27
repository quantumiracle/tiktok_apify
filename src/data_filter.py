"""
Data Filter Module - Filters processed influencer data based on criteria
"""

import logging
from typing import List, Dict, Any

from .email_extractor import EmailExtractor

logger = logging.getLogger(__name__)

class DataFilter:
    """
    Filters the processed influencer data based on specified criteria,
    primarily the presence of an extracted email address.
    """
    
    def __init__(self, email_extractor: EmailExtractor):
        """
        Initializes the DataFilter.
        
        Args:
            email_extractor (EmailExtractor): Instance of the EmailExtractor.
        """
        self.email_extractor = email_extractor
        logger.info("Initialized DataFilter")

    def apply_email_filter(self, processed_profiles: List[Dict[str, Any]], require_email: bool = True) -> List[Dict[str, Any]]:
        """
        Applies email extraction and filters the list of profiles.
        
        Args:
            processed_profiles (List[Dict[str, Any]]): List of processed profile data.
            require_email (bool): If True, only profiles with an extracted email are returned.
            
        Returns:
            List[Dict[str, Any]]: Filtered list of profile data, with email fields updated.
        """
        if not processed_profiles:
            return []
            
        logger.info(f"Applying email filter (require_email={require_email}) to {len(processed_profiles)} profiles.")
        
        filtered_profiles = []
        for profile in processed_profiles:
            # Extract email from bio
            bio = profile.get("bio", "")
            email = self.email_extractor.extract_email(bio)
            
            # Update profile data
            profile["email"] = email
            profile["has_email"] = bool(email)
            
            # Apply filter
            if require_email:
                if profile["has_email"]:
                    filtered_profiles.append(profile)
            else:
                # If email is not required, include all profiles
                filtered_profiles.append(profile)
                
        logger.info(f"Filtered profiles count: {len(filtered_profiles)}")
        return filtered_profiles

# Example usage (for testing purposes)
if __name__ == '__main__':
    # Setup basic logging
    logging.basicConfig(level=logging.INFO)
    
    # Example processed data (from DataProcessor)
    processed_data = [
        {
            "topic": "testing", "username": "testuser1", "profile_url": "url1", 
            "followers": 1000, "likes": 50000, 
            "bio": "This is my bio. Contact: test@example.com", 
            "email": None, "has_email": False
        },
        {
            "topic": "testing", "username": "testuser2", "profile_url": "url2", 
            "followers": 2500, "likes": 120000, 
            "bio": "Another bio here.", 
            "email": None, "has_email": False
        },
        {
            "topic": "testing", "username": "testuser3", "profile_url": "url3", 
            "followers": 500, "likes": 10000, 
            "bio": "Bio 3. Email me at user3@domain.net", 
            "email": None, "has_email": False
        }
    ]
    
    email_extractor = EmailExtractor()
    data_filter = DataFilter(email_extractor)
    
    # Test with require_email = True
    print("\nFiltering with require_email=True:")
    filtered_results_required = data_filter.apply_email_filter(processed_data, require_email=True)
    for profile in filtered_results_required:
        print(profile)
        
    # Reset email fields for next test
    for p in processed_data:
        p["email"] = None
        p["has_email"] = False
        
    # Test with require_email = False
    print("\nFiltering with require_email=False:")
    filtered_results_not_required = data_filter.apply_email_filter(processed_data, require_email=False)
    for profile in filtered_results_not_required:
        print(profile)
