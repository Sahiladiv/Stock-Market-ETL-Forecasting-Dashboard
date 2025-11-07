# etl_runner.py
import streamlit as st
from datetime import datetime
from prefect import flow
from stock_etl.pipeline import extract, transform, analyze, load

# -----------------------------
# Database Config (match pipeline.py)
DB_CONFIG = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'trade_data'
}

# -----------------------------
@flow(name="Manual ETL Pipeline")
def etl_flow(symbol: str, start_date: str, end_date: str):
    raw = extract(symbol, start_date, end_date)
    clean = transform(raw)
    analyze(clean)
    load(clean, DB_CONFIG)

# -----------------------------
# Streamlit UI
st.set_page_config(page_title="ETL Runner", layout="centered")
st.title("⚙️ Run ETL Pipeline Manually")

# Inputs
stock = st.selectbox("Select Stock Ticker", ['AAPL', 'MSFT', 'GOOGL', 'TSLA'])
col1, col2 = st.columns(2)
with col1:
    start = st.date_input("Start Date", datetime(2023, 1, 1))
with col2:
    end = st.date_input("End Date", datetime(2023, 12, 31))

# Trigger button
if st.button("🚀 Run ETL Pipeline"):
    with st.spinner("Running ETL pipeline..."):
        try:
            etl_flow(symbol=stock, start_date=start.strftime("%Y-%m-%d"), end_date=end.strftime("%Y-%m-%d"))
            st.success("✅ ETL pipeline completed successfully!")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
