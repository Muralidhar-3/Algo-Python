import yfinance as yf
import time
from datetime import datetime, time as dt_time
import warnings

# Ignore FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Define the symbols of the NSE-listed stocks you want to track
stock_list = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS']

def check_day_range(stock_symbol):
    try:
        # Fetch historical stock data
        stock = yf.Ticker(stock_symbol)

        # Get historical data for the stock with 1-day interval
        data = stock.history(period="1d", interval="1m")

        # Define the time for 9:30 AM
        target_time = dt_time(9, 15)

        # Filter data after 9:30
        data_after_915 = data[data.index.time >= target_time]

        # Check if there is data available after 9:15
        if not data_after_915.empty:
            # Calculate the opening range (high and low) after 9:15
            day_range_high = data_after_915['High'].max()
            day_range_low = data_after_915['Low'].min()

            # Print the stock symbol and its opening range after 9:15
            # print(f"Stock: {stock_symbol}")
            print(f"{stock_symbol} Day Range High:", day_range_high)
            print(f"{stock_symbol} Day Range Low:", day_range_low)
        else:
            print(f"No data available for {stock_symbol} after 9:15 AM.")

    except Exception as e:
        print(f"Error fetching data for {stock_symbol}: {e}")

def main(stock_list):
    while True:
        for stock_symbol in stock_list:
            check_day_range(stock_symbol)
        time.sleep(300)  # Check every 5 minutes (adjust as needed)

if __name__ == "__main__":
    main(stock_list)
