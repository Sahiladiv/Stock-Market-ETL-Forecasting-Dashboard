# pipeline.py
import yfinance as yf
import pandas as pd
from datetime import datetime
import mysql.connector

def extract(stock_symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    df = yf.download(stock_symbol, start=start_date, end=end_date)
    df['ticker'] = stock_symbol
    df['data_scraped_on'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return df

def transform(df: pd.DataFrame) -> pd.DataFrame:
    df['SMA_10'] = df['Close'].rolling(window=10).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df.fillna(method='bfill', inplace=True)
    df = df[['Open', 'High', 'Low', 'Close', 'Volume', 'SMA_10', 'SMA_50', 'ticker', 'data_scraped_on']]
    df.reset_index(inplace=True)  
    return df

def analyze(df: pd.DataFrame):
    print("\n🔍 Summary Stats:")
    print(df[['Close', 'SMA_10', 'SMA_50']].describe())
    
    print("\n📈 Bullish Crossovers:")
    bullish = df[df['SMA_10'] > df['SMA_50']]
    print(f"{len(bullish)} signals detected")

def load(df: pd.DataFrame, db_config: dict, table_name='stock_data'):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            Date DATE,
            Open FLOAT,
            High FLOAT,
            Low FLOAT,
            Close FLOAT,
            Volume BIGINT,
            SMA_10 FLOAT,
            SMA_50 FLOAT,
            ticker VARCHAR(10),
            data_scraped_on DATETIME
        )
    ''')

    for _, row in df.iterrows():
        cursor.execute(f'''
            INSERT INTO {table_name} (
                Date, Open, High, Low, Close, Volume,
                SMA_10, SMA_50, ticker, data_scraped_on
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', tuple(row))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ {len(df)} rows inserted into `{table_name}`.")
