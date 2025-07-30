"""
Configuration module for the Insurance Telegram Bot
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for bot settings"""
    
    # Bot configuration
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Insurance configuration
    DEFAULT_CURRENCY = 'USD'
    SUPPORTED_INSURANCE_TYPES = [
        'auto', 'home', 'health', 'travel', 'business'
    ]
    
    # Contact information
    CONTACT_PHONE = '1-800-INSURANCE'
    CONTACT_EMAIL = 'agents@insurance.com'
    CLAIMS_PHONE = '1-800-CLAIMS'
    
    # Business hours
    BUSINESS_HOURS = {
        'monday_friday': '8 AM - 8 PM',
        'saturday': '9 AM - 5 PM', 
        'sunday': '10 AM - 4 PM'
    }
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN is required")
        
        return True
