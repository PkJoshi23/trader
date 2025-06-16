import os
from dotenv import load_dotenv

load_dotenv()

# Alpaca API credentials
ALPACA_API_KEY = os.getenv('APCA_API_KEY_ID') or os.getenv('ALPACA_API_KEY')
ALPACA_SECRET_KEY = os.getenv('APCA_API_SECRET_KEY') or os.getenv('ALPACA_SECRET_KEY')
ALPACA_BASE_URL = os.getenv('APCA_API_BASE_URL', 'https://paper-api.alpaca.markets')
# Trading parameters
MAX_RISK_PER_TRADE = 0.20  # 1% of total capital
STOP_LOSS_ATR_MULTIPLIER = 1.5
TAKE_PROFIT_ATR_MULTIPLIER = 2.5
MAX_CONCURRENT_POSITIONS = 3
DAILY_MAX_LOSS_CAP = 0.20  # 5% of account balance

# Timeframes
TIMEFRAMES = ['1Min', '5Min']

# Penny stock filter
MAX_STOCK_PRICE = 50.0  # Only trade stocks below $5
MIN_VOLUME_SPIKE = 0.8  # 2x average volume spike


