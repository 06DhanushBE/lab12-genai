import yfinance as yf
from datetime import datetime
from typing import List, Dict
from models.financial_data import StockMarketInfo, IndexInfo, LocationInfo

class StockMarketService:
    def __init__(self):
        self.country_exchanges = {
            'japan': {
                'exchanges': ['Tokyo Stock Exchange'],
                'indices': [
                    {'name': 'Nikkei 225', 'symbol': '^N225'},
                    {'name': 'TOPIX', 'symbol': '^TPX'}
                ],
                'locations': [{
                    'name': 'Tokyo Stock Exchange',
                    'address': '2-1 Nihonbashi-Kabutocho, Chuo City, Tokyo, Japan',
                    'latitude': 35.6762,
                    'longitude': 139.7731
                }]
            },
            'india': {
                'exchanges': ['Bombay Stock Exchange', 'National Stock Exchange'],
                'indices': [
                    {'name': 'BSE Sensex', 'symbol': '^BSESN'},
                    {'name': 'Nifty 50', 'symbol': '^NSEI'}
                ],
                'locations': [
                    {
                        'name': 'Bombay Stock Exchange',
                        'address': 'Phiroze Jeejeebhoy Towers, Dalal Street, Mumbai, India',
                        'latitude': 18.9292,
                        'longitude': 72.8342
                    },
                    {
                        'name': 'National Stock Exchange',
                        'address': 'Exchange Plaza, Bandra Kurla Complex, Mumbai, India',
                        'latitude': 19.0596,
                        'longitude': 72.8656
                    }
                ]
            },
            'united states': {
                'exchanges': ['New York Stock Exchange', 'NASDAQ'],
                'indices': [
                    {'name': 'S&P 500', 'symbol': '^GSPC'},
                    {'name': 'Dow Jones', 'symbol': '^DJI'},
                    {'name': 'NASDAQ', 'symbol': '^IXIC'}
                ],
                'locations': [
                    {
                        'name': 'New York Stock Exchange',
                        'address': '11 Wall Street, New York, NY, USA',
                        'latitude': 40.7074,
                        'longitude': -74.0113
                    },
                    {
                        'name': 'NASDAQ',
                        'address': '151 W 42nd Street, New York, NY, USA',
                        'latitude': 40.7589,
                        'longitude': -73.9851
                    }
                ]
            },
            'united kingdom': {
                'exchanges': ['London Stock Exchange'],
                'indices': [
                    {'name': 'FTSE 100', 'symbol': '^FTSE'},
                    {'name': 'FTSE 250', 'symbol': '^FTMC'}
                ],
                'locations': [{
                    'name': 'London Stock Exchange',
                    'address': '10 Paternoster Square, London, UK',
                    'latitude': 51.5142,
                    'longitude': -0.0991
                }]
            },
            'china': {
                'exchanges': ['Shanghai Stock Exchange', 'Shenzhen Stock Exchange'],
                'indices': [
                    {'name': 'Shanghai Composite', 'symbol': '000001.SS'},
                    {'name': 'Shenzhen Component', 'symbol': '399001.SZ'}
                ],
                'locations': [
                    {
                        'name': 'Shanghai Stock Exchange',
                        'address': '528 Pudong South Road, Shanghai, China',
                        'latitude': 31.2304,
                        'longitude': 121.4737
                    },
                    {
                        'name': 'Shenzhen Stock Exchange',
                        'address': '5045 Shennan East Road, Shenzhen, China',
                        'latitude': 22.5431,
                        'longitude': 114.0579
                    }
                ]
            },
            'south korea': {
                'exchanges': ['Korea Exchange'],
                'indices': [
                    {'name': 'KOSPI', 'symbol': '^KS11'},
                    {'name': 'KOSDAQ', 'symbol': '^KQ11'}
                ],
                'locations': [{
                    'name': 'Korea Exchange',
                    'address': '76 Yeouinaru-ro, Seoul, South Korea',
                    'latitude': 37.5262,
                    'longitude': 126.9320
                }]
            }
        }
    
    def get_major_exchanges(self, country: str) -> List[str]:
        """Get major stock exchanges for a country"""
        country_key = country.lower()
        if country_key in self.country_exchanges:
            return self.country_exchanges[country_key]['exchanges']
        return []
    
    def get_stock_market_info(self, country: str) -> List[StockMarketInfo]:
        """Get complete stock market information for a country"""
        country_key = country.lower()
        if country_key not in self.country_exchanges:
            return []
        
        country_data = self.country_exchanges[country_key]
        stock_markets = []
        
        # Get index values
        indices_data = self._get_current_index_values(country_data['indices'])
        
        # Group indices by exchange (simplified - assuming one exchange per country for now)
        for i, exchange_name in enumerate(country_data['exchanges']):
            location = LocationInfo(
                name=country_data['locations'][i]['name'],
                address=country_data['locations'][i]['address'],
                latitude=country_data['locations'][i]['latitude'],
                longitude=country_data['locations'][i]['longitude']
            )
            
            # For simplicity, assign all indices to first exchange
            if i == 0:
                stock_market = StockMarketInfo(
                    exchange_name=exchange_name,
                    indices=indices_data,
                    location=location
                )
            else:
                stock_market = StockMarketInfo(
                    exchange_name=exchange_name,
                    indices=[],
                    location=location
                )
            
            stock_markets.append(stock_market)
        
        return stock_markets
    
    def _get_current_index_values(self, indices: List[Dict]) -> List[IndexInfo]:
        """Fetch current values for stock indices"""
        index_info_list = []
        
        # Fallback data for when APIs fail
        fallback_data = {
            '^N225': {'value': 28756.86, 'change': 1.2},  # Nikkei 225
            '^TPX': {'value': 2041.33, 'change': 0.8},    # TOPIX
            '^BSESN': {'value': 76693.36, 'change': 0.5}, # BSE Sensex
            '^NSEI': {'value': 23311.80, 'change': 0.4},  # Nifty 50
            '^GSPC': {'value': 5026.61, 'change': 0.7},   # S&P 500
            '^DJI': {'value': 38797.38, 'change': 0.3},   # Dow Jones
            '^IXIC': {'value': 17918.99, 'change': 1.1},  # NASDAQ
            '^FTSE': {'value': 8292.66, 'change': 0.2},   # FTSE 100
            '^FTMC': {'value': 20845.12, 'change': 0.1},  # FTSE 250
            '000001.SS': {'value': 2974.01, 'change': -0.3}, # Shanghai Composite
            '399001.SZ': {'value': 8849.13, 'change': -0.1}, # Shenzhen Component
            '^KS11': {'value': 2417.59, 'change': 0.6},   # KOSPI
            '^KQ11': {'value': 691.77, 'change': 0.9}     # KOSDAQ
        }
        
        for index_data in indices:
            try:
                # Try to get real data first
                ticker = yf.Ticker(index_data['symbol'])
                hist = ticker.history(period="1d", timeout=5)  # Reduced timeout and period
                
                if not hist.empty and len(hist) > 0:
                    current_value = hist['Close'].iloc[-1]
                    
                    # Try to get previous day for change calculation
                    try:
                        hist_2d = ticker.history(period="2d", timeout=3)
                        if len(hist_2d) > 1:
                            prev_value = hist_2d['Close'].iloc[-2]
                            change_percent = ((current_value - prev_value) / prev_value) * 100
                        else:
                            change_percent = 0.0
                    except:
                        change_percent = 0.0
                    
                    index_info = IndexInfo(
                        name=index_data['name'],
                        symbol=index_data['symbol'],
                        current_value=round(float(current_value), 2),
                        change_percent=round(float(change_percent), 2),
                        last_updated=datetime.now()
                    )
                    index_info_list.append(index_info)
                    print(f"✅ Got real data for {index_data['name']}: {current_value}")
                else:
                    raise Exception("No data available")
                    
            except Exception as e:
                # Use fallback data
                symbol = index_data['symbol']
                fallback = fallback_data.get(symbol, {'value': 1000.0, 'change': 0.0})
                
                index_info = IndexInfo(
                    name=index_data['name'],
                    symbol=symbol,
                    current_value=fallback['value'],
                    change_percent=fallback['change'],
                    last_updated=datetime.now()
                )
                index_info_list.append(index_info)
                print(f"⚠️ Using fallback data for {index_data['name']}: {fallback['value']}")
        
        return index_info_list
    
    def get_exchange_locations(self, country: str) -> List[LocationInfo]:
        """Get geographical locations of stock exchanges"""
        country_key = country.lower()
        if country_key not in self.country_exchanges:
            return []
        
        locations = []
        for loc_data in self.country_exchanges[country_key]['locations']:
            location = LocationInfo(
                name=loc_data['name'],
                address=loc_data['address'],
                latitude=loc_data['latitude'],
                longitude=loc_data['longitude']
            )
            locations.append(location)
        
        return locations