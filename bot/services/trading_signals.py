"""
trading_signals.py — Free trading signal generator.
Supports multiple strategies. Uses free APIs only.

Strategies available:
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- SMA Crossover (Simple Moving Average)
- Bollinger Bands
- Volume Spike
- Combined (multi-strategy consensus)

Free data sources:
- Alpha Vantage (free tier: 25 calls/day)
- Yahoo Finance (unlimited via yfinance)
- Finnhub (free tier: 60 calls/min)

Usage:
    python trading_signals.py --symbol AAPL --strategy rsi
    python trading_signals.py --symbol BTC-USD --strategy combined
    python trading_signals.py --symbol EURUSD --strategy macd --interval 1h
"""
import argparse
import json
import sys
from datetime import datetime, timedelta

# ── FREE DATA SOURCES ──

def get_data_yfinance(symbol, period="60d", interval="1d"):
    """Get OHLCV data using yfinance (free, unlimited)."""
    try:
        import yfinance as yf
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period, interval=interval)
        if df.empty:
            return None
        return {
            "symbol": symbol,
            "dates": [d.strftime("%Y-%m-%d") for d in df.index],
            "open": df["Open"].tolist(),
            "high": df["High"].tolist(),
            "low": df["Low"].tolist(),
            "close": df["Close"].tolist(),
            "volume": df["Volume"].tolist(),
        }
    except ImportError:
        print("Install yfinance: pip install yfinance")
        return None
    except Exception as e:
        print(f"yfinance error: {e}")
        return None


def get_data_alphavantage(symbol, api_key, function="TIME_SERIES_DAILY"):
    """Get data from Alpha Vantage (free tier: 25 calls/day)."""
    import requests
    url = "https://www.alphavantage.co/query"
    params = {"function": function, "symbol": symbol, "apikey": api_key, "outputsize": "compact"}
    r = requests.get(url, params=params, timeout=15)
    data = r.json()
    # Parse time series
    ts_key = [k for k in data.keys() if "Time Series" in k]
    if not ts_key:
        return None
    ts = data[ts_key[0]]
    dates = sorted(ts.keys())
    return {
        "symbol": symbol,
        "dates": dates,
        "open": [float(ts[d]["1. open"]) for d in dates],
        "high": [float(ts[d]["2. high"]) for d in dates],
        "low": [float(ts[d]["3. low"]) for d in dates],
        "close": [float(ts[d]["4. close"]) for d in dates],
        "volume": [float(ts[d]["5. volume"]) for d in dates],
    }


def get_data_finnhub(symbol, api_key):
    """Get data from Finnhub (free tier: 60 calls/min)."""
    import requests
    end = int(datetime.now().timestamp())
    start = end - (60 * 86400)  # 60 days
    url = f"https://finnhub.io/api/v1/quote"
    # For candles:
    url = f"https://finnhub.io/api/v1/stock/candle"
    params = {"symbol": symbol, "resolution": "D", "from": start, "to": end, "token": api_key}
    r = requests.get(url, params=params, timeout=15)
    data = r.json()
    if data.get("s") != "ok":
        return None
    dates = [datetime.utcfromtimestamp(t).strftime("%Y-%m-%d") for t in data["t"]]
    return {
        "symbol": symbol,
        "dates": dates,
        "open": data["o"],
        "high": data["h"],
        "low": data["l"],
        "close": data["c"],
        "volume": data["v"],
    }


# ── TECHNICAL INDICATORS (pure Python, no TA-Lib needed) ──

def sma(data, period):
    """Simple Moving Average."""
    result = []
    for i in range(len(data)):
        if i < period - 1:
            result.append(None)
        else:
            result.append(sum(data[i - period + 1:i + 1]) / period)
    return result


def ema(data, period):
    """Exponential Moving Average."""
    result = [None] * len(data)
    if len(data) < period:
        return result
    # First EMA = SMA
    result[period - 1] = sum(data[:period]) / period
    multiplier = 2 / (period + 1)
    for i in range(period, len(data)):
        result[i] = (data[i] - result[i - 1]) * multiplier + result[i - 1]
    return result


def rsi(close, period=14):
    """Relative Strength Index."""
    if len(close) < period + 1:
        return [None] * len(close)
    
    gains = []
    losses = []
    for i in range(1, len(close)):
        change = close[i] - close[i - 1]
        gains.append(max(0, change))
        losses.append(max(0, -change))
    
    rsi_values = [None] * (period)
    if len(gains) < period:
        return [None] * len(close)
    
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    
    if avg_loss == 0:
        rsi_values.append(100)
    else:
        rs = avg_gain / avg_loss
        rsi_values.append(100 - (100 / (1 + rs)))
    
    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        if avg_loss == 0:
            rsi_values.append(100)
        else:
            rs = avg_gain / avg_loss
            rsi_values.append(100 - (100 / (1 + rs)))
    
    return rsi_values


def macd(close, fast=12, slow=26, signal=9):
    """MACD — returns (macd_line, signal_line, histogram)."""
    ema_fast = ema(close, fast)
    ema_slow = ema(close, slow)
    macd_line = [None] * len(close)
    for i in range(len(close)):
        if ema_fast[i] is not None and ema_slow[i] is not None:
            macd_line[i] = ema_fast[i] - ema_slow[i]
    
    # Signal line = EMA of MACD
    valid_macd = [v for v in macd_line if v is not None]
    signal_ema = ema(valid_macd, signal)
    
    signal_line = [None] * len(close)
    j = 0
    for i in range(len(close)):
        if macd_line[i] is not None:
            if j < len(signal_ema):
                signal_line[i] = signal_ema[j]
            j += 1
    
    histogram = [None] * len(close)
    for i in range(len(close)):
        if macd_line[i] is not None and signal_line[i] is not None:
            histogram[i] = macd_line[i] - signal_line[i]
    
    return macd_line, signal_line, histogram


def bollinger_bands(close, period=20, std_dev=2):
    """Bollinger Bands — returns (upper, middle, lower)."""
    middle = sma(close, period)
    upper = [None] * len(close)
    lower = [None] * len(close)
    
    for i in range(len(close)):
        if middle[i] is None:
            continue
        window = close[i - period + 1:i + 1]
        mean = sum(window) / len(window)
        variance = sum((x - mean) ** 2 for x in window) / len(window)
        std = variance ** 0.5
        upper[i] = mean + (std_dev * std)
        lower[i] = mean - (std_dev * std)
    
    return upper, middle, lower


# ── SIGNAL GENERATORS ──

def signal_rsi(data, period=14):
    """RSI signal: < 30 = oversold (BUY), > 70 = overbought (SELL)."""
    close = data["close"]
    rsi_values = rsi(close, period)
    
    signals = []
    for i in range(1, len(rsi_values)):
        if rsi_values[i] is None or rsi_values[i - 1] is None:
            continue
        if rsi_values[i - 1] < 30 and rsi_values[i] >= 30:
            signals.append({"date": data["dates"][i], "signal": "BUY", "rsi": round(rsi_values[i], 2), "price": close[i]})
        elif rsi_values[i - 1] > 70 and rsi_values[i] <= 70:
            signals.append({"date": data["dates"][i], "signal": "SELL", "rsi": round(rsi_values[i], 2), "price": close[i]})
    
    current_rsi = rsi_values[-1] if rsi_values[-1] is not None else None
    return {
        "strategy": "RSI",
        "current_rsi": round(current_rsi, 2) if current_rsi else None,
        "signals": signals[-5:],  # Last 5 signals
        "recommendation": "BUY" if current_rsi and current_rsi < 30 else "SELL" if current_rsi and current_rsi > 70 else "HOLD",
    }


def signal_macd(data, fast=12, slow=26, signal_period=9):
    """MACD signal: MACD crosses above signal = BUY, below = SELL."""
    close = data["close"]
    macd_line, signal_line, histogram = macd(close, fast, slow, signal_period)
    
    signals = []
    for i in range(1, len(macd_line)):
        if macd_line[i] is None or signal_line[i] or macd_line[i - 1] is None or signal_line[i - 1] is None:
            continue
        # Bullish crossover
        if macd_line[i - 1] < signal_line[i - 1] and macd_line[i] >= signal_line[i]:
            signals.append({"date": data["dates"][i], "signal": "BUY", "macd": round(macd_line[i], 4), "price": close[i]})
        # Bearish crossover
        elif macd_line[i - 1] > signal_line[i - 1] and macd_line[i] <= signal_line[i]:
            signals.append({"date": data["dates"][i], "signal": "SELL", "macd": round(macd_line[i], 4), "price": close[i]})
    
    current_macd = macd_line[-1] if macd_line[-1] is not None else None
    current_signal = signal_line[-1] if signal_line[-1] is not None else None
    return {
        "strategy": "MACD",
        "current_macd": round(current_macd, 4) if current_macd else None,
        "current_signal": round(current_signal, 4) if current_signal else None,
        "signals": signals[-5:],
        "recommendation": "BUY" if current_macd and current_signal and current_macd > current_signal else "SELL" if current_macd and current_signal and current_macd < current_signal else "HOLD",
    }


def signal_sma_crossover(data, short_period=20, long_period=50):
    """SMA Crossover: short SMA crosses above long SMA = BUY."""
    close = data["close"]
    sma_short = sma(close, short_period)
    sma_long = sma(close, long_period)
    
    signals = []
    for i in range(1, len(sma_short)):
        if sma_short[i] is None or sma_long[i] is None or sma_short[i - 1] is None or sma_long[i - 1] is None:
            continue
        if sma_short[i - 1] < sma_long[i - 1] and sma_short[i] >= sma_long[i]:
            signals.append({"date": data["dates"][i], "signal": "BUY", "sma_short": round(sma_short[i], 2), "sma_long": round(sma_long[i], 2), "price": close[i]})
        elif sma_short[i - 1] > sma_long[i - 1] and sma_short[i] <= sma_long[i]:
            signals.append({"date": data["dates"][i], "signal": "SELL", "sma_short": round(sma_short[i], 2), "sma_long": round(sma_long[i], 2), "price": close[i]})
    
    current_short = sma_short[-1] if sma_short[-1] is not None else None
    current_long = sma_long[-1] if sma_long[-1] is not None else None
    return {
        "strategy": "SMA Crossover",
        "current_sma_short": round(current_short, 2) if current_short else None,
        "current_sma_long": round(current_long, 2) if current_long else None,
        "signals": signals[-5:],
        "recommendation": "BUY" if current_short and current_long and current_short > current_long else "SELL" if current_short and current_long and current_short < current_long else "HOLD",
    }


def signal_bollinger(data, period=20, std_dev=2):
    """Bollinger Bands: price touches lower band = BUY, upper band = SELL."""
    close = data["close"]
    upper, middle, lower = bollinger_bands(close, period, std_dev)
    
    signals = []
    for i in range(len(close)):
        if upper[i] is None:
            continue
        if close[i] <= lower[i]:
            signals.append({"date": data["dates"][i], "signal": "BUY", "price": close[i], "lower_band": round(lower[i], 2)})
        elif close[i] >= upper[i]:
            signals.append({"date": data["dates"][i], "signal": "SELL", "price": close[i], "upper_band": round(upper[i], 2)})
    
    current_upper = upper[-1] if upper[-1] is not None else None
    current_lower = lower[-1] if lower[-1] is not None else None
    current_price = close[-1]
    return {
        "strategy": "Bollinger Bands",
        "current_upper": round(current_upper, 2) if current_upper else None,
        "current_lower": round(current_lower, 2) if current_lower else None,
        "current_price": round(current_price, 2),
        "signals": signals[-5:],
        "recommendation": "BUY" if current_lower and current_price <= current_lower else "SELL" if current_upper and current_price >= current_upper else "HOLD",
    }


def signal_volume_spike(data, period=20, multiplier=2):
    """Volume Spike: volume > 2x average = potential breakout."""
    volume = data["volume"]
    avg_volume = sma(volume, period)
    
    signals = []
    for i in range(len(volume)):
        if avg_volume[i] is None:
            continue
        if volume[i] > avg_volume[i] * multiplier:
            signals.append({
                "date": data["dates"][i],
                "signal": "VOLUME_SPIKE",
                "volume": int(volume[i]),
                "avg_volume": int(avg_volume[i]),
                "price": data["close"][i],
            })
    
    current_vol = volume[-1]
    current_avg = avg_volume[-1] if avg_volume[-1] else None
    return {
        "strategy": "Volume Spike",
        "current_volume": int(current_vol),
        "avg_volume": int(current_avg) if current_avg else None,
        "spike_detected": current_avg and current_vol > current_avg * multiplier,
        "signals": signals[-5:],
        "recommendation": "WATCH" if current_avg and current_vol > current_avg * multiplier else "NORMAL",
    }


def signal_combined(data):
    """Run all strategies and return consensus."""
    results = {
        "rsi": signal_rsi(data),
        "macd": signal_macd(data),
        "sma": signal_sma_crossover(data),
        "bollinger": signal_bollinger(data),
        "volume": signal_volume_spike(data),
    }
    
    buy_count = sum(1 for r in results.values() if r.get("recommendation") == "BUY")
    sell_count = sum(1 for r in results.values() if r.get("recommendation") == "SELL")
    hold_count = sum(1 for r in results.values() if r.get("recommendation") in ("HOLD", "NORMAL", "WATCH"))
    
    if buy_count > sell_count and buy_count >= 2:
        consensus = "BUY"
    elif sell_count > buy_count and sell_count >= 2:
        consensus = "SELL"
    else:
        consensus = "HOLD"
    
    return {
        "strategy": "Combined (Consensus)",
        "consensus": consensus,
        "buy_signals": buy_count,
        "sell_signals": sell_count,
        "hold_signals": hold_count,
        "details": results,
    }


# ── MAIN ──

def main():
    parser = argparse.ArgumentParser(description="Free Trading Signal Generator")
    parser.add_argument("--symbol", required=True, help="Trading symbol (e.g., AAPL, BTC-USD, EURUSD)")
    parser.add_argument("--strategy", default="combined", choices=["rsi", "macd", "sma", "bollinger", "volume", "combined"], help="Strategy to use")
    parser.add_argument("--period", default="60d", help="Data period (e.g., 30d, 60d, 1y)")
    parser.add_argument("--interval", default="1d", help="Candle interval (1d, 1h, 5m)")
    parser.add_argument("--api", default="yfinance", choices=["yfinance", "alphavantage", "finnhub"], help="Data source")
    parser.add_argument("--apikey", default="", help="API key (for Alpha Vantage or Finnhub)")
    args = parser.parse_args()
    
    print(f"\n{'='*60}")
    print(f"  TRADING SIGNAL: {args.symbol}")
    print(f"  Strategy: {args.strategy.upper()}")
    print(f"  Data Source: {args.api}")
    print(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"{'='*60}\n")
    
    # Get data
    if args.api == "yfinance":
        data = get_data_yfinance(args.symbol, args.period, args.interval)
    elif args.api == "alphavantage":
        data = get_data_alphavantage(args.symbol, args.apikey)
    elif args.api == "finnhub":
        data = get_data_finnhub(args.symbol, args.apikey)
    else:
        data = get_data_yfinance(args.symbol, args.period, args.interval)
    
    if not data:
        print("ERROR: Could not fetch data. Check symbol and API key.")
        sys.exit(1)
    
    print(f"Data: {len(data['dates'])} candles from {data['dates'][0]} to {data['dates'][-1]}")
    print(f"Current price: {data['close'][-1]:.2f}\n")
    
    # Run strategy
    strategies = {
        "rsi": signal_rsi,
        "macd": signal_macd,
        "sma": signal_sma_crossover,
        "bollinger": signal_bollinger,
        "volume": signal_volume_spike,
        "combined": signal_combined,
    }
    
    result = strategies[args.strategy](data)
    
    # Print results
    print(f"── {result['strategy']} ──")
    print(f"Recommendation: {result['recommendation']}")
    
    if args.strategy == "combined":
        print(f"Consensus: {result['buy_signals']} BUY / {result['sell_signals']} SELL / {result['hold_signals']} HOLD")
        print("\nIndividual strategies:")
        for name, detail in result["details"].items():
            print(f"  {name.upper()}: {detail['recommendation']}")
    
    if result.get("signals"):
        print(f"\nRecent signals:")
        for sig in result["signals"]:
            print(f"  {sig['date']} | {sig['signal']} | Price: {sig.get('price', 'N/A')}")
    
    print(f"\n{'='*60}\n")


if __name__ == "__main__":
    main()
