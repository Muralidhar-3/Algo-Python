import yfinance as yf
import time 
from datetime import time as dt_time
from datetime import datetime, timedelta
import warnings
import requests

# Ignore FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Define the Slack webhook URL
slack_webhook_url = 'https://hooks.slack.com/services/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'

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
stock_list = ['HDFCBANK.NS', 'MCX.NS', 'TCS.NS', 'TITAN.NS', 'APOLLOTYRE.NS', 
              'AUBANK.NS','HCLTECH.NS', 'M&M.NS', 'POWERGRID.NS', 'BIOCON.NS', 'UPL.NS', 
              'ULTRACEMCO.NS', 'BAJAJ-AUTO.NS', 'POLYCAB.NS', 'M&MFIN.NS', 'TECHM.NS', 'PNB.NS', 
              'RELIANCE.NS', 'HINDALCO.NS', 'AXISBANK.NS', 'GLENMARK.NS', 'VEDL.NS', 'PFC.NS', 
              'TATASTEEL.NS', 'JSWSTEEL.NS', 'HAL.NS', 'BANDHANBNK.NS', 'MARUTI.NS', 'DRREDDY.NS', 'CANBK.NS',
              'SBIN.NS', 'IBULHSGFIN.NS', 'RECLTD.NS', 'FEDERALBNK.NS']

# Create a dictionary to store the last alert time for each stock
last_alert_time = {stock: None for stock in stock_list}

def check_entry_conditions(stock_symbol):
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
                        message = f"Alert: High crossed by {stock_symbol} : {latestPrice} at {idx.strftime('%H:%M %m-%d')}"
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
                        message = f"Alert: Low crossed by {stock_symbol} : {latestPrice} at {idx.strftime('%H:%M %m-%d')}"
                        print(message)
                        send_slack_notification(message)
                        last_alert_time[stock_symbol] = idx
                    low_crossed = True

        # Check entry conditions
        if (data.iloc[-1]['Close'] > high_of_opening_range):
            print(f"Alert: Entry conditions met for {stock_symbol}")

    except Exception as e:
        print(f"Error fetching data for {stock_symbol}: {e}")

def main(stock_list):
    while True:
        for stock_symbol in stock_list:
            check_entry_conditions(stock_symbol)
        time.sleep(120)  # Check every 5 minutes (adjust as needed)

if __name__ == "__main__":
    main(stock_list)
