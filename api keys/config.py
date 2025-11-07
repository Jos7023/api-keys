# Configuration settings
class Config:
    # Browser settings
    CHROME_DRIVER_PATH = './chromedriver'
    HEADLESS_MODE = False
    DEFAULT_TIMEOUT = 10
    
    # Data collection settings
    DEFAULT_COLLECTION_INTERVAL = 10  # seconds
    MAX_DATA_POINTS = 1000
    
    # Security settings
    ALLOWED_DOMAINS = [
        'aviator',
        'betting',
        'spribe'
    ]
    
    # Storage settings
    DATA_RETENTION_DAYS = 30