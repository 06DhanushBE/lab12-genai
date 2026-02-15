from datetime import datetime
from typing import Optional
from models.financial_data import CountryFinancialData
from services.currency_service import CurrencyService
from services.exchange_rate_service import ExchangeRateService
from services.stock_market_service import StockMarketService
from services.llm_controller import LLMAgentController

class DataOrchestrator:
    def __init__(self):
        self.currency_service = CurrencyService()
        self.exchange_rate_service = ExchangeRateService()
        self.stock_market_service = StockMarketService()
        self.llm_controller = LLMAgentController()
    
    def get_country_financial_data(self, query: str) -> Optional[CountryFinancialData]:
        """Orchestrate data collection for a country financial query"""
        try:
            # Step 1: Identify country from query
            country = self.llm_controller.identify_country(query)
            
            if country == 'unknown':
                raise ValueError("Could not identify a supported country from the query")
            
            # Step 2: Get currency information
            currency_info = self.currency_service.get_official_currency(country)
            
            # Step 3: Get exchange rates
            exchange_rates = self.exchange_rate_service.get_exchange_rates(
                currency_info.code, 
                ['USD', 'INR', 'GBP', 'EUR']
            )
            
            # Step 4: Get stock market information
            stock_markets = self.stock_market_service.get_stock_market_info(country)
            
            # Step 5: Get exchange locations
            exchange_locations = self.stock_market_service.get_exchange_locations(country)
            
            # Step 6: Compile all data
            financial_data = CountryFinancialData(
                country_name=country.title(),
                currency=currency_info,
                exchange_rates=exchange_rates,
                stock_markets=stock_markets,
                exchange_locations=exchange_locations,
                timestamp=datetime.now()
            )
            
            return financial_data
            
        except Exception as e:
            print(f"Error in data orchestration: {str(e)}")
            return None
    
    def generate_summary(self, financial_data: CountryFinancialData) -> str:
        """Generate a natural language summary of the financial data"""
        try:
            data_dict = financial_data.to_dict()
            return self.llm_controller.generate_response_summary(data_dict)
        except Exception as e:
            return f"Here's the financial information for {financial_data.country_name}."
    
    def validate_query(self, query: str) -> bool:
        """Validate if the query can be processed"""
        if not query or len(query.strip()) < 3:
            return False
        
        # Check if query contains any country-related keywords
        country_keywords = [
            'japan', 'india', 'usa', 'us', 'america', 'united states',
            'uk', 'britain', 'england', 'united kingdom', 'china', 
            'korea', 'south korea', 'currency', 'exchange', 'stock', 'market'
        ]
        
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in country_keywords)