import alpaca_trade_api as tradeapi
import pandas as pd
from config import ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_BASE_URL

class AlpacaAPI:
    def __init__(self):
        self.api = tradeapi.REST(
            ALPACA_API_KEY,
            ALPACA_SECRET_KEY,
            ALPACA_BASE_URL,
            api_version='v2'
        )

    def get_account(self):
        return self.api.get_account()

    def get_positions(self):
        return self.api.list_positions()

    def get_historical_data(self, symbol, timeframe, limit=500, start=None, end=None):
        bars = self.api.get_bars(symbol, timeframe, limit=limit, start=start, end=end).df
        bars.index = pd.to_datetime(bars.index)
        return bars

    def submit_order(self, symbol, qty, side, type='market', time_in_force='day', stop_loss=None, take_profit=None):
        order = self.api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type=type,
            time_in_force=time_in_force,
            order_class='bracket' if stop_loss or take_profit else 'simple',
            stop_loss={'stop_price': stop_loss} if stop_loss else None,
            take_profit={'limit_price': take_profit} if take_profit else None
        )
        return order

    def cancel_all_orders(self):
        self.api.cancel_all_orders()

    def get_open_orders(self):
        return self.api.list_orders(status='open')

    def get_penny_stocks(self, max_price, min_avg_volume=500000):
        assets = self.api.list_assets(status='active', asset_class='us_equity')
        penny_stocks = []
        for asset in assets:
            if asset.tradable and asset.easy_to_borrow:
                try:
                    last_quote = self.api.get_latest_trade(asset.symbol)
                    price = last_quote.price
                    if price is not None and price <= max_price:
                        # Check average volume over last 10 days
                        bars = self.api.get_bars(asset.symbol, '1Day', limit=10).df
                        if not bars.empty and bars['volume'].mean() >= min_avg_volume:
                            penny_stocks.append(asset.symbol)
                except Exception:
                    continue
        return penny_stocks 