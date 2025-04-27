"""
Configuration Manager Module - Handles loading and providing configuration
"""

import os
import json
import logging

logger = logging.getLogger(__name__)

class ConfigManager:
    """
    Manages loading configuration from environment variables or a config file.
    """
    
    def __init__(self, config_file_path="config.json"):
        """
        Initializes the ConfigManager.
        
        Args:
            config_file_path (str): Path to the JSON configuration file.
        """
        self.config_file_path = config_file_path
        self.config = self._load_config()
        
    def _load_config(self):
        """
        Loads configuration, prioritizing environment variables over config file.
        """
        config = {
            # --- Apify Settings ---
            "apify_api_token": None,  # Essential: Must be set via env var or config file
            "tiktok_actor_id": "clockworks/tiktok-scraper", # Default TikTok scraper actor
            
            # --- Search Settings ---
            "results_per_hashtag": 50, # Number of videos to retrieve per hashtag
            "max_profiles_per_topic": 20, # Max profiles to process per topic after hashtag search
            
            # --- Filtering Settings ---
            "require_email": True,
            
            # --- Output Settings ---
            "output_format": "csv", # csv or json
            "output_dir": "./output_api"
        }
        
        # 1. Load from config file if it exists
        if os.path.exists(self.config_file_path):
            try:
                with open(self.config_file_path, 'r') as f:
                    file_config = json.load(f)
                    config.update(file_config)
                    logger.info(f"Loaded configuration from {self.config_file_path}")
            except Exception as e:
                logger.warning(f"Could not load config file {self.config_file_path}: {e}")
        
        # 2. Override with environment variables
        env_api_token = os.getenv("APIFY_API_TOKEN")
        if env_api_token:
            config["apify_api_token"] = env_api_token
            logger.info("Loaded APIFY_API_TOKEN from environment variable.")
            
        # --- Add other environment variable overrides as needed ---
        # Example:
        # env_output_dir = os.getenv("TIKTOK_PARSER_OUTPUT_DIR")
        # if env_output_dir:
        #     config["output_dir"] = env_output_dir
            
        # Validate essential config
        if not config.get("apify_api_token"):
            logger.warning("APIFY_API_TOKEN is not set. Please set it via environment variable or in config.json.")
            # In a real application, might raise an error here or prompt the user
            
        return config

    def get(self, key, default=None):
        """
        Retrieves a configuration value.
        
        Args:
            key (str): The configuration key.
            default: The default value if the key is not found.
            
        Returns:
            The configuration value or the default.
        """
        return self.config.get(key, default)

    def get_all(self):
        """
        Returns the entire configuration dictionary.
        """
        return self.config

# Example usage (for testing purposes)
if __name__ == '__main__':
    # Create a dummy config file for testing
    if not os.path.exists("config.json"):
        dummy_config = {"results_per_hashtag": 75, "output_dir": "./dummy_output"}
        with open("config.json", "w") as f:
            json.dump(dummy_config, f, indent=4)
            
    # Set a dummy env var for testing
    # os.environ["APIFY_API_TOKEN"] = "dummy_env_token"
    
    manager = ConfigManager()
    print("Loaded Config:", manager.get_all())
    print("API Token:", manager.get("apify_api_token"))
    print("Results per Hashtag:", manager.get("results_per_hashtag"))
    
    # Clean up dummy file
    # if os.path.exists("config.json"):
    #     os.remove("config.json")
