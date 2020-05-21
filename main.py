import datetime
import configparser
import alpha_vantage
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="darkgrid")

# configparser
config = configparser.ConfigParser()
config.read('alpha_vantage.cfg')
key = config['alpha_vantage']['key']

API_URL= "https://www.alphavantage.co/query"

stocks = ['MSFT']

# Get data for stocks.
for stock in stocks:
    data = {
        # timeseries function
        "function": "TIME_SERIES_DAILY",
        "symbol": stock,
        # outputsize - compact = latest 100, full = 20 yrs
        "outputsize": "compact",
        "datatype": "json",
        "apikey": key
    }
    response = requests.get(API_URL, data)
    data = response.json()
    # retreive ohlc values only
    daily_ts = data['Time Series (Daily)']
    # print(f"{stock}: {daily_ts}")

    # Create pandas DF with values
    df = pd.DataFrame.from_dict(daily_ts, orient="index")

# Time periods for RSI
time_periods = [50,200]

for period in time_periods:
    data = {
        "function": "RSI",
        "symbol": stock,
        "interval": "daily",
        "time_period": period,
        "series_type": "close",
        "datatype": "json",
        "apikey": key
    }
    response = requests.get(API_URL, data)
    data = response.json()
    rsi = data['Technical Analysis: RSI']
    df_rsi = pd.DataFrame.from_dict(rsi, orient="index")
    # df['rsi'] = df_rsi
    # print(f'rsi{period}: {df_rsi}')
    df[f'rsi_{period}'] = df_rsi
    # print(df)

# Check if df.types are float
# df.info()
# Convert df object into float
df = df.astype(float)
df.info()

# Plot chart of close prices and RSI
# df[['rsi_50', 'rsi_200']].plot()
sns.lineplot(data=df[['rsi_50', 'rsi_200']])
plt.show()
# Rsi bullish crossover
