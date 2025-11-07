from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import base64

class BrowserAutomation:
    def __init__(self):
        self.driver = None
        self.wait = None
    
    def init_driver(self, headless=False):
        """Initialize Chrome driver with necessary options"""
        chrome_options = Options()
        
        if headless:
            chrome_options.add_argument('--headless')
        
        # Add options for better automation
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Enable performance logging for network analysis
        chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        self.wait = WebDriverWait(self.driver, 10)
        return self.driver
    
    def navigate_to_url(self, driver, url):
        """Navigate to target URL"""
        driver.get(url)
        time.sleep(3)  # Wait for page to load
    
    def wait_for_element(self, selector, by=By.CSS_SELECTOR, timeout=10):
        """Wait for specific element to load"""
        return self.wait.until(EC.presence_of_element_located((by, selector)))
    
    def take_screenshot(self, driver, filename='screenshot.png'):
        """Take screenshot of current page"""
        driver.save_screenshot(filename)
        with open(filename, 'rb') as f:
            screenshot_data = base64.b64encode(f.read()).decode('utf-8')
        return screenshot_data
    
    def cleanup(self):
        """Clean up browser instance"""
        if self.driver:
            self.driver.quit()
            self.driver = None