import os
from dotenv import load_dotenv

load_dotenv()

# Alpaca API credentials
ALPACA_API_KEY = os.getenv('ALPACA_API_KEY')
ALPACA_SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')
ALPACA_BASE_URL = os.getenv('ALPACA_BASE_URL', 'https://paper-api.alpaca.markets')

# Trading parameters
MAX_RISK_PER_TRADE = 0.01  # 1% of total capital
STOP_LOSS_ATR_MULTIPLIER = 1.5
TAKE_PROFIT_ATR_MULTIPLIER = 2.5
MAX_CONCURRENT_POSITIONS = 3
DAILY_MAX_LOSS_CAP = 0.05  # 5% of account balance

# Timeframes
TIMEFRAMES = ['1Min', '5Min']

# Penny stock filter
MAX_STOCK_PRICE = 5.0  # Only trade stocks below $5
MIN_VOLUME_SPIKE = 2.0  # 2x average volume spike

# Market session focus
PRE_MARKET_START = '04:00'
MARKET_OPEN = '09:30'
MARKET_CLOSE = '16:00'
EOD_REVERSAL_START = '15:00' 