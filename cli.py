#!/usr/bin/env python3
"""
Command-line interface for the TikTok Parser
"""

import argparse
import logging
import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from src.tiktok_parser import TikTokParser

def setup_logging(verbose=False):
    """Configure logging based on verbosity level."""
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='TikTok Parser - Find influencers by topic with email addresses')
    
    parser.add_argument('topics', nargs='+', help='Topics (hashtags) to search for')
    parser.add_argument('--config', '-c', help='Path to configuration file')
    parser.add_argument('--output-format', '-f', choices=['csv', 'json'], default='csv',
                        help='Output format (default: csv)')
    parser.add_argument('--output-dir', '-o', default='./hybrid_output',
                        help='Directory for output files (default: ./hybrid_output)')
    parser.add_argument('--require-email', '-e', action='store_true', default=False,
                        help='Only include profiles with email addresses (default: True)')
    parser.add_argument('--no-require-email', action='store_false', dest='require_email',
                        help='Include profiles without email addresses')
    parser.add_argument('--max-profiles', '-m', type=int, default=20,
                        help='Maximum profiles to process per topic (default: 20)')
    parser.add_argument('--results-per-hashtag', '-r', type=int, default=20,
                        help='Number of results to fetch per hashtag (default: 20)')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Enable verbose logging')
    
    return parser.parse_args()

def main():
    """Main entry point for the CLI."""
    args = parse_arguments()
    setup_logging(args.verbose)
    
    # Check for API token
    api_token = os.environ.get('APIFY_API_TOKEN')
    if not api_token and not args.config:
        print("Error: APIFY_API_TOKEN environment variable is not set and no config file provided.")
        print("Please set the environment variable or provide a config file with the API token.")
        sys.exit(1)
    
    # Create config file if using command line arguments without a config file
    if not args.config:
        import json
        import tempfile
        
        config = {
            "apify_api_token": api_token,
            "tiktok_actor_id": "clockworks/tiktok-scraper",
            "profile_actor_id": "clockworks/tiktok-profile-scraper",
            "results_per_hashtag": args.results_per_hashtag,
            "max_profiles_per_topic": args.max_profiles,
            "require_email": args.require_email,
            "output_format": args.output_format,
            "output_dir": args.output_dir
        }
        
        # Create a temporary config file
        fd, temp_config_path = tempfile.mkstemp(suffix='.json')
        with os.fdopen(fd, 'w') as f:
            json.dump(config, f, indent=4)
        
        args.config = temp_config_path
    
    try:
        # Initialize and run the parser
        parser = TikTokParser(args.config)
        results = parser.run(args.topics)
        
        # Print summary
        total_profiles = sum(len(profiles) for profiles in results.values())
        print(f"\nParsing completed. Found {total_profiles} profiles with email across {len(args.topics)} topics.")
        
        for topic, profiles in results.items():
            print(f"\nTopic: {topic} - Found {len(profiles)} profiles with email")
            for i, profile in enumerate(profiles[:3]):  # Show first 3 profiles
                print(f"  - {profile['username']} ({profile['email']})")
            if len(profiles) > 3:
                print(f"  - ... and {len(profiles) - 3} more")
        
        print(f"\nResults exported to: {parser.output_dir}")
        
    except Exception as e:
        logging.error(f"Error running TikTok parser: {e}")
        sys.exit(1)
    finally:
        # Clean up temporary config file if created
        if not args.config and 'temp_config_path' in locals():
            try:
                os.remove(temp_config_path)
            except:
                pass

if __name__ == '__main__':
    main()
