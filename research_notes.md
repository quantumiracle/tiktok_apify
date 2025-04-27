# TikTok Parser Research Notes

## Official TikTok API Options

After investigating the official TikTok API documentation, we found:

1. **TikTok Research API**:
   - Limited to academic researchers from non-profit institutions
   - Requires application approval and adherence to terms of service
   - Provides access to account information including follower counts
   - Not suitable for general-purpose influencer discovery by topic

2. **TikTok Marketing API**:
   - Primarily designed for business advertising purposes
   - Does not provide comprehensive access to influencer discovery by topic
   - No clear support for email extraction

3. **Other TikTok APIs**:
   - Content Posting API, Display API, etc.
   - None specifically designed for influencer discovery or email extraction

## Web Scraping Approaches

Since official APIs don't meet our requirements, web scraping is the most viable approach:

### 1. Playwright-based Scraping

- **Advantages**:
  - Modern browser automation tool
  - Handles dynamic content well
  - Good for bypassing anti-scraping measures
  - Works with TikTok's JavaScript-heavy interface

- **Implementation Example**:
  ```python
  import asyncio
  import csv
  from playwright.async_api import Playwright, async_playwright
  
  # Browser launch and page creation
  browser = await playwright.chromium.launch(headless=False)
  context = await browser.new_context()
  page = await context.new_page()
  
  # Navigation to TikTok
  await page.goto("https://www.TikTok.com/foryou", timeout=120000)
  
  # Handle login popup
  await page.locator('//div[@id="loginContainer"]').wait_for()
  await page.get_by_role("link", name="Continue as guest").click()
  
  # Data extraction
  usernames = await extract_text(page, 'h3[data-e2e="video-author-uniqueid"]')
  descriptions = await extract_text(page, 'div[data-e2e="video-desc"]')
  likes = await extract_text(page, 'strong[data-e2e="like-count"]')
  comments = await extract_text(page, 'strong[data-e2e="comment-count"]')
  shares = await extract_text(page, 'strong[data-e2e="share-count"]')
  ```

### 2. Selenium-based Scraping

- **Advantages**:
  - Widely used browser automation tool
  - Good community support
  - Can handle TikTok's dynamic content

- **Limitations**:
  - May be slower than Playwright
  - Requires additional configuration for headless mode

### 3. Third-party Libraries and APIs

- **TikTokApi (David Teather)**:
  - Unofficial API wrapper for TikTok
  - Mentioned in the YouTube tutorial for email scraping
  - GitHub: https://github.com/davidteather/TikTokApi

- **Apify TikTok Scrapers**:
  - Commercial service with Python SDK
  - Offers hashtag scraping and email extraction capabilities
  - Handles rate limiting and anti-scraping measures

## Topic-based Search Methods

For finding influencers by topic, we have several approaches:

1. **Hashtag Search**:
   - Search TikTok by hashtags related to topics (e.g., #sports, #food)
   - Extract users who frequently post with these hashtags
   - Example repositories:
     - bellingcat/tiktok-hashtag-analysis
     - Apify's TikTok hashtag scrapers

2. **Keyword Search**:
   - Search for keywords in user bios and video descriptions
   - Filter users based on relevance to topics

3. **Category Navigation**:
   - Navigate through TikTok's category pages
   - Extract top creators from each category

## Email Extraction Methods

For extracting emails from profiles:

1. **Bio Parsing**:
   - Use regular expressions to extract email patterns from user bios
   - Example pattern: `r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'`

2. **Link Following**:
   - Extract links from user bios
   - Follow links to personal websites/landing pages
   - Extract contact information from these pages

3. **YouTube Tutorial Approach**:
   - Uses TikTokApi library
   - Searches for users by topic/hashtag
   - Extracts emails from user descriptions
   - Saves results to CSV

## Challenges and Considerations

1. **Anti-Scraping Measures**:
   - TikTok implements rate limiting
   - IP blocking for excessive requests
   - CAPTCHAs for suspicious activity

2. **Authentication Requirements**:
   - Some scraping approaches require TikTok accounts
   - May need to rotate accounts for large-scale scraping

3. **Dynamic Content**:
   - TikTok's interface is highly dynamic
   - Requires robust selectors and waiting strategies

4. **Legal and Ethical Considerations**:
   - Respect TikTok's terms of service
   - Only scrape publicly available data
   - Implement rate limiting to avoid overloading servers

## Recommended Approach

Based on our research, we recommend:

1. Use Playwright for browser automation
2. Implement hashtag/topic search functionality
3. Extract user profile data including follower counts and engagement metrics
4. Use regex pattern matching to identify profiles with email addresses
5. Export results to CSV with filtering capabilities
