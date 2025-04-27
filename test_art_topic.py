"""
Test script for TikTok Parser with 'art' topic
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Add parent directory to path to allow importing from src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.tiktok_parser import TikTokParser

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('tiktok_parser_art_test')

async def test_art_topic():
    """Test the TikTok Parser with 'art' topic"""
    # Configure parser for testing
    test_config = {
        'headless': False,  # Set to True for headless testing
        'search_type': 'topic',
        'results_limit': 5,  # Limit results for faster testing
        'request_delay': 2,
        'require_email': True,
        'output_format': 'csv',
        'output_dir': os.path.join(os.getcwd(), "art_test_output")
    }
    
    # Create output directory
    os.makedirs(test_config['output_dir'], exist_ok=True)
    
    # Initialize parser
    parser = TikTokParser(test_config)
    
    try:
        logger.info("Testing TikTok Parser with topic: art")
        
        # Run parser
        results = await parser.run("art")
        
        # Print results summary
        print("\n=== TikTok Parser Test Results for 'art' ===")
        for topic, profiles in results['results'].items():
            print(f"\nTopic: {topic}")
            print(f"  Profiles found: {len(profiles)}")
            print(f"  Profiles with email: {sum(1 for p in profiles if p.get('has_email', False))}")
            
            # Print all profile data
            print("\n  Profile Data:")
            for i, profile in enumerate(profiles):
                print(f"\n    Profile {i+1}:")
                print(f"      Username: {profile.get('username', 'N/A')}")
                print(f"      Display Name: {profile.get('display_name', 'N/A')}")
                print(f"      Followers: {profile.get('followers', 'N/A')}")
                print(f"      Likes: {profile.get('likes', 'N/A')}")
                print(f"      Email: {profile.get('email', 'N/A')}")
                print(f"      Bio: {profile.get('bio', 'N/A')[:100]}..." if len(profile.get('bio', '')) > 100 else f"      Bio: {profile.get('bio', 'N/A')}")
        
        print("\n=== Exported Files ===")
        for topic, filepath in results['export_by_topic'].items():
            print(f"  {topic}: {filepath}")
        print(f"\nCombined export: {results['export_combined']}")
        
        logger.info("Test completed successfully")
        return results
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        print(f"\nTest Error: {e}")
        return None

if __name__ == '__main__':
    asyncio.run(test_art_topic())
