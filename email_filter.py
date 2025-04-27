"""
Email Filter Module - Filters TikTok profiles based on email availability
"""

import re
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('email_filter')

class EmailFilter:
    """
    Filters TikTok profiles based on email availability and domain criteria
    """
    
    def __init__(self, domain_filter=None):
        """
        Initialize the email filter
        
        Args:
            domain_filter (list, optional): List of email domains to filter by
        """
        self.domain_filter = domain_filter or []
        self.email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    
    def extract_email(self, text):
        """
        Extract email address from text using regex
        
        Args:
            text (str): Text to extract email from
            
        Returns:
            str: Extracted email address or empty string if none found
        """
        if not text:
            return ""
            
        # Find all matches
        matches = re.findall(self.email_pattern, text)
        
        # Return first match or empty string
        return matches[0] if matches else ""
    
    def validate_email(self, email):
        """
        Validate email format and domain if domain filter is set
        
        Args:
            email (str): Email address to validate
            
        Returns:
            bool: True if email is valid, False otherwise
        """
        if not email:
            return False
            
        # Check if email matches pattern
        if not re.match(self.email_pattern, email):
            return False
            
        # If domain filter is set, check if email domain is in the filter
        if self.domain_filter:
            domain = email.split('@')[-1].lower()
            return domain in [d.lower() for d in self.domain_filter]
            
        return True
    
    def filter_profiles(self, profiles):
        """
        Filter profiles based on email availability and domain criteria
        
        Args:
            profiles (list): List of profile dictionaries
            
        Returns:
            list: Filtered list of profile dictionaries
        """
        filtered_profiles = []
        
        for profile in profiles:
            # Extract email if not already present
            if 'email' not in profile or not profile['email']:
                if 'bio' in profile:
                    profile['email'] = self.extract_email(profile['bio'])
                    profile['has_email'] = bool(profile['email'])
            
            # Check if profile has a valid email
            if profile.get('has_email', False) and self.validate_email(profile.get('email', '')):
                filtered_profiles.append(profile)
        
        logger.info(f"Filtered {len(filtered_profiles)} profiles with valid emails out of {len(profiles)} total profiles")
        return filtered_profiles
    
    def set_domain_filter(self, domains):
        """
        Set or update the domain filter
        
        Args:
            domains (list): List of email domains to filter by
        """
        self.domain_filter = domains
        logger.info(f"Updated domain filter: {domains}")
