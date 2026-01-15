import yfinance as yf
import pandas as pd
import sqlite3
from datetime import datetime

def fetch_data(ticker):
    data = yf.download(ticker, period="5d")
    return data

def validate_data(df):
    if df.isnull().sum().sum() > 0:
        raise ValueError("Data validation failed: Missing values detected")
    return True

def calculate_metrics(df):
    df["Returns"] = df["Close"].pct_change()
    pnl = df["Returns"].sum()
    return pnl

def store_report(ticker, pnl, date):
    conn = sqlite3.connect("daily_reports.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            ticker TEXT,
            date TEXT,
            pnl REAL
        )
    """)
    cursor.execute("INSERT INTO reports VALUES (?, ?, ?)", (ticker, date, pnl))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    ticker = "AAPL"
    today = datetime.now().strftime("%Y-%m-%d")

    data = fetch_data(ticker)
    validate_data(data)
    pnl = calculate_metrics(data)

    store_report(ticker, pnl, today)

    data.to_csv(f"daily_report_{ticker}_{today}.csv")
    print("Daily market report generated successfully")
