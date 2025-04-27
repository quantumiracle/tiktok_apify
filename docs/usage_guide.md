# TikTok Parser - Hybrid API Approach

## Installation and Usage Guide

This guide explains how to install and use the TikTok Parser with the hybrid API approach, which leverages two Apify services for optimal data extraction:
1. **TikTok Scraper API** for topic-based searching
2. **TikTok Profile Scraper API** for detailed profile metrics

### Prerequisites

*   Python 3.8 or higher
*   pip (Python package installer)
*   An Apify account and API token

### Installation

1.  **Clone the Repository (if applicable)**
    If you have the project files, navigate to the `tiktok_parser` directory in your terminal.

2.  **Install Dependencies**
    Install the required Python packages using pip:
    ```bash
    cd /path/to/tiktok_parser
    pip install -r requirements.txt # Assuming a requirements.txt exists or create one
    # Or install directly:
    pip install apify-client
    ```
    *Note: If a `requirements.txt` doesn't exist, the primary dependency is `apify-client`.*

3.  **Install the Package (Optional but Recommended)**
    For easier command-line usage, install the package in editable mode:
    ```bash
    pip install -e .
    ```

### Configuration

The parser requires an Apify API token to function. You can provide this token in two ways:

1.  **Environment Variable (Recommended)**:
    Set the `APIFY_API_TOKEN` environment variable:
    ```bash
    export APIFY_API_TOKEN="your_apify_api_token_here"
    ```
    Replace `"your_apify_api_token_here"` with your actual token.

2.  **Configuration File (`config.json`)**:
    Create a file named `config.json` in the `tiktok_parser` directory with the following content:
    ```json
    {
        "apify_api_token": "your_apify_api_token_here",
        "tiktok_actor_id": "clockworks/tiktok-scraper",
        "profile_actor_id": "clockworks/tiktok-profile-scraper",
        "results_per_hashtag": 50,
        "max_profiles_per_topic": 20,
        "require_email": true,
        "output_format": "csv",
        "output_dir": "./hybrid_output"
    }
    ```
    Replace `"your_apify_api_token_here"` with your actual token. You can also adjust other parameters like `results_per_hashtag`, `max_profiles_per_topic`, `require_email`, `output_format`, and `output_dir`.

**Getting Your Apify API Token:**

*   Log in to your Apify account.
*   Navigate to Settings > Integrations.
*   Copy your Personal API token.
*   Link: [https://console.apify.com/account/integrations](https://console.apify.com/account/integrations)

### Usage

#### Command-Line Interface (CLI)

The easiest way to use the parser is via the command line.

**Basic Usage:**

```bash
python cli.py <topic1> <topic2> ... [options]
```

*   Replace `<topic1>`, `<topic2>`, etc., with the hashtags (without the # symbol) you want to search for (e.g., `art`, `food`, `technology`).

**Examples:**

*   Search for 'art' and 'food' influencers with emails, outputting to CSV (default):
    ```bash
    python cli.py art food --require-email
    ```

*   Search for 'technology' influencers (including those without emails), outputting to JSON:
    ```bash
    python cli.py technology --no-require-email --output-format json
    ```

*   Search for 'sports' influencers, limiting results and using a specific config file:
    ```bash
    python cli.py sports --max-profiles 10 --results-per-hashtag 30 --config my_config.json
    ```

**CLI Options:**

*   `topics`: One or more topics (hashtags) to search.
*   `--config`, `-c`: Path to a custom configuration file.
*   `--output-format`, `-f`: Output format (`csv` or `json`, default: `csv`).
*   `--output-dir`, `-o`: Directory for output files (default: `./hybrid_output`).
*   `--require-email`, `-e`: Only include profiles with email addresses (default: True).
*   `--no-require-email`: Include profiles without email addresses.
*   `--max-profiles`, `-m`: Maximum profiles to process per topic (default: 20).
*   `--results-per-hashtag`, `-r`: Number of video results to fetch per hashtag via API (default: 50).
*   `--verbose`, `-v`: Enable detailed debug logging.

#### Python API

You can also import and use the `TikTokParser` class in your own Python scripts.

```python
import logging
import os
from src.tiktok_parser import TikTokParser

# Setup logging
logging.basicConfig(level=logging.INFO)

# Ensure API token is set (e.g., via environment variable)
# os.environ["APIFY_API_TOKEN"] = "your_api_token_here"

# Initialize the parser (optionally provide path to config file)
parser = TikTokParser()

# Define topics to parse
topics_to_parse = ["gaming", "travel"]

# Run the parser
results = parser.run(topics_to_parse)

# Process results (dictionary mapping topic to list of profiles)
for topic, profiles in results.items():
    print(f"\nTopic: {topic} - Found {len(profiles)} profiles")
    for profile in profiles[:3]: # Print first 3
        print(f"  - Username: {profile['username']}")
        print(f"    Followers: {profile['followers']}")
        print(f"    Likes: {profile['likes']}")
        print(f"    Following: {profile['following']}")
        print(f"    Videos: {profile['video_count']}")
        print(f"    Email: {profile['email']}")

print(f"\nOutput files saved in: {parser.output_dir}")
```

### Output

The parser generates output files in the specified `output_dir` (default: `./hybrid_output`).

*   **Topic-specific files**: For each topic processed, a file named `topic_<topic_name>.<format>` (e.g., `topic_art.csv`) is created containing the filtered profiles for that topic.
*   **Combined file**: A file named `all_topics.<format>` (e.g., `all_topics.csv`) is created containing all filtered profiles found across all processed topics.

The output files (CSV or JSON) contain the following columns/fields for each influencer:

*   `topic`: The topic/hashtag the profile was found under.
*   `username`: TikTok username.
*   `profile_url`: URL to the TikTok profile.
*   `followers`: Number of followers (from "fans" field in Profile API).
*   `likes`: Total number of likes received (from "heart" field in Profile API).
*   `following`: Number of accounts the user is following.
*   `friends`: Number of mutual follows (friends).
*   `video_count`: Number of videos posted by the user.
*   `bio`: User's profile bio text.
*   `email`: Extracted email address (if found and `require_email` is True).
*   `has_email`: Boolean indicating if an email was found in the bio.

### How the Hybrid Approach Works

The parser uses a two-step process to get the most comprehensive data:

1. **Topic Search**: Uses the TikTok Scraper API (`clockworks/tiktok-scraper`) to find usernames related to the specified topics/hashtags.

2. **Profile Data Extraction**: Uses the TikTok Profile Scraper API (`clockworks/tiktok-profile-scraper`) to get detailed profile data for each username, including:
   - Followers (from "fans" field)
   - Likes (from "heart" field)
   - Following count
   - Friends count
   - Video count

This hybrid approach provides the most comprehensive data while maintaining the ability to search by topic.
