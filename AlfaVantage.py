import requests
import pandas as pd


# Replace with your Alpha Vantage API key
api_key = 'JQYSMHKOW5VA33TF'

def get_intraday_data(ticker_symbol, start_date, end_date, interval="5min"):
    base_url = "https://www.alphavantage.co/query"
    
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": ticker_symbol,
        "interval": interval,
        "apikey": api_key,
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if "Time Series (5min)" in data:
        intraday_data = pd.DataFrame(data["Time Series (5min)"]).T
        intraday_data.index = pd.to_datetime(intraday_data.index)
        return intraday_data[start_date:end_date]

    return None

if __name__ == "__main__":
    # Define the parameters
    ticker_symbol = "TCS.NS"
    start_date = "2023-09-01"
    end_date = "2023-09-29"

    # Get intraday data
    intraday_data = get_intraday_data(ticker_symbol, start_date, end_date)

    if intraday_data is not None:
        # Extract high and low prices
        high_low_prices = intraday_data[["2. high", "3. low"]]
        high_low_prices.columns = ["High", "Low"]

        # Print the results
        print("High and Low Prices between 9:15 AM and 10:15 AM:")
        print(high_low_prices)
    else:
        print("No data available for the specified date range.")
