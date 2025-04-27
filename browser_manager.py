"""
Browser Manager Module - Handles browser initialization and management for TikTok Parser
"""

import asyncio
from playwright.async_api import async_playwright, Page, Browser, BrowserContext
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('browser_manager')

class BrowserManager:
    """
    Manages browser initialization, navigation, and interaction for TikTok scraping
    """
    
    def __init__(self, config=None):
        """
        Initialize the browser manager with configuration
        
        Args:
            config (dict, optional): Configuration dictionary for browser settings
        """
        self.config = config or {}
        self.browser = None
        self.context = None
        self.page = None
        self.playwright = None
        
        # Default configuration
        self.headless = self.config.get('headless', False)
        self.user_agent = self.config.get('user_agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        self.viewport = self.config.get('viewport', {'width': 1280, 'height': 800})
        self.timeout = self.config.get('page_load_timeout', 30000)
        self.request_delay = self.config.get('request_delay', 2)
    
    async def initialize(self):
        """
        Initialize the browser, context, and page
        
        Returns:
            Page: Playwright page object
        """
        logger.info("Initializing browser")
        self.playwright = await async_playwright().start()
        
        # Launch browser
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless
        )
        
        # Create a new browser context
        self.context = await self.browser.new_context(
            user_agent=self.user_agent,
            viewport=self.viewport
        )
        
        # Create a new page
        self.page = await self.context.new_page()
        
        # Set default timeout
        self.page.set_default_timeout(self.timeout)
        
        logger.info("Browser initialized successfully")
        return self.page
    
    async def navigate(self, url):
        """
        Navigate to a URL
        
        Args:
            url (str): URL to navigate to
            
        Returns:
            Page: Playwright page object
        """
        if not self.page:
            await self.initialize()
        
        logger.info(f"Navigating to {url}")
        await self.page.goto(url, wait_until='networkidle', timeout=self.timeout)
        
        # Add delay to avoid rate limiting
        await asyncio.sleep(self.request_delay)
        
        return self.page
    
    async def handle_login_popup(self):
        """
        Handle TikTok login popup by clicking "Continue as guest"
        
        Returns:
            bool: True if popup was handled, False otherwise
        """
        try:
            # Wait for login container to appear
            await self.page.wait_for_selector('//div[@id="loginContainer"]', timeout=5000)
            
            # Click "Continue as guest" button
            await self.page.click('text="Continue as guest"')
            
            logger.info("Login popup handled successfully")
            await asyncio.sleep(2)
            return True
        except Exception as e:
            logger.info(f"No login popup detected or unable to handle: {e}")
            return False
    
    async def scroll_page(self, scrolls=5, scroll_delay=1):
        """
        Scroll down the page to load more content
        
        Args:
            scrolls (int): Number of times to scroll
            scroll_delay (int): Delay between scrolls in seconds
            
        Returns:
            Page: Playwright page object
        """
        logger.info(f"Scrolling page {scrolls} times")
        
        for i in range(scrolls):
            # Scroll down
            await self.page.evaluate('window.scrollBy(0, window.innerHeight)')
            
            # Wait for content to load
            await asyncio.sleep(scroll_delay)
            
            logger.debug(f"Completed scroll {i+1}/{scrolls}")
        
        return self.page
    
    async def extract_text(self, selector):
        """
        Extract text from elements matching a selector
        
        Args:
            selector (str): CSS selector for elements
            
        Returns:
            list: List of extracted text strings
        """
        elements = await self.page.query_selector_all(selector)
        texts = []
        
        for element in elements:
            text = await element.inner_text() if element else ""
            texts.append(text)
        
        return texts
    
    async def close(self):
        """
        Close the browser and all associated resources
        """
        logger.info("Closing browser")
        
        if self.page:
            await self.page.close()
            self.page = None
        
        if self.context:
            await self.context.close()
            self.context = None
        
        if self.browser:
            await self.browser.close()
            self.browser = None
        
        if self.playwright:
            await self.playwright.stop()
            self.playwright = None
        
        logger.info("Browser closed successfully")
