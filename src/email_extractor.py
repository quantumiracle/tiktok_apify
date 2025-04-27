"""
Email Extractor Module - Identifies and extracts email addresses from text
"""

import re
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class EmailExtractor:
    """
    Identifies and extracts the first valid email address found in a text string.
    """
    
    # Regex to find potential email addresses
    # Handles common formats, including those with dots, hyphens, underscores in local part
    # and common TLDs. It's not exhaustive but covers many cases.
    EMAIL_REGEX = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

    def __init__(self):
        """
        Initializes the EmailExtractor.
        """
        logger.info("Initialized EmailExtractor")

    def extract_email(self, text: Optional[str]) -> Optional[str]:
        """
        Finds the first valid email address in the given text.
        
        Args:
            text (Optional[str]): The text to search within (e.g., user bio).
            
        Returns:
            Optional[str]: The first email address found, or None if no email is found.
        """
        if not text:
            return None
            
        try:
            match = self.EMAIL_REGEX.search(text)
            if match:
                email = match.group(0)
                # Basic validation: avoid common false positives like image URLs ending in .jpg/.png
                if not email.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                    logger.debug(f"Extracted email: {email} from text: {text[:100]}...")
                    return email
                else:
                    logger.debug(f"Skipped potential false positive email: {email}")
                    # Continue searching if needed, though this implementation returns the first match
                    # For more complex scenarios, might need findall and further filtering
            
        except Exception as e:
            logger.error(f"Error during email extraction: {e}")
            
        return None

# Example usage (for testing purposes)
if __name__ == '__main__':
    # Setup basic logging
    logging.basicConfig(level=logging.DEBUG)
    
    extractor = EmailExtractor()
    
    test_texts = [
        "Contact me at my.email+test@example.co.uk for details.",
        "Bio with no email address.",
        "Reach out via email: another-email_123@subdomain.example.com.",
        "Check my website example.com or email me at info@example.com",
        "Image: profile.jpg, email: false.positive@image.png, real: contact@domain.info",
        None,
        ""
    ]
    
    print("\nTesting Email Extraction:")
    for text in test_texts:
        email = extractor.extract_email(text)
        print(f"Text: {str(text)[:50]}... -> Email: {email}")
