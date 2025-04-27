"""
Profile Extractor Module - Extracts profile data from TikTok user profiles
"""

import asyncio
import logging
import re
from urllib.parse import urljoin

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('profile_extractor')

class ProfileExtractor:
    """
    Extracts profile data from TikTok user profiles including account details and metrics
    """
    
    def __init__(self, browser_manager):
        """
        Initialize the profile extractor with a browser manager
        
        Args:
            browser_manager (BrowserManager): Instance of BrowserManager for browser control
        """
        self.browser_manager = browser_manager
        self.base_url = "https://www.tiktok.com"
        self.request_delay = self.browser_manager.config.get('request_delay', 2)
    
    async def extract_profile_data(self, profile_url):
        """
        Extract data from a TikTok profile
        
        Args:
            profile_url (str): URL of the profile to extract data from
            
        Returns:
            dict: Dictionary containing profile data
        """
        logger.info(f"Extracting data from profile: {profile_url}")
        
        # Navigate to profile page
        page = await self.browser_manager.navigate(profile_url)
        
        # Handle login popup if it appears
        await self.browser_manager.handle_login_popup()
        
        # Extract profile data
        try:
            # Extract username from URL
            username = profile_url.split('/@')[-1].split('?')[0]
            
            # Extract display name
            display_name_element = await page.query_selector('h1[data-e2e="user-subtitle"], h2[data-e2e="user-title"]')
            display_name = await display_name_element.inner_text() if display_name_element else username
            
            # Extract bio/description
            bio_element = await page.query_selector('h2[data-e2e="user-bio"], div[data-e2e="user-bio"]')
            bio = await bio_element.inner_text() if bio_element else ""
            
            # Extract follower count
            followers_element = await page.query_selector('strong[data-e2e="followers-count"], div[data-e2e="followers-count"]')
            followers_text = await followers_element.inner_text() if followers_element else "0"
            followers = self._parse_count(followers_text)
            
            # Extract following count
            following_element = await page.query_selector('strong[data-e2e="following-count"], div[data-e2e="following-count"]')
            following_text = await following_element.inner_text() if following_element else "0"
            following = self._parse_count(following_text)
            
            # Extract likes count
            likes_element = await page.query_selector('strong[data-e2e="likes-count"], div[data-e2e="likes-count"]')
            likes_text = await likes_element.inner_text() if likes_element else "0"
            likes = self._parse_count(likes_text)
            
            # Extract email from bio using regex
            email = self._extract_email(bio)
            
            # Create profile data dictionary
            profile_data = {
                'username': username,
                'display_name': display_name,
                'profile_url': profile_url,
                'bio': bio,
                'followers': followers,
                'following': following,
                'likes': likes,
                'email': email,
                'has_email': bool(email)
            }
            
            logger.info(f"Successfully extracted data for profile: {username}")
            return profile_data
            
        except Exception as e:
            logger.error(f"Error extracting profile data: {e}")
            return {
                'username': profile_url.split('/@')[-1].split('?')[0],
                'profile_url': profile_url,
                'error': str(e)
            }
    
    async def extract_multiple_profiles(self, profile_urls):
        """
        Extract data from multiple TikTok profiles
        
        Args:
            profile_urls (list): List of profile URLs to extract data from
            
        Returns:
            list: List of dictionaries containing profile data
        """
        profiles_data = []
        
        for url in profile_urls:
            profile_data = await self.extract_profile_data(url)
            profiles_data.append(profile_data)
            
            # Add delay between profile extractions to avoid rate limiting
            await asyncio.sleep(self.request_delay)
        
        return profiles_data
    
    def _parse_count(self, count_text):
        """
        Parse count text (e.g., "1.5M", "500K", "1,200") to integer
        
        Args:
            count_text (str): Count text to parse
            
        Returns:
            int: Parsed count as integer
        """
        try:
            # Remove commas
            count_text = count_text.replace(',', '')
            
            # Handle K (thousands)
            if 'K' in count_text:
                return int(float(count_text.replace('K', '')) * 1000)
            
            # Handle M (millions)
            elif 'M' in count_text:
                return int(float(count_text.replace('M', '')) * 1000000)
            
            # Handle B (billions)
            elif 'B' in count_text:
                return int(float(count_text.replace('B', '')) * 1000000000)
            
            # Handle plain numbers
            else:
                return int(float(count_text))
                
        except Exception:
            return 0
    
    def _extract_email(self, text):
        """
        Extract email address from text using regex
        
        Args:
            text (str): Text to extract email from
            
        Returns:
            str: Extracted email address or empty string if none found
        """
        if not text:
            return ""
            
        # Email regex pattern
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        
        # Find all matches
        matches = re.findall(email_pattern, text)
        
        # Return first match or empty string
        return matches[0] if matches else ""
