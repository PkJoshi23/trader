import time
import pandas as pd
from alpaca_api import AlpacaAPI
from strategy import generate_signals
from risk import calculate_position_size, calculate_stop_loss, calculate_take_profit, check_max_positions, check_daily_loss
from config import MAX_STOCK_PRICE

def main():
    alpaca = AlpacaAPI()
    account = alpaca.get_account()
    start_equity = float(account.equity)

    while True:
        # Check daily loss cap
        account = alpaca.get_account()
        if not check_daily_loss(account, start_equity):
            print('Daily loss cap reached. Stopping trading for today.')
            break

        open_positions = alpaca.get_positions()
        if not check_max_positions(open_positions):
            print('Max concurrent positions reached. Waiting...')
            time.sleep(60)
            continue

        # Dynamically fetch penny stocks with liquidity filter
        penny_stocks = alpaca.get_penny_stocks(MAX_STOCK_PRICE, min_avg_volume=100000)
        print(f"Found {len(penny_stocks)} penny stocks to scan.")
        for symbol in penny_stocks:
            # Get latest 1-min data (last 50 bars)
            df = alpaca.get_historical_data(symbol, '1Min', limit=50)
            if df.empty or df['close'].iloc[-1] > MAX_STOCK_PRICE:
                continue

            signals = generate_signals(df)
            if signals is None:
                continue

            latest = signals.iloc[-1]
            if latest['entry_signal']:
                atr = latest['atr']
                price = latest['close']
                position_size = calculate_position_size(float(account.equity), atr, price)
                if position_size < 1:
                    continue
                stop_loss = calculate_stop_loss(price, atr)
                take_profit = calculate_take_profit(price, atr)
                print(f"Placing order: {symbol}, qty={position_size}, entry={price}, SL={stop_loss}, TP={take_profit}")
                alpaca.submit_order(
                    symbol=symbol,
                    qty=position_size,
                    side='buy',
                    type='market',
                    stop_loss=stop_loss,
                    take_profit=take_profit
                )
                time.sleep(2)  # Avoid API rate limits

        # Sleep before next scan
        time.sleep(60)

if __name__ == '__main__':
    main() 
