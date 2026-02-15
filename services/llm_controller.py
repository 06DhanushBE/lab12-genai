import os
from langchain_google_genai import ChatGoogleGenerativeAI
from config import Config

class LLMAgentController:
    def __init__(self):
        try:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-pro",
                google_api_key=Config.GOOGLE_API_KEY,
                temperature=0.1
            )
        except Exception as e:
            print(f"Warning: Could not initialize LLM: {e}")
            self.llm = None
        
        # Supported countries for validation
        self.supported_countries = [
            'japan', 'india', 'united states', 'usa', 'united kingdom', 
            'uk', 'china', 'south korea', 'korea'
        ]
    
    def identify_country(self, query: str) -> str:
        """Extract country name from user query using LLM"""
        try:
            if not self.llm:
                return self._fallback_country_detection(query)
                
            prompt = f"""
            Extract the country name from this query: "{query}"
            
            Supported countries: Japan, India, United States (USA), United Kingdom (UK), China, South Korea
            
            Rules:
            - Return only the country name in lowercase
            - Use standard names: 'japan', 'india', 'united states', 'united kingdom', 'china', 'south korea'
            - If USA/US/America mentioned, return 'united states'
            - If UK/Britain/England mentioned, return 'united kingdom'
            - If Korea mentioned, return 'south korea'
            - If no valid country found, return 'unknown'
            
            Country:"""
            
            response = self.llm.invoke(prompt)
            
            country = response.content.strip().lower()
            
            # Validate and normalize the response
            return self._normalize_country_name(country)
            
        except Exception as e:
            # Fallback to keyword-based detection
            return self._fallback_country_detection(query)
    
    def _normalize_country_name(self, country: str) -> str:
        """Normalize country name to standard format"""
        country = country.lower().strip()
        
        # Handle common variations
        if country in ['usa', 'us', 'america', 'united states']:
            return 'united states'
        elif country in ['uk', 'britain', 'england', 'great britain', 'united kingdom']:
            return 'united kingdom'
        elif country in ['korea', 'south korea']:
            return 'south korea'
        elif country in ['japan', 'india', 'china']:
            return country
        else:
            return 'unknown'
    
    def _fallback_country_detection(self, query: str) -> str:
        """Fallback method using keyword matching"""
        query_lower = query.lower()
        
        # Simple keyword matching
        if any(word in query_lower for word in ['japan', 'japanese', 'tokyo']):
            return 'japan'
        elif any(word in query_lower for word in ['india', 'indian', 'mumbai', 'delhi']):
            return 'india'
        elif any(word in query_lower for word in ['usa', 'us', 'america', 'united states', 'new york']):
            return 'united states'
        elif any(word in query_lower for word in ['uk', 'britain', 'england', 'united kingdom', 'london']):
            return 'united kingdom'
        elif any(word in query_lower for word in ['china', 'chinese', 'beijing', 'shanghai']):
            return 'china'
        elif any(word in query_lower for word in ['korea', 'south korea', 'korean', 'seoul']):
            return 'south korea'
        else:
            return 'unknown'
    
    def generate_response_summary(self, data: dict) -> str:
        """Generate a natural language summary of the financial data"""
        try:
            if not self.llm:
                return self._generate_simple_summary(data)
                
            prompt = f"""
            Create a brief, friendly summary of this financial data:
            
            Country: {data.get('country_name', 'Unknown')}
            Currency: {data.get('currency', {}).get('name', 'Unknown')} ({data.get('currency', {}).get('code', 'XXX')})
            
            Exchange Rates (1 {data.get('currency', {}).get('code', 'XXX')} equals):
            {self._format_rates_for_prompt(data.get('exchange_rates', {}).get('rates', {}))}
            
            Stock Markets:
            {self._format_markets_for_prompt(data.get('stock_markets', []))}
            
            Write a 2-3 sentence summary highlighting the key information.
            """
            
            response = self.llm.invoke(prompt)
            
            return response.content.strip()
            
        except Exception as e:
            return self._generate_simple_summary(data)
    
    def _generate_simple_summary(self, data: dict) -> str:
        """Generate a simple summary without LLM"""
        country = data.get('country_name', 'the requested country')
        currency = data.get('currency', {})
        currency_name = currency.get('name', 'Unknown currency')
        currency_code = currency.get('code', 'XXX')
        
        return f"Here's the financial information for {country}. The official currency is {currency_name} ({currency_code}), and I've gathered the latest exchange rates and stock market data for you."
    
    def _format_rates_for_prompt(self, rates: dict) -> str:
        """Format exchange rates for LLM prompt"""
        if not rates:
            return "No exchange rate data available"
        
        formatted = []
        for currency, rate in rates.items():
            formatted.append(f"- {currency}: {rate}")
        
        return "\n".join(formatted)
    
    def _format_markets_for_prompt(self, markets: list) -> str:
        """Format stock market data for LLM prompt"""
        if not markets:
            return "No stock market data available"
        
        formatted = []
        for market in markets:
            exchange_name = market.get('exchange_name', 'Unknown Exchange')
            indices = market.get('indices', [])
            
            if indices:
                index_info = []
                for idx in indices:
                    name = idx.get('name', 'Unknown')
                    value = idx.get('current_value', 0)
                    change = idx.get('change_percent', 0)
                    index_info.append(f"{name}: {value} ({change:+.2f}%)")
                
                formatted.append(f"- {exchange_name}: {', '.join(index_info)}")
            else:
                formatted.append(f"- {exchange_name}: No index data available")
        
        return "\n".join(formatted)
    
    def handle_errors(self, error: Exception) -> str:
        """Generate user-friendly error messages"""
        error_msg = str(error).lower()
        
        if 'api' in error_msg or 'key' in error_msg:
            return "I'm having trouble connecting to external services. Please check your API configuration."
        elif 'country' in error_msg or 'unknown' in error_msg:
            return "I couldn't identify the country from your query. Please try asking about Japan, India, US, UK, China, or South Korea."
        else:
            return "I encountered an error while processing your request. Please try again."