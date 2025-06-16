from config import MAX_RISK_PER_TRADE, STOP_LOSS_ATR_MULTIPLIER, TAKE_PROFIT_ATR_MULTIPLIER, MAX_CONCURRENT_POSITIONS, DAILY_MAX_LOSS_CAP


def calculate_position_size(account_balance, atr, price):
    # Risk per trade in dollars
    risk_dollars = account_balance * MAX_RISK_PER_TRADE
    # Stop distance in dollars
    stop_distance = atr * STOP_LOSS_ATR_MULTIPLIER
    if stop_distance == 0:
        return 0
    # Position size (shares)
    position_size = risk_dollars // stop_distance
    # Ensure we don't buy more than we can afford
    max_affordable = account_balance // price
    return int(min(position_size, max_affordable))


def calculate_stop_loss(entry_price, atr):
    return round(entry_price - (atr * STOP_LOSS_ATR_MULTIPLIER), 2)


def calculate_take_profit(entry_price, atr):
    return round(entry_price + (atr * TAKE_PROFIT_ATR_MULTIPLIER), 2)


def check_max_positions(current_positions):
    return len(current_positions) < MAX_CONCURRENT_POSITIONS


def check_daily_loss(account, start_equity):
    # Enforce daily loss cap
    current_equity = float(account.equity)
    loss = (start_equity - current_equity) / start_equity
    return loss < DAILY_MAX_LOSS_CAP 