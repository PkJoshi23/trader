import pandas as pd
import ta

def calculate_rsi(df, period=14):
    return ta.momentum.RSIIndicator(close=df['close'], window=period).rsi()

def calculate_vwap(df):
    return ta.volume.VolumeWeightedAveragePrice(
        high=df['high'], low=df['low'], close=df['close'], volume=df['volume']
    ).vwap()

def calculate_ema(df, period=9):
    return ta.trend.EMAIndicator(close=df['close'], window=period).ema_indicator()

def calculate_atr(df, period=14):
    return ta.volatility.AverageTrueRange(
        high=df['high'], low=df['low'], close=df['close'], window=period
    ).average_true_range()

def calculate_macd(df):
    macd = ta.trend.MACD(close=df['close'])
    return pd.DataFrame({
        'macd': macd.macd(),
        'macd_signal': macd.macd_signal(),
        'macd_diff': macd.macd_diff()
    }) 