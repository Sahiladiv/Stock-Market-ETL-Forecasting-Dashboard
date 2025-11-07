# Stock Market ETL & Forecasting Dashboard

An end-to-end project for extracting, transforming, analyzing, and forecasting stock market data using:

- **ETL Pipelines** with `yfinance`, `Prefect`, and `MySQL`
- **Interactive Dashboards** using `Streamlit` and `Plotly`
- **Time Series Forecasting** with LSTM (TensorFlow/Keras)

---

## Project Overview

After spending time building Generative AI projects, I decided to explore the core data engineering and forecasting workflows — and this project brings it all together.

This app allows you to:
- Extract & store historical stock data
- Compute technical indicators (SMA10, SMA50)
- Detect bullish crossover signals
- Train an LSTM model to predict future closing prices
- Visualize everything in an interactive Streamlit UI

---

## Tech Stack

| Layer         | Toolset                          |
|---------------|----------------------------------|
| ETL           | yfinance · pandas · Prefect      |
| Storage       | MySQL                            |
| Modeling      | LSTM · TensorFlow · sklearn      |
| Dashboard     | Streamlit · Plotly               |
| Orchestration | Prefect 2.x                      |

---


---

## 🧪 Features

### ETL Flow (via Prefect or UI)
- Extracts historical stock data (Open, High, Low, Close, Volume)
- Computes SMA_10 and SMA_50 technical indicators
- Loads clean data into MySQL database

### Streamlit Dashboard
- Candlestick chart with SMA overlays
- Summary stats and bullish signal detection
- LSTM predicted vs actual closing prices
- Interactive controls for:
  - Ticker selection
  - Date range filter
  - LSTM training window (30–120 days)

### ETL Trigger UI (`etl_runner.py`)
- Manually run ETL from browser
- Select symbol and date range
- Watch live status messages

---



