"""
TikTok Parser - Main module for orchestrating the TikTok parsing workflow
"""

import logging
import os
from typing import List, Dict, Any, Set, Optional

from .config_manager import ConfigManager
from .api_client import ApiClient
from .topic_processor import TopicProcessor
from .profile_processor import ProfileProcessor
from .data_processor import DataProcessor
from .email_extractor import EmailExtractor
from .data_filter import DataFilter
from .data_exporter import DataExporter

logger = logging.getLogger(__name__)

class TikTokParser:
    """
    Main class that orchestrates the TikTok parsing workflow.
    """
    
    def __init__(self, config_file_path: Optional[str] = None):
        """
        Initializes the TikTokParser with configuration.
        
        Args:
            config_file_path (Optional[str]): Path to the configuration file.
        """
        # Initialize configuration
        self.config_manager = ConfigManager(config_file_path or "config.json")
        
        # Get configuration values
        self.api_token = self.config_manager.get("apify_api_token")
        self.tiktok_actor_id = self.config_manager.get("tiktok_actor_id", "clockworks/tiktok-scraper")
        self.results_per_hashtag = self.config_manager.get("results_per_hashtag", 50)
        self.max_profiles_per_topic = self.config_manager.get("max_profiles_per_topic", 20)
        self.require_email = self.config_manager.get("require_email", True)
        self.output_format = self.config_manager.get("output_format", "csv")
        self.output_dir = self.config_manager.get("output_dir", "./output_api")
        
        # Validate essential configuration
        if not self.api_token:
            raise ValueError("APIFY_API_TOKEN is not set. Please set it via environment variable or in config.json.")
            
        # Initialize components
        self.api_client = ApiClient(self.api_token, self.tiktok_actor_id)
        self.topic_processor = TopicProcessor(self.api_client, self.results_per_hashtag)
        self.profile_processor = ProfileProcessor(self.api_client)
        self.data_processor = DataProcessor()
        self.email_extractor = EmailExtractor()
        self.data_filter = DataFilter(self.email_extractor)
        self.data_exporter = DataExporter(self.output_dir)
        
        logger.info("TikTokParser initialized successfully.")
        
    def parse_topic(self, topic: str) -> List[Dict[str, Any]]:
        """
        Parses a single topic to find influencers with email addresses.
        
        Args:
            topic (str): The topic (hashtag) to search for.
            
        Returns:
            List[Dict[str, Any]]: List of processed and filtered influencer data.
        """
        logger.info(f"Parsing topic: {topic}")
        
        # Step 1: Search for profiles by topic
        usernames = self.topic_processor.get_profiles_from_topic(topic)
        if not usernames:
            logger.warning(f"No profiles found for topic: {topic}")
            return []
            
        # Limit the number of profiles to process if needed
        if len(usernames) > self.max_profiles_per_topic:
            logger.info(f"Limiting profiles from {len(usernames)} to {self.max_profiles_per_topic}")
            usernames = list(usernames)[:self.max_profiles_per_topic]
            
        # Step 2: Get detailed profile data
        profile_data = self.profile_processor.get_profile_data(list(usernames))
        if not profile_data:
            logger.warning(f"No profile data retrieved for topic: {topic}")
            return []
            
        # Step 3: Process raw profile data
        processed_profiles = self.data_processor.process_profile_data(profile_data, topic)
        
        # Step 4: Apply email filtering
        filtered_profiles = self.data_filter.apply_email_filter(processed_profiles, self.require_email)
        
        logger.info(f"Found {len(filtered_profiles)} profiles with email for topic: {topic}")
        return filtered_profiles
        
    def parse_topics(self, topics: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Parses multiple topics to find influencers with email addresses.
        
        Args:
            topics (List[str]): List of topics (hashtags) to search for.
            
        Returns:
            Dict[str, List[Dict[str, Any]]]: Dictionary mapping topics to lists of influencer data.
        """
        results = {}
        all_profiles = []
        
        for topic in topics:
            topic_profiles = self.parse_topic(topic)
            results[topic] = topic_profiles
            all_profiles.extend(topic_profiles)
            
            # Export topic-specific results
            if topic_profiles:
                self.data_exporter.export_data(
                    topic_profiles, 
                    base_filename=f"topic_{topic}", 
                    output_format=self.output_format
                )
                
        # Export combined results
        if all_profiles:
            self.data_exporter.export_data(
                all_profiles, 
                base_filename="all_topics", 
                output_format=self.output_format
            )
            
        return results
        
    def run(self, topics: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Main entry point to run the parser with the given topics.
        
        Args:
            topics (List[str]): List of topics (hashtags) to search for.
            
        Returns:
            Dict[str, List[Dict[str, Any]]]: Dictionary mapping topics to lists of influencer data.
        """
        if not topics:
            logger.warning("No topics provided to parse.")
            return {}
            
        logger.info(f"Starting TikTok parser with topics: {topics}")
        
        try:
            results = self.parse_topics(topics)
            
            # Log summary
            total_profiles = sum(len(profiles) for profiles in results.values())
            logger.info(f"Parsing completed. Found {total_profiles} profiles with email across {len(topics)} topics.")
            
            return results
            
        except Exception as e:
            logger.error(f"Error running TikTok parser: {e}")
            return {}

# Example usage (for testing purposes)
if __name__ == '__main__':
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Set API token for testing
    os.environ["APIFY_API_TOKEN"] = "your_api_token_here"
    
    # Initialize parser
    parser = TikTokParser()
    
    # Run parser with sample topics
    sample_topics = ["technology", "food"]
    results = parser.run(sample_topics)
    
    # Print summary
    for topic, profiles in results.items():
        print(f"\nTopic: {topic} - Found {len(profiles)} profiles with email")
        for profile in profiles[:3]:  # Show first 3 profiles
            print(f"  - {profile['username']} ({profile['email']})")
        if len(profiles) > 3:
            print(f"  - ... and {len(profiles) - 3} more")
            
    print(f"\nResults exported to: {parser.output_dir}")
