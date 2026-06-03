"""
trading_backtest.py — Backtest any strategy on historical data.
Tests win rate over a given period.
"""
import json, sys
from datetime import datetime, timedelta

# Import from our trading signals module
sys.path.insert(0, "/data/home/workspace/coachtoby-site/bot/services")
from trading_signals import (
    get_data_yfinance, signal_rsi, signal_macd, signal_sma_crossover,
    signal_bollinger, signal_volume_spike, signal_combined
)

def backtest_strategy(symbol, strategy_name, period="60d", interval="1d"):
    """
    Backtest a strategy: simulate trading on historical data.
    Returns win rate, total trades, profit/loss.
    """
    data = get_data_yfinance(symbol, period, interval)
    if not data:
        return {"error": "Could not fetch data"}
    
    close = data["close"]
    dates = data["dates"]
    
    # Get signals
    strategies = {
        "rsi": signal_rsi,
        "macd": signal_macd,
        "sma": signal_sma_crossover,
        "bollinger": signal_bollinger,
        "volume": signal_volume_spike,
        "combined": signal_combined,
    }
    
    if strategy_name not in strategies:
        return {"error": f"Unknown strategy: {strategy_name}"}
    
    result = strategies[strategy_name](data)
    signals = result.get("signals", [])
    
    if not signals:
        return {
            "symbol": symbol,
            "strategy": strategy_name,
            "period": period,
            "data_range": f"{dates[0]} to {dates[-1]}",
            "total_candles": len(close),
            "current_price": round(close[-1], 2),
            "total_trades": 0,
            "wins": 0,
            "losses": 0,
            "win_rate": 0,
            "total_pnl": 0,
            "avg_pnl_per_trade": 0,
            "trades": [],
            "note": "No signals generated in this period",
        }
    
    # Simulate trades
    trades = []
    position = None
    
    for sig in signals:
        if sig["signal"] == "BUY" and position is None:
            position = {"entry_price": sig["price"], "entry_date": sig["date"]}
        elif sig["signal"] == "SELL" and position is not None:
            pnl = sig["price"] - position["entry_price"]
            pnl_pct = (pnl / position["entry_price"]) * 100
            trades.append({
                "entry_date": position["entry_date"], "exit_date": sig["date"],
                "entry_price": round(position["entry_price"], 2),
                "exit_price": round(sig["price"], 2),
                "pnl": round(pnl, 2), "pnl_pct": round(pnl_pct, 2),
                "result": "WIN" if pnl > 0 else "LOSS",
            })
            position = None
    
    # If still holding
    if position is not None:
        pnl = close[-1] - position["entry_price"]
        pnl_pct = (pnl / position["entry_price"]) * 100
        trades.append({
            "entry_date": position["entry_date"], "exit_date": dates[-1] + " (open)",
            "entry_price": round(position["entry_price"], 2),
            "exit_price": round(close[-1], 2),
            "pnl": round(pnl, 2), "pnl_pct": round(pnl_pct, 2),
            "result": "WIN" if pnl > 0 else "LOSS", "status": "OPEN",
        })
    
    # Calculate stats
    total_trades = len(trades)
    wins = len([t for t in trades if t["result"] == "WIN"])
    losses = len([t for t in trades if t["result"] == "LOSS"])
    win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
    total_pnl = sum(t["pnl"] for t in trades)
    avg_pnl = total_pnl / total_trades if total_trades > 0 else 0
    
    return {
        "symbol": symbol,
        "strategy": strategy_name,
        "period": period,
        "data_range": f"{dates[0]} to {dates[-1]}",
        "total_candles": len(close),
        "current_price": round(close[-1], 2),
        "total_trades": total_trades,
        "wins": wins,
        "losses": losses,
        "win_rate": round(win_rate, 1),
        "total_pnl": round(total_pnl, 2),
        "avg_pnl_per_trade": round(avg_pnl, 2),
        "trades": trades,
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Backtest trading strategies")
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--strategy", default="combined", choices=["rsi","macd","sma","bollinger","volume","combined"])
    parser.add_argument("--period", default="60d")
    parser.add_argument("--interval", default="1d")
    args = parser.parse_args()
    
    print(f"\n{'='*60}")
    print(f"  BACKTEST: {args.symbol} | {args.strategy.upper()}")
    print(f"  Period: {args.period}")
    print(f"{'='*60}\n")
    
    result = backtest_strategy(args.symbol, args.strategy, args.period, args.interval)
    
    if "error" in result:
        print(f"ERROR: {result['error']}")
        return
    
    print(f"Symbol: {result['symbol']}")
    print(f"Strategy: {result['strategy']}")
    print(f"Data: {result['data_range']} ({result['total_candles']} candles)")
    if "current_price" in result:
        print(f"Current price: {result['current_price']}")
    print(f"\n── RESULTS ──")
    print(f"Total trades: {result['total_trades']}")
    print(f"Wins: {result['wins']} | Losses: {result['losses']}")
    print(f"Win rate: {result['win_rate']}%")
    print(f"Total P&L: {result['total_pnl']}")
    print(f"Avg P&L per trade: {result['avg_pnl_per_trade']}")
    
    if result.get("trades"):
        print(f"\n── TRADES ──")
        for i, t in enumerate(result["trades"], 1):
            status = t.get("status", "CLOSED")
            print(f"  {i}. {t['entry_date']} → {t['exit_date']}")
            print(f"     Entry: {t['entry_price']} | Exit: {t['exit_price']}")
            print(f"     P&L: {t['pnl']} ({t['pnl_pct']}%) | {t['result']} [{status}]")
    
    print(f"\n{'='*60}\n")


if __name__ == "__main__":
    main()
