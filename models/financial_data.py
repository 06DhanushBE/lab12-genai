from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class CurrencyInfo:
    name: str
    code: str
    symbol: str

@dataclass
class ExchangeRateInfo:
    base_currency: str
    rates: Dict[str, float]  # {target_currency: rate}
    last_updated: datetime

@dataclass
class LocationInfo:
    name: str
    address: str
    latitude: float
    longitude: float
    map_embed_url: Optional[str] = None

@dataclass
class IndexInfo:
    name: str
    symbol: str
    current_value: float
    change_percent: float
    last_updated: datetime

@dataclass
class StockMarketInfo:
    exchange_name: str
    indices: List[IndexInfo]
    location: LocationInfo

@dataclass
class CountryFinancialData:
    country_name: str
    currency: CurrencyInfo
    exchange_rates: ExchangeRateInfo
    stock_markets: List[StockMarketInfo]
    exchange_locations: List[LocationInfo]
    timestamp: datetime
    
    def to_dict(self) -> dict:
        """Convert to dictionary for easy serialization"""
        return {
            'country_name': self.country_name,
            'currency': {
                'name': self.currency.name,
                'code': self.currency.code,
                'symbol': self.currency.symbol
            },
            'exchange_rates': {
                'base_currency': self.exchange_rates.base_currency,
                'rates': self.exchange_rates.rates,
                'last_updated': self.exchange_rates.last_updated.isoformat()
            },
            'stock_markets': [
                {
                    'exchange_name': market.exchange_name,
                    'indices': [
                        {
                            'name': idx.name,
                            'symbol': idx.symbol,
                            'current_value': idx.current_value,
                            'change_percent': idx.change_percent,
                            'last_updated': idx.last_updated.isoformat()
                        } for idx in market.indices
                    ],
                    'location': {
                        'name': market.location.name,
                        'address': market.location.address,
                        'latitude': market.location.latitude,
                        'longitude': market.location.longitude
                    }
                } for market in self.stock_markets
            ],
            'timestamp': self.timestamp.isoformat()
        }