import os
import sys
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # LLM Configuration - Check both secrets and env vars
    GOOGLE_API_KEY = st.secrets.get('GOOGLE_API_KEY') if 'streamlit' in sys.modules else os.getenv('GOOGLE_API_KEY')
    
    # External API Keys
    EXCHANGE_RATE_API_KEY = st.secrets.get('EXCHANGE_RATE_API_KEY') if 'streamlit' in sys.modules else os.getenv('EXCHANGE_RATE_API_KEY')
    GOOGLE_MAPS_API_KEY = st.secrets.get('GOOGLE_MAPS_API_KEY') if 'streamlit' in sys.modules else os.getenv('GOOGLE_MAPS_API_KEY')
    
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