from flask import Flask, render_template
import cryptocompare
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from io import BytesIO
import base64
plt.style.use('classic')

cryptocompare_API_key = '51bc0afe84340b0011ce93eaba365a8d0a5834a6efe084634bf13d4ed92cca0e'
cryptocompare.cryptocompare._set_api_key_parameter('51bc0afe84340b0011ce93eaba365a8d0a5834a6efe084634bf13d4ed92cca0e')
print("API Key set!")


raw_ticker_data = cryptocompare.get_coin_list()
all_tickers = pd.DataFrame.from_dict(raw_ticker_data).T
print(all_tickers.iloc[:, :5].tail())

app = Flask(__name__)

def timestamp_to_string(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

app.jinja_env.filters['timestamp_to_string'] = timestamp_to_string

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/price")
def price():

    ticker_symbol= 'BTC'
    currency = 'EUR'
    limit_value = 100
    exchange_name = 'CCCAGG'
    data_before_timestamp = 1706655600

    day_prices = cryptocompare.get_historical_price_day(ticker_symbol, currency, limit_value, exchange_name, data_before_timestamp)
    print("Historical Prices (Days):")
    print(day_prices)

    return render_template("price.html", day_prices=day_prices)

@app.route("/graph")
def graph():

    ticker_symbol = 'BTC'
    currency = 'EUR'
    limit_value = 10
    exchange_name = 'CCCAGG'
    data_before_timestamp = 1706655600

    hourly_price_data = cryptocompare.get_historical_price_hour(ticker_symbol, currency, limit_value, exchange_name, data_before_timestamp)

    df = pd.DataFrame(hourly_price_data)
    df['time'] = pd.to_datetime(df['time'], unit='s')

    plt.figure(figsize=(15,7))
    plt.plot(df['time'], df['close'])

    plt.title('BTC Close Price', fontsize=16)
    plt.xlabel('Date', fontsize=15)
    plt.ylabel('Price (€)', fontsize=15)
    plt.tick_params(axis='both', labelsize=15)

    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()

    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')
    plot_data_uri = 'data:image/png;base64,' + image_base64

    return render_template("graph.html", plot_data_uri=plot_data_uri)

if __name__ == "__main__":
    app.run(debug=True)

