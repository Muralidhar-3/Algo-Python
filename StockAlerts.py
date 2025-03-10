import yfinance as yf
import time 
from datetime import time as dt_time
from datetime import datetime, timedelta
import warnings
import requests
import json

# Ignore FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Define the Slack webhook URL
slack_webhook_url = 'https://hooks.slack.com/services/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'

def load_stock_data():
    try:
        with open('stock_data.json', 'r') as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        return {}

# You can call this function to load the data at the beginning of your script:
stock_data = load_stock_data()


# Define the send_slack_notification function
def send_slack_notification(message):
    try:
        payload = {
            'text': message,
        }

        response = requests.post(slack_webhook_url, json=payload)

        if response.status_code == 200:
            print('Notification sent successfully to Slack')
        else:
            print('Failed to send notification to Slack')
            print(response.text)

    except Exception as e:
        print(f"Error sending Slack notification: {e}")

# Define the symbols of the NSE-listed stocks you want to track
stock_list = ['CHAMBLFERT.NS', 'BAJFINANCE.NS', 'DELTACORP.NS', 'GRANULES.NS', 'BERGEPAINT.NS', 
              'TECHM.NS','DIXON.NS', 'LTIM.NS', 'MARUTI.NS', 'CANBK.NS', 'BAJAJ-AUTO.NS',
              'ASIANPAINT.NS', 'HDFCBANK.NS', 'BAJAJFINSV.NS', 'BHEL.NS', 'PNB.NS', 'IRCTC.NS', 
              'M&M.NS', 'POLYCAB.NS', 'INFY.NS', 'TCS.NS', 'ZEEL.NS', 'APOLLOHOSP.NS', 
              'AXISBANK.NS', 'RBLBANK.NS', 'RELIANCE.NS', 'WIPRO.NS', 'ONGC.NS', 'BANKBARODA.NS', 'SAIL.NS',
              'GLENMARK.NS', 'AMBUJACEM.NS', 'CHOLAFIN.NS', 'INDUSTOWER.NS', 'HAL.NS',

              'CANFINHOME.NS', 'GODREJPROP.NS', 'EXIDEIND.NS', 'COROMANDEL.NS', 'RAMCOCEM.NS', 'SBICARD.NS', 
              'JKCEMENT.NS', 'ICICIGI.NS', 'TVSMOTOR.NS', 'CONCOR.NS', 'L&TFH.NS', 'ZYDUSLIFE.NS'
              ]

# Create a dictionary to store the last alert time for each stock
last_alert_time = {stock: None for stock in stock_list}

def check_entry_conditions(stock_symbol, stock_data):
    try:
        # Fetch historical stock data
        stock = yf.Ticker(stock_symbol)

        # Get historical data for the stock
        data = stock.history(period="1d", interval="5m")  # Fetch 1-minute interval data


        # Calculate the opening range and high of the opening range breakout
        opening_range = data.between_time('09:15', '09:30')  # Assuming the market opens at 09:15 and closes at 15:30
        high_of_opening_range = opening_range['High'].max()
        low_of_opening_range = opening_range['Low'].min()

        high_crossed = False
        low_crossed = False
        latestPrice = round(data.iloc[-1]['Close'], 2)

        # Check entry conditions
        for idx, row in data.iterrows():
            if idx.time() > dt_time(9, 30) and idx.time() <= dt_time(15, 30):
                if not high_crossed and row['Close'] > high_of_opening_range:
                    # Check if enough time has passed since the last alert
                    last_alert_time_for_stock = last_alert_time[stock_symbol]
                    if (
                        last_alert_time_for_stock is None
                        or (idx - last_alert_time_for_stock).total_seconds() >= 120
                    ):
                        message = f"{stock_symbol} ORB High breakout by : {latestPrice} at {idx.strftime('%H:%M %m-%d')}"
                        print(message)
                        send_slack_notification(message)
                        last_alert_time[stock_symbol] = idx
                    high_crossed = True
                elif not low_crossed and row['Close'] < low_of_opening_range:
                    # Check if enough time has passed since the last alert
                    last_alert_time_for_stock = last_alert_time[stock_symbol]
                    if (
                        last_alert_time_for_stock is None
                        or (idx - last_alert_time_for_stock).total_seconds() >= 120
                    ):
                        message = f"{stock_symbol} ORB Low breakout by : {latestPrice} at {idx.strftime('%H:%M %m-%d')}"
                        print(message)
                        send_slack_notification(message)
                        last_alert_time[stock_symbol] = idx
                    low_crossed = True

         # Check entry conditions by comparing with the previous day's high and low from JSON data
        # if stock_symbol in stock_data:
        #     day_range_high = stock_data[stock_symbol]['Day Range High']
        #     day_range_low = stock_data[stock_symbol]['Day Range Low']

        #     if latestPrice > day_range_high:
        #         message = f"{stock_symbol} crossed Previous Day High by : {latestPrice}"
        #         print(message)
        #         send_slack_notification(message)

        #     if latestPrice < day_range_low:
        #         message = f"{stock_symbol} crossed Previous Day Low by : {latestPrice}"
        #         print(message)
        #         send_slack_notification(message)

    except Exception as e:
        print(f"Error fetching data for {stock_symbol}: {e}")

def main(stock_list):
    while True:
        for stock_symbol in stock_list:
            check_entry_conditions(stock_symbol, stock_data)
        time.sleep(60)  # Check every 5 minutes (adjust as needed)

if __name__ == "__main__":
    main(stock_list)
