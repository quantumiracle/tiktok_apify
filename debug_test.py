"""
Test script for TikTok Parser with debug logging for followers and likes
"""

import os
import logging
import json
import sys

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.config_manager import ConfigManager
from src.api_client import ApiClient
from src.topic_processor import TopicProcessor
from src.profile_processor import ProfileProcessor
from src.data_processor import DataProcessor
from src.email_extractor import EmailExtractor
from src.data_filter import DataFilter
from src.data_exporter import DataExporter

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    # Check for API token
    api_token = os.environ.get("APIFY_API_TOKEN")
    if not api_token:
        print("Error: APIFY_API_TOKEN environment variable is not set.")
        print("Please set it before running this script.")
        sys.exit(1)
    
    print(f"Using API token: {api_token[:5]}...{api_token[-5:]}")
    
    # Initialize components
    api_client = ApiClient(api_token)
    topic_processor = TopicProcessor(api_client, results_per_hashtag=10)  # Limit to 10 for testing
    profile_processor = ProfileProcessor(api_client)
    data_processor = DataProcessor()
    email_extractor = EmailExtractor()
    data_filter = DataFilter(email_extractor)
    
    # Create output directory
    output_dir = "./debug_output"
    os.makedirs(output_dir, exist_ok=True)
    data_exporter = DataExporter(output_dir)
    
    # Test topic
    test_topic = "art"
    print(f"\nSearching for topic: {test_topic}")
    
    # Step 1: Get profiles from topic
    usernames = topic_processor.get_profiles_from_topic(test_topic)
    if not usernames:
        print("No profiles found for the topic.")
        return
    
    print(f"Found {len(usernames)} profiles. Limiting to 5 for testing.")
    usernames_list = list(usernames)[:5]  # Limit to 5 profiles for testing
    
    # Step 2: Get profile data
    print(f"Getting profile data for: {usernames_list}")
    profile_data = profile_processor.get_profile_data(usernames_list)
    
    # Save raw API response for inspection
    with open(f"{output_dir}/raw_api_response.json", "w") as f:
        json.dump(profile_data, f, indent=2)
    print(f"Saved raw API response to {output_dir}/raw_api_response.json")
    
    # Step 3: Process profile data
    processed_profiles = data_processor.process_profile_data(profile_data, test_topic)
    
    # Save processed data for inspection
    with open(f"{output_dir}/processed_profiles.json", "w") as f:
        json.dump(processed_profiles, f, indent=2)
    print(f"Saved processed profiles to {output_dir}/processed_profiles.json")
    
    # Step 4: Apply email filter
    filtered_profiles = data_filter.apply_email_filter(processed_profiles, require_email=False)  # Include all profiles for testing
    
    # Export results
    data_exporter.export_data(filtered_profiles, "debug_results", "csv")
    data_exporter.export_data(filtered_profiles, "debug_results", "json")
    
    print(f"\nResults exported to {output_dir}/debug_results.csv and {output_dir}/debug_results.json")
    
    # Print summary
    print("\nProfile Summary:")
    for profile in filtered_profiles:
        print(f"Username: {profile['username']}")
        print(f"Followers: {profile['followers']}")
        print(f"Likes: {profile['likes']}")
        print(f"Email: {profile['email']}")
        print("-" * 40)

if __name__ == "__main__":
    main()
