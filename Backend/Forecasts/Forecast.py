import datetime
import math
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf
from prophet import Prophet
from pmdarima.arima import auto_arima
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from statsmodels.tsa.stattools import adfuller
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.models import Sequential

warnings.filterwarnings('ignore')

def get_stock_data(ticker, years=10):
    start_date = datetime.datetime.now() - datetime.timedelta(days=365.25 * years)
    end_date = datetime.date.today()
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        if data.empty:
            print(f"No data found for ticker {ticker}. Please check the symbol.")
            return None
        return data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

def arima_forecast(data, n_periods=30):
    print("Running Auto-ARIMA forecast...")
    train_data = data['Close']
    
    model = auto_arima(train_data, start_p=0, start_q=0,
                       test='adf',
                       max_p=3, max_q=3,
                       m=1,
                       d=None,
                       seasonal=False,
                       start_P=0, 
                       D=0, 
                       trace=True,
                       error_action='ignore',  
                       suppress_warnings=True, 
                       stepwise=True)

    print(model.summary())
    
    forecast, conf_int = model.predict(n_periods=n_periods, return_conf_int=True)
    print("ARIMA forecast complete.")
    return forecast, conf_int

def lstm_forecast(data, look_back=60, epochs=5):
    print("Running LSTM forecast...")
    close_data = data.filter(['Close']).values
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(close_data)

    train_data_len = math.ceil(len(close_data) * .8)
    train_data = scaled_data[0:train_data_len, :]

    x_train, y_train = [], []
    for i in range(look_back, len(train_data)):
        x_train.append(train_data[i-look_back:i, 0])
        y_train.append(train_data[i, 0])
    
    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)),
        LSTM(50, return_sequences=False),
        Dense(25),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x_train, y_train, batch_size=1, epochs=epochs)

    test_data = scaled_data[train_data_len - look_back:, :]
    x_test = []
    y_test = close_data[train_data_len:, :]
    for i in range(look_back, len(test_data)):
        x_test.append(test_data[i-look_back:i, 0])
        
    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)
    print("LSTM forecast complete.")
    return predictions

def prophet_forecast(data, n_years=1):
    print("Running Prophet forecast...")
    prophet_df = data.reset_index()[['Date', 'Close']].rename(columns={'Date': 'ds', 'Close': 'y'})
    
    model = Prophet(daily_seasonality=True)
    model.fit(prophet_df)
    
    future = model.make_future_dataframe(periods=365 * n_years)
    forecast = model.predict(future)
    
    print("Prophet forecast complete.")
    return forecast

def plot_forecast(data, forecast, ticker, model_name=""):
    plt.figure(figsize=(16, 8))
    plt.title(f'{ticker} Stock Price Forecast using {model_name}')
    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Close Price (USD)', fontsize=16)
    
    plt.plot(data.index, data['Close'], label='Historical Price')

    if isinstance(forecast, pd.DataFrame):
        if 'ds' in forecast.columns:
            plt.plot(forecast['ds'], forecast['yhat'], label='Forecast', color='orange')
            plt.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], color='k', alpha=.1, label='Confidence Interval')
        elif 'predicted_mean' in forecast.columns:
             plt.plot(forecast.index, forecast['predicted_mean'], label='Forecast', color='orange')
    else:
        forecast_index = data.index[len(data) - len(forecast):]
        plt.plot(forecast_index, forecast, label='Forecast', color='orange')

    plt.legend(loc='upper left')
    plt.grid(True)
    plt.show()

def generate_ten_year_forecast(ticker):
    print(f"Generating 10-year forecast for {ticker}...")
    data = get_stock_data(ticker, years=15)
    
    if data is None:
        return

    forecast = prophet_forecast(data, n_years=10)
    
    plot_forecast(data, forecast, ticker, model_name="Prophet")
    
    final_price = forecast['yhat'].iloc[-1]
    final_date = forecast['ds'].iloc[-1].strftime('%Y-%m-%d')
    print(f"\nPredicted closing price for {ticker} on {final_date}: ${final_price:,.2f}")


if __name__ == '__main__':
    stock_ticker = input("Enter a stock ticker to forecast (e.g., AAPL, GOOGL, MSFT): ").upper()
    generate_ten_year_forecast(stock_ticker)
