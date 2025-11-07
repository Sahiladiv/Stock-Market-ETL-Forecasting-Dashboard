import streamlit as st
import pandas as pd
import mysql.connector
import plotly.graph_objects as go
from datetime import datetime
from utils.model_lstm import (
    prepare_lstm_data, train_lstm, predict_lstm,
    get_prediction_df, plot_predictions
)

# ------------------------------
# MySQL credentials
DB_CONFIG = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'trade_data'
}

# ------------------------------
@st.cache_data
def get_data(ticker: str, start_date: str, end_date: str):
    """Fetch stock data between date range"""
    conn = mysql.connector.connect(**DB_CONFIG)
    query = f"""
        SELECT * FROM stock_data
        WHERE ticker = '{ticker}'
        AND Date BETWEEN '{start_date}' AND '{end_date}'
        ORDER BY Date
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def plot_candlestick(df):
    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=df['Date'],
        open=df['Open'], high=df['High'],
        low=df['Low'], close=df['Close'],
        name='OHLC'
    ))

    fig.add_trace(go.Scatter(
        x=df['Date'], y=df['SMA_10'],
        line=dict(color='blue', width=1),
        name='SMA 10'
    ))

    fig.add_trace(go.Scatter(
        x=df['Date'], y=df['SMA_50'],
        line=dict(color='orange', width=1),
        name='SMA 50'
    ))

    fig.update_layout(title='Stock Price & Moving Averages',
                      xaxis_title='Date', yaxis_title='Price')
    return fig

def show_summary(df):
    st.subheader("Summary Statistics")
    st.write(df[['Close', 'SMA_10', 'SMA_50']].describe())

def show_signals(df):
    st.subheader("Bullish Crossover Signals (SMA 10 > SMA 50)")
    signals = df[df['SMA_10'] > df['SMA_50']]
    st.write(f"{len(signals)} signals found")
    st.dataframe(signals[['Date', 'Close', 'SMA_10', 'SMA_50']].tail(10))

# ------------------------------
# STREAMLIT UI
st.set_page_config(layout="wide", page_title="Stock ETL Dashboard")

st.title("Stock Trading ETL Dashboard")

# Select ticker
ticker = st.selectbox("Select Stock Ticker", ['AAPL', 'MSFT', 'GOOGL', 'TSLA'])

# Date range selector
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", datetime(2023, 1, 1))
with col2:
    end_date = st.date_input("End Date", datetime(2024, 1, 1))

# Fetch data
df = get_data(ticker, start_date, end_date)

if df.empty:
    st.warning("No data found for the selected range. Try different dates.")
else:
    st.plotly_chart(plot_candlestick(df), use_container_width=True)
    show_summary(df)
    show_signals(df)

    # ------------------------------
    # LSTM MODEL SECTION
    st.subheader("LSTM Prediction vs Actual Closing Price")

    # Training window slider
    window_size = st.slider(
        "Select Training Window (days)",
        min_value=30,
        max_value=120,
        value=60,
        step=10,
        help="Adjust the number of past days used for LSTM training."
    )

    try:
        # Prepare data for LSTM
        X, y, scaler = prepare_lstm_data(df, window_size=window_size)
        X_reshaped = X.reshape((X.shape[0], X.shape[1], 1))

        # Train model
        with st.spinner("Training LSTM model... this may take a few seconds ⏳"):
            model = train_lstm(X_reshaped, y)

        # Predict
        preds = predict_lstm(model, X_reshaped, scaler)

        # Combine predictions
        pred_df = get_prediction_df(df, preds, window_size)

        # Display results
        st.plotly_chart(plot_predictions(pred_df), use_container_width=True)

    except Exception as e:
        st.error(f"Error during LSTM prediction: {str(e)}")
