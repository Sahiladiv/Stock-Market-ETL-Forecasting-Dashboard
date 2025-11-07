# prefect_flow.py
from prefect import flow, task
from stock_etl.pipeline import extract, transform, analyze, load

DB_CONFIG = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'trade_data'
}

@task
def extract_task(symbol, start, end):
    return extract(symbol, start, end)

@task
def transform_task(df):
    return transform(df)

@task
def analyze_task(df):
    analyze(df)

@task
def load_task(df, table_name='stock_data'):
    load(df, DB_CONFIG, table_name)

@flow(name="Stock ETL Pipeline")
def stock_etl_flow(symbol: str, start_date: str, end_date: str):
    df_raw = extract_task(symbol, start_date, end_date)
    df_clean = transform_task(df_raw)
    analyze_task(df_clean)
    load_task(df_clean)

# Run manually
if __name__ == "__main__":
    stock_etl_flow(symbol="VUG", start_date="2023-01-01", end_date="2024-03-01")
