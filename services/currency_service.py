from models.financial_data import CurrencyInfo

class CurrencyService:
    def __init__(self):
        self.country_currencies = {
            'japan': {'name': 'Japanese Yen', 'code': 'JPY', 'symbol': '¥'},
            'india': {'name': 'Indian Rupee', 'code': 'INR', 'symbol': '₹'},
            'united states': {'name': 'US Dollar', 'code': 'USD', 'symbol': '$'},
            'usa': {'name': 'US Dollar', 'code': 'USD', 'symbol': '$'},
            'united kingdom': {'name': 'British Pound', 'code': 'GBP', 'symbol': '£'},
            'uk': {'name': 'British Pound', 'code': 'GBP', 'symbol': '£'},
            'china': {'name': 'Chinese Yuan', 'code': 'CNY', 'symbol': '¥'},
            'south korea': {'name': 'South Korean Won', 'code': 'KRW', 'symbol': '₩'},
            'korea': {'name': 'South Korean Won', 'code': 'KRW', 'symbol': '₩'}
        }
    
    def get_official_currency(self, country: str) -> CurrencyInfo:
        """Get official currency information for a country"""
        country_key = country.lower().strip()
        
        # Handle common variations
        country_variations = {
            'us': 'usa',
            'america': 'usa',
            'britain': 'uk',
            'england': 'uk',
            'great britain': 'uk',
            'south korea': 'south korea',
            'republic of korea': 'south korea'
        }
        
        if country_key in country_variations:
            country_key = country_variations[country_key]
        
        if country_key in self.country_currencies:
            currency_data = self.country_currencies[country_key]
            return CurrencyInfo(
                name=currency_data['name'],
                code=currency_data['code'],
                symbol=currency_data['symbol']
            )
        else:
            # Default fallback
            return CurrencyInfo(
                name=f"{country.title()} Currency",
                code="XXX",
                symbol="?"
            )
    
    def validate_currency_code(self, code: str) -> bool:
        """Validate if a currency code is supported"""
        valid_codes = [curr['code'] for curr in self.country_currencies.values()]
        return code.upper() in valid_codes
    
    def get_supported_countries(self) -> list:
        """Get list of supported countries"""
        return list(self.country_currencies.keys())