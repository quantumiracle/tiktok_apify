# TikTok Parser Architecture Design (API Approach)

This document outlines the architecture for the TikTok Parser, redesigned to use the Apify TikTok Scraper API for improved speed and reliability, based on user feedback and initial research/evaluation.

## 1. Overview

The goal is to parse TikTok to find influencers based on specific topics (hashtags), extract their profile information (username, profile URL, followers, likes, bio), filter for those with email addresses, and export the data.

This version replaces direct web scraping (using Playwright) with calls to the Apify `clockworks/tiktok-scraper` Actor via the `apify-client` Python library.

## 2. Core Components

The system will be composed of the following Python modules/classes:

1.  **`ApiClient`**: 
    -   Responsibilities: Manages interaction with the Apify API.
    -   Functions: Initializes the `ApifyClient` with the API token, calls specified Apify Actors (e.g., `clockworks/tiktok-scraper`) with given input, waits for runs to complete, retrieves dataset items.
    -   Dependencies: `apify-client` library.

2.  **`ConfigManager`**: 
    -   Responsibilities: Loads and provides configuration settings.
    -   Functions: Reads configuration from a file or environment variables (especially the Apify API token), provides access to settings like results limits, output format, etc.

3.  **`TopicProcessor`**: 
    -   Responsibilities: Handles the logic for searching TikTok based on topics (hashtags) and identifying relevant user profiles.
    -   Functions: Takes a list of hashtags, prepares input for the Apify Actor for hashtag search, triggers the API call via `ApiClient`, processes results to extract unique author identifiers (usernames/IDs).

4.  **`ProfileProcessor`**: 
    -   Responsibilities: Handles the logic for scraping detailed data for specific user profiles.
    -   Functions: Takes a list of user identifiers, prepares input for the Apify Actor for profile scraping, triggers the API call via `ApiClient`, retrieves profile data.

5.  **`DataProcessor`**: 
    -   Responsibilities: Parses and normalizes the raw data obtained from the Apify API (both hashtag and profile results).
    -   Functions: Extracts key fields (username, profile URL, followers, likes, bio) from the Apify dataset items into a consistent internal format (e.g., list of dictionaries or dataclasses).

6.  **`EmailExtractor`**: 
    -   Responsibilities: Identifies and extracts email addresses from text fields (primarily the user bio).
    -   Functions: Uses regular expressions to find potential email addresses within the extracted bio text.

7.  **`DataFilter`**: 
    -   Responsibilities: Filters the processed influencer data based on specified criteria.
    -   Functions: Primarily filters the list of influencers to include only those for whom an email address was successfully extracted (if the `require_email` flag is set).

8.  **`DataExporter`**: 
    -   Responsibilities: Exports the final, filtered data to the desired file format.
    -   Functions: Writes the list of influencer data to CSV or JSON files, handling both topic-specific and combined outputs.

9.  **`MainParser` (Orchestrator)**: 
    -   Responsibilities: Coordinates the overall workflow, managing the interaction between the different components.
    -   Functions: Initializes components, takes input topics and configuration, drives the process of searching hashtags, identifying profiles, scraping profiles, processing data, filtering, and exporting.

## 3. Workflow

The parser will follow these steps:

1.  **Initialization**: `MainParser` loads configuration (including Apify API token) via `ConfigManager` and initializes `ApiClient`.
2.  **Topic Iteration**: `MainParser` iterates through the list of input topics (hashtags).
3.  **Hashtag Search (per topic)**:
    a.  `TopicProcessor` prepares the input JSON for the `clockworks/tiktok-scraper` Actor, specifying the hashtag and desired number of results.
    b.  `ApiClient` is called to run the Actor and retrieve the resulting video dataset items.
    c.  `DataProcessor` extracts unique author usernames/IDs from the video results.
4.  **Profile Scraping (per topic)**:
    a.  `ProfileProcessor` prepares the input JSON for the `clockworks/tiktok-scraper` Actor (or potentially `apify/tiktok-profile-scraper` if more suitable), providing the list of unique author usernames/IDs obtained from the hashtag search.
    b.  `ApiClient` is called to run the Actor and retrieve the resulting profile dataset items.
5.  **Data Processing & Filtering (per topic)**:
    a.  `DataProcessor` iterates through the profile dataset items, extracting relevant fields (username, URL, followers, likes, bio) into a structured format.
    b.  `EmailExtractor` parses the `bio` field of each profile to find email addresses.
    c.  `DataFilter` filters the list of profiles based on the `require_email` configuration flag.
    d.  The filtered list of profiles for the current topic is stored.
6.  **Aggregation**: `MainParser` collects the filtered results from all processed topics.
7.  **Export**: `DataExporter` saves the aggregated results into the specified format (CSV/JSON), creating topic-specific files and a combined file.

## 4. Data Structures

-   **Apify Actor Input**: JSON object specific to the `clockworks/tiktok-scraper` Actor (e.g., `{"hashtags": ["topic"], "resultsPerPage": 100}` or `{"profiles": ["username1", "username2"], "resultsPerPage": 1}`).
-   **Apify Actor Output**: A list of JSON objects (dataset items) returned by the Actor run. The exact structure needs to be confirmed from API documentation or test runs, but is expected to contain fields like `authorMeta`, `text` (bio), `diggCount`, `followerCount`, `followingCount`, `webVideoUrl`, etc.
-   **Internal Profile Data**: A list of Python dictionaries or dataclasses representing cleaned influencer data, e.g.:
    ```python
    {
        "topic": "string",
        "username": "string",
        "profile_url": "string",
        "followers": "integer | string",
        "likes": "integer | string",
        "bio": "string",
        "email": "string | None",
        "has_email": "boolean"
    }
    ```

## 5. Configuration

Key configuration parameters:

-   `APIFY_API_TOKEN`: Essential for API authentication (should be handled securely).
-   `topics`: List of hashtags to search.
-   `results_per_hashtag`: Limit for initial video results per hashtag.
-   `max_profiles_per_topic`: Limit for the number of profiles to scrape per topic (derived from hashtag results).
-   `require_email`: Boolean flag to control email filtering.
-   `output_format`: "csv" or "json".
-   `output_dir`: Directory for saving results.

## 6. Error Handling & Considerations

-   API Errors: Implement robust error handling for API calls (e.g., invalid token, Actor not found, run failures, network issues).
-   Rate Limiting: Apify handles its own rate limiting, but be mindful of potential usage costs based on Actor runs and dataset items.
-   Data Consistency: The structure of data returned by the Apify Actor might change. The `DataProcessor` should be designed to handle potential variations or missing fields gracefully.
-   Email Extraction Accuracy: Regex for email extraction might need refinement to handle various formats and avoid false positives.
-   Cost Management: Apify usage incurs costs. The number of results requested and the frequency of runs should be configurable and monitored.
