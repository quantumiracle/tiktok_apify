"""
Simplified test script for TikTok Parser with 'art' topic
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Add parent directory to path to allow importing from src
sys.path.insert(0, str(Path(__file__).parent))

# Create a simple mock implementation for demonstration
class MockTikTokParser:
    """Mock implementation of TikTok Parser for demonstration"""
    
    def __init__(self, config=None):
        self.config = config or {}
        
    async def run(self, topics):
        """Mock run method that returns sample data"""
        if isinstance(topics, str):
            topics = [topics]
            
        results = {}
        for topic in topics:
            # Generate sample profiles for the topic
            profiles = self._generate_sample_profiles(topic)
            results[topic] = profiles
            
        # Create sample export paths
        export_by_topic = {topic: f"art_test_output/tiktok_{topic}_influencers.csv" for topic in topics}
        export_combined = "art_test_output/tiktok_all_influencers.csv"
        
        return {
            'results': results,
            'export_by_topic': export_by_topic,
            'export_combined': export_combined
        }
    
    def _generate_sample_profiles(self, topic):
        """Generate sample profiles for demonstration"""
        if topic == "art":
            return [
                {
                    'username': 'artmaster123',
                    'display_name': 'Art Master',
                    'profile_url': 'https://www.tiktok.com/@artmaster123',
                    'bio': 'Professional artist sharing tips and tricks. Contact me at artmaster@example.com for commissions.',
                    'followers': 250000,
                    'following': 1200,
                    'likes': 3500000,
                    'email': 'artmaster@example.com',
                    'has_email': True
                },
                {
                    'username': 'paintingpro',
                    'display_name': 'Painting Pro',
                    'profile_url': 'https://www.tiktok.com/@paintingpro',
                    'bio': 'Oil painting specialist. DM for business inquiries or email: pro@paintingexamples.com',
                    'followers': 120000,
                    'following': 850,
                    'likes': 1800000,
                    'email': 'pro@paintingexamples.com',
                    'has_email': True
                },
                {
                    'username': 'sketchdaily',
                    'display_name': 'Daily Sketch',
                    'profile_url': 'https://www.tiktok.com/@sketchdaily',
                    'bio': 'Posting a new sketch every day! Business: sketches@artmail.com',
                    'followers': 75000,
                    'following': 450,
                    'likes': 950000,
                    'email': 'sketches@artmail.com',
                    'has_email': True
                }
            ]
        else:
            # Generic sample for other topics
            return [
                {
                    'username': f'{topic}creator1',
                    'display_name': f'{topic.capitalize()} Creator',
                    'profile_url': f'https://www.tiktok.com/@{topic}creator1',
                    'bio': f'I love {topic}! Contact: {topic}creator@example.com',
                    'followers': 100000,
                    'following': 500,
                    'likes': 1500000,
                    'email': f'{topic}creator@example.com',
                    'has_email': True
                }
            ]

async def test_art_topic():
    """Test with 'art' topic using mock implementation"""
    # Configure parser for testing
    test_config = {
        'headless': False,
        'search_type': 'topic',
        'results_limit': 5,
        'require_email': True,
        'output_format': 'csv',
        'output_dir': os.path.join(os.getcwd(), "art_test_output")
    }
    
    # Create output directory
    os.makedirs(test_config['output_dir'], exist_ok=True)
    
    # Initialize mock parser
    parser = MockTikTokParser(test_config)
    
    try:
        print("Testing TikTok Parser with topic: art")
        
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
        
        print("\nTest completed successfully")
        return results
        
    except Exception as e:
        print(f"\nTest Error: {e}")
        return None

if __name__ == '__main__':
    asyncio.run(test_art_topic())
