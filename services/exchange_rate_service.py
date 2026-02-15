import requests
from datetime import datetime
from typing import Dict, List
from models.financial_data import ExchangeRateInfo
from config import Config

class ExchangeRateService:
    def __init__(self):
        # Using ExchangeRate-API with your API key for better reliability
        self.api_key = Config.EXCHANGE_RATE_API_KEY
        if self.api_key:
            self.base_url = "https://v6.exchangerate-api.com/v6"
        else:
            # Fallback to free service
            self.base_url = "https://api.exchangerate.host"
        self.cache = {}
        self.cache_timeout = 300  # 5 minutes
        
    def get_exchange_rates(self, base_currency: str, target_currencies: List[str] = None) -> ExchangeRateInfo:
        """Get exchange rates for base currency to target currencies"""
        if target_currencies is None:
            target_currencies = ['USD', 'INR', 'GBP', 'EUR']
        
        # Check cache first
        cache_key = f"{base_currency}_{','.join(sorted(target_currencies))}"
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]['data']
        
        try:
            # Use premium ExchangeRate-API if key is available
            if self.api_key:
                url = f"{self.base_url}/{self.api_key}/latest/{base_currency}"
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                
                if data.get('result') == 'success':
                    all_rates = data.get('conversion_rates', {})
                    # Filter to only requested currencies
                    rates = {curr: all_rates.get(curr, 0.0) for curr in target_currencies if curr in all_rates}
                else:
                    raise Exception(f"API Error: {data.get('error-type', 'Unknown error')}")
            else:
                # Use free exchangerate.host API
                url = f"{self.base_url}/latest"
                params = {
                    'base': base_currency,
                    'symbols': ','.join(target_currencies)
                }
                
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                
                if data.get('success', True):
                    rates = data.get('rates', {})
                else:
                    raise Exception(f"API Error: {data.get('error', 'Unknown error')}")
            
            exchange_rate_info = ExchangeRateInfo(
                base_currency=base_currency,
                rates=rates,
                last_updated=datetime.now()
            )
            
            # Cache the result
            self.cache[cache_key] = {
                'data': exchange_rate_info,
                'timestamp': datetime.now()
            }
            
            return exchange_rate_info
                
        except Exception as e:
            # Fallback to mock data if API fails
            return self._get_fallback_rates(base_currency, target_currencies)
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cached data is still valid"""
        if cache_key not in self.cache:
            return False
        
        cache_time = self.cache[cache_key]['timestamp']
        return (datetime.now() - cache_time).seconds < self.cache_timeout
    
    def _get_fallback_rates(self, base_currency: str, target_currencies: List[str]) -> ExchangeRateInfo:
        """Provide fallback exchange rates when API is unavailable"""
        # Basic fallback rates (approximate values)
        fallback_rates = {
            'USD': {'INR': 83.0, 'GBP': 0.79, 'EUR': 0.85, 'USD': 1.0},
            'INR': {'USD': 0.012, 'GBP': 0.0095, 'EUR': 0.010, 'INR': 1.0},
            'GBP': {'USD': 1.27, 'INR': 105.0, 'EUR': 1.08, 'GBP': 1.0},
            'EUR': {'USD': 1.18, 'INR': 98.0, 'GBP': 0.93, 'EUR': 1.0},
            'JPY': {'USD': 0.0067, 'INR': 0.56, 'GBP': 0.0053, 'EUR': 0.0057},
            'CNY': {'USD': 0.14, 'INR': 11.6, 'GBP': 0.11, 'EUR': 0.12},
            'KRW': {'USD': 0.00075, 'INR': 0.062, 'GBP': 0.00059, 'EUR': 0.00064}
        }
        
        rates = {}
        base_rates = fallback_rates.get(base_currency, {})
        
        for target in target_currencies:
            rates[target] = base_rates.get(target, 1.0)
        
        return ExchangeRateInfo(
            base_currency=base_currency,
            rates=rates,
            last_updated=datetime.now()
        )