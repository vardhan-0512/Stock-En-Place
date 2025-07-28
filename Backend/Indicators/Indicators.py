import pandas as pd
import numpy as np
import yfinance as yf

def _get_data_column(data, column_name="close"):
    if isinstance(data, pd.DataFrame):
        return data.get(column_name, data['close'] if 'close' in data.columns else pd.Series(dtype=float))
    elif isinstance(data, pd.Series):
        return data
    else:
        raise TypeError("Input data must be a pandas DataFrame or Series.")

def moving_average(data: pd.DataFrame, period: int = 20, column: str = "close"):
    price_data = _get_data_column(data, column)
    return price_data.rolling(window=period).mean()

def exponential_moving_average(data: pd.DataFrame, period: int = 20, column: str = "close"):
    price_data = _get_data_column(data, column)
    return price_data.ewm(span=period, adjust=False).mean()

def supertrend(data: pd.DataFrame, atr_period: int = 10, multiplier: float = 3.0):
    high = data['high']
    low = data['low']
    close = data['close']
    
    atr = average_true_range(data, period=atr_period)
    
    basic_upper_band = (high + low) / 2 + multiplier * atr
    basic_lower_band = (high + low) / 2 - multiplier * atr
    
    final_upper_band = basic_upper_band.copy()
    final_lower_band = basic_lower_band.copy()
    
    for i in range(1, len(data)):
        if close.iloc[i-1] <= final_upper_band.iloc[i-1]:
            final_upper_band.iloc[i] = min(basic_upper_band.iloc[i], final_upper_band.iloc[i-1])
        if close.iloc[i-1] >= final_lower_band.iloc[i-1]:
            final_lower_band.iloc[i] = max(basic_lower_band.iloc[i], final_lower_band.iloc[i-1])

    supertrend = pd.Series(np.nan, index=data.index)
    if len(data) > 0:
        if close.iloc[0] > final_lower_band.iloc[0]:
             supertrend.iloc[0] = final_lower_band.iloc[0]
        else:
             supertrend.iloc[0] = final_upper_band.iloc[0]

    for i in range(1, len(data)):
        if supertrend.iloc[i-1] == final_upper_band.iloc[i-1] and close.iloc[i] <= final_upper_band.iloc[i]:
            supertrend.iloc[i] = final_upper_band.iloc[i]
        elif supertrend.iloc[i-1] == final_upper_band.iloc[i-1] and close.iloc[i] > final_upper_band.iloc[i]:
            supertrend.iloc[i] = final_lower_band.iloc[i]
        elif supertrend.iloc[i-1] == final_lower_band.iloc[i-1] and close.iloc[i] >= final_lower_band.iloc[i]:
            supertrend.iloc[i] = final_lower_band.iloc[i]
        elif supertrend.iloc[i-1] == final_lower_band.iloc[i-1] and close.iloc[i] < final_lower_band.iloc[i]:
            supertrend.iloc[i] = final_upper_band.iloc[i]
        
    return pd.DataFrame({'supertrend': supertrend, 'final_upper': final_upper_band, 'final_lower': final_lower_band})

def parabolic_sar(data: pd.DataFrame, initial_af: float = 0.02, max_af: float = 0.2, increment: float = 0.02):
    high, low = data['high'], data['low']
    psar = low.copy()
    bull = True
    af = initial_af
    ep = high[0]
    
    for i in range(2, len(data)):
        if bull:
            psar[i] = psar[i-1] + af * (ep - psar[i-1])
        else:
            psar[i] = psar[i-1] - af * (psar[i-1] - ep)
        
        reverse = False
        if bull:
            if low[i] < psar[i]:
                bull = False
                reverse = True
                psar[i] = ep
                ep = low[i]
                af = initial_af
        else:
            if high[i] > psar[i]:
                bull = True
                reverse = True
                psar[i] = ep
                ep = high[i]
                af = initial_af

        if not reverse:
            if bull:
                if high[i] > ep:
                    ep = high[i]
                    af = min(af + increment, max_af)
            else:
                if low[i] < ep:
                    ep = low[i]
                    af = min(af + increment, max_af)
    return psar

def ichimoku_cloud(data: pd.DataFrame, tenkan_period: int = 9, kijun_period: int = 26, senkou_b_period: int = 52, chikou_period: int = 26):
    high = data['high']
    low = data['low']
    
    tenkan_sen = (high.rolling(window=tenkan_period).max() + low.rolling(window=tenkan_period).min()) / 2
    kijun_sen = (high.rolling(window=kijun_period).max() + low.rolling(window=kijun_period).min()) / 2
    senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(kijun_period)
    senkou_span_b = ((high.rolling(window=senkou_b_period).max() + low.rolling(window=senkou_b_period).min()) / 2).shift(kijun_period)
    chikou_span = data['close'].shift(-chikou_period)
    
    return pd.DataFrame({
        'tenkan_sen': tenkan_sen,
        'kijun_sen': kijun_sen,
        'senkou_span_a': senkou_span_a,
        'senkou_span_b': senkou_span_b,
        'chikou_span': chikou_span
    })

def average_directional_index(data: pd.DataFrame, period: int = 14):
    high = data['high']
    low = data['low']
    close = data['close']
    
    tr = average_true_range(data, period=period, return_tr=True)
    
    up_move = high.diff()
    down_move = -low.diff()
    
    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0)
    
    plus_di = 100 * (pd.Series(plus_dm).ewm(alpha=1/period).mean() / tr)
    minus_di = 100 * (pd.Series(minus_dm).ewm(alpha=1/period).mean() / tr)
    
    dx = 100 * (abs(plus_di - minus_di) / (plus_di + minus_di))
    adx = dx.ewm(alpha=1/period).mean()
    
    return pd.DataFrame({'adx': adx, 'plus_di': plus_di, 'minus_di': minus_di})
    
def aroon_oscillator(data: pd.DataFrame, period: int = 25):
    high = data['high']
    low = data['low']
    
    aroon_up = 100 * high.rolling(period + 1).apply(lambda x: x.argmax(), raw=True) / period
    aroon_down = 100 * low.rolling(period + 1).apply(lambda x: x.argmin(), raw=True) / period
    
    return aroon_up - aroon_down

def williams_alligator(data: pd.DataFrame, jaw_period: int = 13, teeth_period: int = 8, lips_period: int = 5):
    median_price = (data['high'] + data['low']) / 2
    
    jaw = median_price.rolling(window=jaw_period).mean().shift(8)
    teeth = median_price.rolling(window=teeth_period).mean().shift(5)
    lips = median_price.rolling(window=lips_period).mean().shift(3)
    
    return pd.DataFrame({'jaw': jaw, 'teeth': teeth, 'lips': lips})

def moving_average_convergence_divergence(data: pd.DataFrame, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9, column: str = "close"):
    price_data = _get_data_column(data, column)
    ema_fast = exponential_moving_average(price_data, period=fast_period)
    ema_slow = exponential_moving_average(price_data, period=slow_period)
    
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
    histogram = macd_line - signal_line
    
    return pd.DataFrame({'macd': macd_line, 'signal': signal_line, 'histogram': histogram})

def relative_strength_index(data: pd.DataFrame, period: int = 14, column: str = "close"):
    price_data = _get_data_column(data, column)
    delta = price_data.diff(1)
    
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
    avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

def stochastic_oscillator(data: pd.DataFrame, k_period: int = 14, d_period: int = 3):
    high = data['high']
    low = data['low']
    close = data['close']
    
    l14 = low.rolling(window=k_period).min()
    h14 = high.rolling(window=k_period).max()
    
    percent_k = 100 * ((close - l14) / (h14 - l14))
    percent_d = percent_k.rolling(window=d_period).mean()
    
    return pd.DataFrame({'%K': percent_k, '%D': percent_d})

def rate_of_change(data: pd.DataFrame, period: int = 10, column: str = "close"):
    price_data = _get_data_column(data, column)
    roc = ((price_data - price_data.shift(period)) / price_data.shift(period)) * 100
    return roc

def williams_r(data: pd.DataFrame, period: int = 14):
    high = data['high']
    low = data['low']
    close = data['close']
    
    highest_high = high.rolling(window=period).max()
    lowest_low = low.rolling(window=period).min()
    
    williams_r = -100 * ((highest_high - close) / (highest_high - lowest_low))
    return williams_r

def money_flow_index(data: pd.DataFrame, period: int = 14):
    typical_price = (data['high'] + data['low'] + data['close']) / 3
    raw_money_flow = typical_price * data['volume']
    
    price_diff = typical_price.diff(1)
    
    positive_flow = raw_money_flow.where(price_diff > 0, 0)
    negative_flow = raw_money_flow.where(price_diff < 0, 0)
    
    positive_mf = positive_flow.rolling(window=period).sum()
    negative_mf = negative_flow.rolling(window=period).sum()
    
    money_ratio = positive_mf / negative_mf
    mfi = 100 - (100 / (1 + money_ratio))
    
    return mfi

def commodity_channel_index(data: pd.DataFrame, period: int = 20):
    typical_price = (data['high'] + data['low'] + data['close']) / 3
    sma_tp = typical_price.rolling(window=period).mean()
    mean_dev = typical_price.rolling(window=period).apply(lambda x: np.mean(np.abs(x - x.mean())))
    
    cci = (typical_price - sma_tp) / (0.015 * mean_dev)
    return cci

def chande_momentum_oscillator(data: pd.DataFrame, period: int = 14, column: str = "close"):
    price_data = _get_data_column(data, column)
    diff = price_data.diff(1)
    
    up_sum = diff.where(diff > 0, 0).rolling(window=period).sum()
    down_sum = np.abs(diff.where(diff < 0, 0)).rolling(window=period).sum()
    
    cmo = 100 * (up_sum - down_sum) / (up_sum + down_sum)
    return cmo

def relative_vigor_index(data: pd.DataFrame, period: int = 14):
    numerator = (data['close'] - data['open']).rolling(window=period).sum()
    denominator = (data['high'] - data['low']).rolling(window=period).sum()
    
    rvi = numerator / denominator
    rvi_signal = rvi.rolling(window=4).mean()
    
    return pd.DataFrame({'rvi': rvi, 'rvi_signal': rvi_signal})

def on_balance_volume(data: pd.DataFrame):
    close = data['close']
    volume = data['volume']
    
    obv = (np.sign(close.diff()) * volume).fillna(0).cumsum()
    return obv

def volume_profile(data: pd.DataFrame, bins: int = 10):
    price_range = (data['close'].min(), data['close'].max())
    price_bins = np.linspace(price_range[0], price_range[1], bins)
    
    profile = data.groupby(pd.cut(data['close'], bins=price_bins))['volume'].sum()
    return profile

def chaikin_money_flow(data: pd.DataFrame, period: int = 20):
    mfv = ((data['close'] - data['low']) - (data['high'] - data['close'])) / (data['high'] - data['low'])
    mfv = mfv.fillna(0) * data['volume']
    
    cmf = mfv.rolling(window=period).sum() / data['volume'].rolling(window=period).sum()
    return cmf

def accumulation_distribution_line(data: pd.DataFrame):
    clv = ((data['close'] - data['low']) - (data['high'] - data['close'])) / (data['high'] - data['low'])
    clv = clv.fillna(0)
    ad_line = (clv * data['volume']).cumsum()
    return ad_line

def volume_weighted_average_price(data: pd.DataFrame):
    q = data['volume']
    p = (data['high'] + data['low'] + data['close']) / 3
    vwap = (p * q).cumsum() / q.cumsum()
    return vwap

def money_flow(data: pd.DataFrame, period: int = 14):
    typical_price = (data['high'] + data['low'] + data['close']) / 3
    return typical_price * data['volume']

def bollinger_bands(data: pd.DataFrame, period: int = 20, std_dev: int = 2, column: str = "close"):
    price_data = _get_data_column(data, column)
    middle_band = moving_average(price_data, period=period)
    std = price_data.rolling(window=period).std()
    
    upper_band = middle_band + (std * std_dev)
    lower_band = middle_band - (std * std_dev)
    
    return pd.DataFrame({'middle': middle_band, 'upper': upper_band, 'lower': lower_band})

def average_true_range(data: pd.DataFrame, period: int = 14, return_tr: bool = False):
    high = data['high']
    low = data['low']
    close = data['close']
    
    tr1 = abs(high - low)
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())
    
    true_range = pd.DataFrame({'tr1': tr1, 'tr2': tr2, 'tr3': tr3}).max(axis=1)
    if return_tr:
        return true_range
        
    atr = true_range.ewm(span=period, adjust=False).mean()
    return atr

def keltner_channel(data: pd.DataFrame, period: int = 20, atr_period: int = 10, multiplier: int = 2):
    ema = exponential_moving_average(data, period=period)
    atr = average_true_range(data, period=atr_period)
    
    upper_channel = ema + (atr * multiplier)
    lower_channel = ema - (atr * multiplier)
    
    return pd.DataFrame({'middle': ema, 'upper': upper_channel, 'lower': lower_channel})

def donchian_channel(data: pd.DataFrame, period: int = 20):
    upper_channel = data['high'].rolling(window=period).max()
    lower_channel = data['low'].rolling(window=period).min()
    middle_channel = (upper_channel + lower_channel) / 2
    
    return pd.DataFrame({'upper': upper_channel, 'lower': lower_channel, 'middle': middle_channel})

def standard_deviation(data: pd.DataFrame, period: int = 20, column: str = "close"):
    price_data = _get_data_column(data, column)
    return price_data.rolling(window=period).std()

def pivot_points(data: pd.DataFrame):
    high = data['high'].iloc[-1]
    low = data['low'].iloc[-1]
    close = data['close'].iloc[-1]
    
    pivot = (high + low + close) / 3
    
    s1 = (pivot * 2) - high
    r1 = (pivot * 2) - low
    s2 = pivot - (high - low)
    r2 = pivot + (high - low)
    s3 = low - 2 * (high - pivot)
    r3 = high + 2 * (pivot - low)
    
    return {'R3': r3, 'R2': r2, 'R1': r1, 'Pivot': pivot, 'S1': s1, 'S2': s2, 'S3': s3}

def fibonacci_retracement(data: pd.DataFrame):
    max_price = data['high'].max()
    min_price = data['low'].min()
    diff = max_price - min_price
    
    return {
        'level_0.0': max_price,
        'level_23.6': max_price - 0.236 * diff,
        'level_38.2': max_price - 0.382 * diff,
        'level_50.0': max_price - 0.5 * diff,
        'level_61.8': max_price - 0.618 * diff,
        'level_100.0': min_price
    }

def price_action(data: pd.DataFrame):
    o = data['open']
    h = data['high']
    l = data['low']
    c = data['close']
    
    patterns = pd.Series("", index=data.index)
    
    patterns[(c.shift(1) < o.shift(1)) & (c > o) & (o < c.shift(1)) & (c > o.shift(1))] = "Bullish Engulfing"
    patterns[(c.shift(1) > o.shift(1)) & (c < o) & (o > c.shift(1)) & (c < o.shift(1))] = "Bearish Engulfing"
    patterns[abs(c - o) < ((h - l) * 0.1)] = "Doji"
    
    return patterns