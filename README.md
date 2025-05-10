# TikTok Influencer Parser - Gradio App

This Hugging Face Space provides a user-friendly interface to find TikTok influencers based on specific topics (hashtags), extract their profile data, and filter for profiles that include an email address in their bio.

## Features

- **Easy-to-use Interface**: Simple web UI built with Gradio
- **Topic Search**: Find TikTok users associated with specific hashtags
- **Comprehensive Data Extraction**: Get detailed profile information
- **Email Filtering**: Identify profiles with email addresses in their bio
- **CSV Download**: Export results in a structured format

## How to Use

1. Enter your [Apify API token](https://console.apify.com/settings/integrations)
2. Specify topics/hashtags (comma or space separated)
3. Adjust settings:
   - Results per hashtag (5-100)
   - Maximum profiles per topic (5-100)
   - Whether to require email in bio
4. Click "Find Influencers"
5. View summary and download CSV results

## How It Works

This tool uses a hybrid approach with two Apify APIs:
1. **TikTok Scraper API** for topic-based searching
2. **TikTok Profile Scraper API** for detailed profile metrics

The process:
1. Searches for TikTok users associated with your specified hashtags
2. Retrieves detailed profile information (followers, likes, bio, etc.)
3. Optionally filters for profiles containing email addresses
4. Provides results as a downloadable CSV file

## Getting an Apify API Token

1. Create an account on [Apify](https://apify.com/)
2. Go to [Account Settings → Integrations](https://console.apify.com/settings/integrations)
3. Generate a new API token
4. Copy and paste the token into the app

## Output Data

The CSV output includes the following data for each profile:
- Username
- Profile URL
- Follower Count
- Total Likes
- Following Count
- Friends Count
- Video Count
- Bio Text
- Email (if available)
- Topic/Hashtag

## Note on Usage Costs

Using the Apify APIs incurs costs of approximately $3-4 per 1000 items. Please be mindful of your usage.
