# TikTok API Service Research

Based on user feedback regarding the slowness of the web scraping approach, research was conducted into using API services for faster TikTok data parsing, specifically focusing on Apify and MCP servers as suggested.

## Apify TikTok Scraper API

- **Provider**: Clockworks on the Apify Platform ([https://apify.com/clockworks/tiktok-scraper](https://apify.com/clockworks/tiktok-scraper))
- **Functionality**: Extracts data from TikTok videos, hashtags, and users. Can scrape profiles, posts, followers, likes, video details, music data, etc., using URLs or search queries.
- **Access**: Programmatic access via the Apify API using an API token.
- **Python Client**: Available (`apify-client`). The client allows calling specific Apify Actors (like `clockworks/tiktok-scraper`) with defined input parameters.
- **Example Usage**: The documentation shows examples of calling the actor with inputs like `hashtags: ["topic"]` and `resultsPerPage: 100`.
- **Relevance**: Directly addresses the need to search by topic (using hashtags) and extract user profile data (followers, likes). The availability of email addresses in the output needs further investigation during the evaluation phase.

## Model Context Protocol (MCP) and Apify MCP Server

- **MCP**: An open protocol designed to allow AI applications and agents to connect securely to external tools and data sources ([https://mcpservers.org/](https://mcpservers.org/)).
- **Apify MCP Server**: An implementation of MCP that exposes Apify Actors as tools for AI agents ([https://mcpservers.org/servers/apify/actors-mcp-server](https://mcpservers.org/servers/apify/actors-mcp-server)).
- **Functionality**: Allows an AI agent (like Claude Desktop, LibreChat, etc.) to call any Apify Actor, including the TikTok Scraper, using natural language commands or structured requests via the MCP protocol.
- **Relevance**: While powerful for integrating tools into AI agents, it adds an extra layer of abstraction (MCP server) compared to calling the Apify API directly. For building a dedicated script focused solely on TikTok parsing, using the `apify-client` to call the TikTok Scraper Actor directly seems more straightforward and efficient.

## Conclusion

Using the **Apify TikTok Scraper API directly via the `apify-client` Python library** appears to be the most suitable approach for replacing the slow web scraping method. It offers:

- **Speed**: Leverages Apify's infrastructure, likely much faster than local browser automation.
- **Focus**: Directly targets TikTok data extraction.
- **Simplicity**: Avoids the overhead of setting up and interacting with an MCP server, which is more relevant for AI agent tool integration.

The next step is to evaluate the specific input parameters and output data structure of the `clockworks/tiktok-scraper` Actor to confirm it can provide all necessary data points (especially email addresses) and meet the filtering requirements.
