# TikTok Parser - Web Interface

This web interface provides a user-friendly way to interact with the TikTok Parser tool, allowing you to find TikTok influencers based on topics (hashtags) and extract their profile data.

## Features

- **Simple Form Interface**: Easily configure and run the TikTok Parser without using the command line
- **Topic Visualization**: See your topics displayed as tags as you type them
- **API Token Storage**: Option to save your Apify API token in the browser for convenience
- **Real-time Feedback**: Loading indicators and status messages keep you informed
- **Results Display**: View a summary of results and sample profiles directly in the browser
- **Download Options**: Download results in CSV or JSON format for further analysis

## Installation

1. **Install Dependencies**

   Make sure you have Python 3.8 or higher installed, then install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Web Application**

   Start the Flask development server:

   ```bash
   python app.py
   ```

   The web interface will be available at [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Usage

1. **Enter Your Apify API Token**

   - Get your API token from the [Apify Console](https://console.apify.com/account/integrations)
   - Enter it in the form
   - Optionally check "Save token in browser" to store it for future sessions

2. **Specify Topics**

   - Enter comma-separated topics (hashtags) to search for (e.g., "art, food, technology")
   - The topics will appear as tags below the input field

3. **Configure Options**

   - **Results Per Hashtag**: Number of video results to fetch per hashtag (default: 20)
   - **Max Profiles Per Topic**: Maximum profiles to process per topic (default: 20)
   - **Require Email**: Toggle to include only profiles with email addresses
   - **Output Format**: Choose between CSV and JSON formats

4. **Run the Parser**

   - Click the "Run Parser" button
   - A loading indicator will appear while the parser is running
   - This may take several minutes depending on the number of topics and profiles

5. **View and Download Results**

   - Once processing is complete, you'll be redirected to the results page
   - View a summary of the results and sample profiles
   - Download the full results for all topics or individual topics

## Notes

- The parser uses a hybrid approach with two Apify APIs:
  1. **TikTok Scraper API** for topic-based searching
  2. **TikTok Profile Scraper API** for detailed profile metrics
- Running the parser may incur costs on your Apify account (approximately $3-4 per 1000 items)
- The output files are saved in the `hybrid_output` directory

## Troubleshooting

- **API Token Issues**: Ensure your Apify API token is valid and has sufficient credits
- **No Results**: Try different topics or increase the "Results Per Hashtag" value
- **Processing Takes Too Long**: Reduce the number of topics or the "Max Profiles Per Topic" value

## Related Documentation

- [TikTok Parser README](README.md): Main documentation for the TikTok Parser
- [Usage Guide](docs/usage_guide.md): Detailed usage instructions for the command-line interface
