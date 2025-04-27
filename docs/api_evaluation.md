# Apify TikTok Scraper API Evaluation

Following the research phase, the `clockworks/tiktok-scraper` Actor on the Apify platform was evaluated for its suitability in replacing the previous web scraping approach.

## Evaluation Criteria vs. API Capabilities

1.  **Topic Search**: 
    - **Requirement**: Search for influencers based on topics (e.g., sports, food).
    - **API Capability**: Yes. The API accepts a `hashtags` array as input, allowing searches based on specific topics represented by hashtags.
    - **Feasibility**: High.

2.  **Influencer Data Extraction**:
    - **Requirement**: Extract account name, profile URL, follower count, and likes count.
    - **API Capability**: Yes. 
        - The documentation explicitly states that scraping **user profiles** yields details like "name, nickname, ID, bio, followers/following numbers".
        - Scraping by **hashtag** yields video results including `authorMeta.name`, `diggCount`, `shareCount`, `playCount`, `commentCount`. While follower counts aren't directly shown in the *hashtag video output example*, the associated author profile can likely be scraped subsequently using the author's name/ID obtained from the video results, or the API might provide richer author details depending on the specific scraping mode (hashtag vs. profile).
        - Profile URL: The video output example shows `webVideoUrl`. The author's profile URL should be derivable or available when scraping profiles directly.
    - **Feasibility**: High. Requires potentially combining hashtag search results with subsequent profile scrapes if hashtag search alone doesn't provide full author details.

3.  **Email Filtering**:
    - **Requirement**: Filter results to include only influencers who provide an email address.
    - **API Capability**: Likely. The documentation confirms that the user's **bio** is extracted when scraping profiles. Email addresses are typically placed in the bio.
    - **Implementation**: Email extraction will need to be implemented client-side by parsing the `bio` field obtained from the API response.
    - **Feasibility**: High, assuming emails are present in the bio text returned by the API.

4.  **Speed**: 
    - **Requirement**: Faster parsing than the previous web scraping method.
    - **API Capability**: Expected. As a dedicated cloud service, Apify's infrastructure should provide significantly faster data extraction compared to local browser automation.
    - **Feasibility**: High.

5.  **Python Integration**: 
    - **Requirement**: Integrate into a Python script.
    - **API Capability**: Yes. Apify provides an official Python client (`apify-client`).
    - **Feasibility**: High.

## Conclusion

The Apify TikTok Scraper (`clockworks/tiktok-scraper`) appears **highly suitable** for the task. It meets the core requirements for topic search and influencer data extraction. Email filtering is feasible by processing the bio text obtained from the API. Using this API service is expected to be significantly faster and more reliable than the previous web scraping approach.

The next step is to design the architecture for the new parser based on this API.
