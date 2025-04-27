"""
Test script for TikTok Parser
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
logger = logging.getLogger('tiktok_parser_test')

async def test_parser():
    """Test the TikTok Parser with sample topics"""
    # Sample topics to test
    test_topics = ["fitness", "cooking", "technology"]
    
    # Configure parser for testing
    test_config = {
        'headless': False,  # Set to True for headless testing
        'search_type': 'topic',
        'results_limit': 5,  # Limit results for faster testing
        'request_delay': 2,
        'require_email': True,
        'output_format': 'csv',
        'output_dir': os.path.join(os.getcwd(), "test_output")
    }
    
    # Create output directory
    os.makedirs(test_config['output_dir'], exist_ok=True)
    
    # Initialize parser
    parser = TikTokParser(test_config)
    
    try:
        logger.info(f"Testing TikTok Parser with topics: {test_topics}")
        
        # Run parser
        results = await parser.run(test_topics)
        
        # Print results summary
        print("\n=== TikTok Parser Test Results ===")
        for topic, profiles in results['results'].items():
            print(f"\nTopic: {topic}")
            print(f"  Profiles found: {len(profiles)}")
            print(f"  Profiles with email: {sum(1 for p in profiles if p.get('has_email', False))}")
            
            # Print sample profile data
            if profiles:
                print("\n  Sample Profile Data:")
                sample = profiles[0]
                print(f"    Username: {sample.get('username', 'N/A')}")
                print(f"    Display Name: {sample.get('display_name', 'N/A')}")
                print(f"    Followers: {sample.get('followers', 'N/A')}")
                print(f"    Likes: {sample.get('likes', 'N/A')}")
                print(f"    Email: {sample.get('email', 'N/A')}")
        
        print("\n=== Exported Files ===")
        for topic, filepath in results['export_by_topic'].items():
            print(f"  {topic}: {filepath}")
        print(f"\nCombined export: {results['export_combined']}")
        
        logger.info("Test completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        print(f"\nTest Error: {e}")
        return False

if __name__ == '__main__':
    asyncio.run(test_parser())
