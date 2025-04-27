# TikTok Parser (Hybrid API Approach)

This project provides a Python tool to parse TikTok and find influencers based on specific topics (hashtags), extract their profile data (username, URL, followers, likes, following, friends, video count, bio), and filter for profiles that include an email address in their bio.

This version uses a **hybrid approach** with two Apify APIs:
1. **TikTok Scraper API** for topic-based searching
2. **TikTok Profile Scraper API** for detailed profile metrics

Price:

$3-4/1000 items

## Features

*   **Topic Search**: Finds TikTok users associated with specific hashtags (e.g., "art", "food", "technology") using the TikTok Scraper API.
*   **Comprehensive Data Extraction**: Retrieves detailed profile information using the TikTok Profile Scraper API:
    *   Username
    *   Profile URL
    *   Follower Count (from "fans" field)
    *   Total Likes (from "heart" field)
    *   Following Count
    *   Friends Count (mutual follows)
    *   Video Count
    *   Bio Text
*   **Email Filtering**: Identifies and extracts email addresses from user bios and allows filtering results to include only profiles with emails.
*   **Hybrid API Integration**: Leverages two complementary Apify actors:
    *   `clockworks/tiktok-scraper` for topic-based searching
    *   `clockworks/tiktok-profile-scraper` for detailed profile metrics
*   **Configurable**: Settings like API token, results limits, and output format can be configured.
*   **Output Formats**: Exports results to CSV or JSON files.
*   **Usage Options**: Can be used via a command-line interface (CLI) or imported as a Python library.

## Project Structure

```
tiktok_parser/
├── src/
│   ├── __init__.py
│   ├── api_client.py         # Handles communication with both Apify APIs
│   ├── config_manager.py     # Manages configuration
│   ├── data_exporter.py      # Exports data to files (CSV, JSON)
│   ├── data_filter.py        # Filters profiles based on criteria (e.g., email)
│   ├── data_processor.py     # Parses and normalizes API data
│   ├── email_extractor.py    # Extracts emails from text
│   ├── profile_processor.py  # Retrieves detailed profile data via Profile Scraper API
│   ├── tiktok_parser.py      # Main orchestrator class
│   └── topic_processor.py    # Searches topics/hashtags via TikTok Scraper API
├── docs/
│   ├── architecture_design_api.md # Design document for API approach
│   ├── api_evaluation.md       # Evaluation of Apify APIs
│   ├── api_options.md          # Research on API options
│   └── usage_guide.md          # Detailed installation and usage instructions
├── cli.py                    # Command-line interface script
├── config.json.example       # Example configuration file
├── README.md                 # This file
├── requirements.txt          # Python dependencies (primarily apify-client)
└── todo.md                   # Development task checklist
```

## Getting Started

Please refer to the detailed **[Installation and Usage Guide](docs/usage_guide.md)** for instructions on:

*   Installation
*   Configuration (including setting up your Apify API token)
*   Using the Command-Line Interface (CLI)
*   Using the Python API
*   Understanding the output formats

## Dependencies

*   `apify-client`: The official Python client for the Apify API.

Install dependencies using:
```bash
pip install -r requirements.txt
# or
pip install apify-client
```

## Basic CLI Usage

1.  **Set API Token**: Export your Apify API token as an environment variable:
    ```bash
    export APIFY_API_TOKEN="your_apify_api_token_here"
    ```
2.  **Run the Parser**:
    ```bash
    python cli.py <topic1> <topic2> ... --require-email
    ```
    Example:
    ```bash
    python cli.py art food technology --require-email
    ```

Results will be saved in the `hybrid_output` directory by default.

## How the Hybrid Approach Works

The parser uses a two-step process:

1. **Topic Search**: Uses the TikTok Scraper API (`clockworks/tiktok-scraper`) to find usernames related to the specified topics/hashtags.

2. **Profile Data Extraction**: Uses the TikTok Profile Scraper API (`clockworks/tiktok-profile-scraper`) to get detailed profile data for each username, including:
   - Followers (from "fans" field)
   - Likes (from "heart" field)
   - Following count
   - Friends count
   - Video count

This hybrid approach provides the most comprehensive data while maintaining the ability to search by topic.
