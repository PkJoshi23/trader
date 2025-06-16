from indicators import calculate_rsi, calculate_vwap, calculate_ema, calculate_atr, calculate_macd
import pandas as pd
from config import MAX_STOCK_PRICE, MIN_VOLUME_SPIKE


def detect_breakout(df, window=20):
    # Breakout above recent consolidation (highest close in window)
    df['recent_high'] = df['close'].rolling(window=window).max()
    df['breakout'] = (df['close'] > df['recent_high'].shift(1))
    return df['breakout']


def detect_volume_spike(df, window=20):
    avg_vol = df['volume'].rolling(window=window).mean()
    df['vol_spike'] = df['volume'] > (MIN_VOLUME_SPIKE * avg_vol)
    return df['vol_spike']


def detect_pullback(df, ema_period=9):
    # Pullback to EMA support
    ema = calculate_ema(df, period=ema_period)
    df['pullback'] = (df['low'] <= ema) & (df['close'] > ema)
    return df['pullback']


def generate_signals(df):
    # Filter penny stocks
    if df['close'].iloc[-1] > MAX_STOCK_PRICE:
        return None

    # Calculate indicators
    df['rsi'] = calculate_rsi(df)
    df['vwap'] = calculate_vwap(df)
    df['ema9'] = calculate_ema(df, 9)
    df['ema21'] = calculate_ema(df, 21)
    df['atr'] = calculate_atr(df)
    macd = calculate_macd(df)
    df = pd.concat([df, macd], axis=1)

    # Detect signals
    breakout = detect_breakout(df)
    vol_spike = detect_volume_spike(df)
    pullback = detect_pullback(df)

    # Entry: breakout + volume spike + pullback confirmation
    entry = breakout & vol_spike & pullback
    # Exit: RSI overbought/oversold, or price hits stop/take-profit (handled in risk)
    exit_signal = (df['rsi'] > 80) | (df['rsi'] < 20)

    df['entry_signal'] = entry
    df['exit_signal'] = exit_signal
    return df[['entry_signal', 'exit_signal', 'atr', 'close']] 