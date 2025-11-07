# model_lstm.py

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import plotly.graph_objects as go

# ---------------------
# Data Preparation
# ---------------------
def prepare_lstm_data(df: pd.DataFrame, window_size=60):
    df = df[['Close']].copy()
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(df)

    X, y = [], []
    for i in range(window_size, len(scaled)):
        X.append(scaled[i-window_size:i])
        y.append(scaled[i])
    
    X = np.array(X)
    y = np.array(y)
    return X, y, scaler

# ---------------------
# LSTM Model Training
# ---------------------
def train_lstm(X, y):
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(X.shape[1], 1)))
    model.add(LSTM(units=50))
    model.add(Dense(1))

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X, y, epochs=10, batch_size=32, verbose=0)
    return model

# ---------------------
# Prediction
# ---------------------
def predict_lstm(model, X, scaler):
    predictions = model.predict(X)
    return scaler.inverse_transform(predictions)

# ---------------------
# Combine prediction with actual data
# ---------------------
def get_prediction_df(df: pd.DataFrame, predictions: np.ndarray, window_size=60) -> pd.DataFrame:
    df = df.copy().reset_index(drop=True)
    result_df = df[window_size:].copy()
    result_df["Predicted_Close"] = predictions
    return result_df

# ---------------------
# Plotting Function (for Streamlit)
# ---------------------
def plot_predictions(result_df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=result_df["Date"], y=result_df["Close"], name="Actual Close"))
    fig.add_trace(go.Scatter(x=result_df["Date"], y=result_df["Predicted_Close"], name="Predicted Close"))
    fig.update_layout(
        title="LSTM: Predicted vs Actual Closing Price",
        xaxis_title="Date",
        yaxis_title="Stock Price"
    )
    return fig
