import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    @staticmethod
    def _get_secret_or_env(key):
        """Get value from Streamlit secrets or environment variables"""
        try:
            import streamlit as st
            if hasattr(st, 'secrets') and key in st.secrets:
                return st.secrets[key]
        except:
            pass
        return os.getenv(key)
    
    # LLM Configuration
    GOOGLE_API_KEY = _get_secret_or_env.__func__('GOOGLE_API_KEY')
    
    # External API Keys
    EXCHANGE_RATE_API_KEY = _get_secret_or_env.__func__('EXCHANGE_RATE_API_KEY')
    GOOGLE_MAPS_API_KEY = _get_secret_or_env.__func__('GOOGLE_MAPS_API_KEY')
    
    # Application Settings
    DEBUG_MODE = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
    CACHE_TIMEOUT = int(os.getenv('CACHE_TIMEOUT', '300'))
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
    
    # API URLs
    EXCHANGE_RATE_API_URL = "https://api.exchangerate-api.com/v4/latest"
    
    @classmethod
    def validate_config(cls):
        """Validate that required API keys are present"""
        required_keys = ['GOOGLE_API_KEY']
        missing_keys = []
        
        for key in required_keys:
            if not getattr(cls, key):
                missing_keys.append(key)
        
        if missing_keys:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_keys)}")
        
        return True