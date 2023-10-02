import yfinance as yf
import time 
from datetime import time as dt_time
import concurrent.futures
from datetime import datetime, timedelta
import warnings
import requests
import json
import os
import logging

# Ignore FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Constants
check_interval_seconds = 30
slack_webhook_url = os.environ.get('https://hooks.slack.com/services/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')

# Initialize logging
logging.basicConfig(filename='stock_monitor.log', level=logging.INFO)

class StockMonitor:
    def __init__(self, stock_list):
        self.stock_list = stock_list
        self.last_alert_time = {stock: None for stock in stock_list}
        self.last_condition_time = {}
        self.stock_data = self.load_stock_data()

    def load_stock_data(self):
        try:
            with open('stock_data.json', 'r') as json_file:
                data = json.load(json_file)
            return data
        except FileNotFoundError:
            return {}

    # You can call this function to load the data at the beginning of your script:
    # stock_data = load_stock_data()

    # Define the send_slack_notification function
    def send_slack_notification(self, message):
        try:
           payload = {'text': message}
           response = requests.post(slack_webhook_url, json=payload)

           if response.status_code == 200:
                logging.info('Notification sent successfully to Slack')
           else:
                logging.error('Failed to send notification to Slack')
                logging.error(response.text)
        
        except Exception as e:
            logging.error(f"Error sending Slack notification: {e}")

    def check_entry_conditions(stock_symbol, stock_data, last_alert_time, last_condition_time, send_slack_notification):
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

            current_time = time.time()

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
                            last_alert_time[stock_symbol] = idx
                        low_crossed = True

            # Check entry conditions by comparing with the previous day's high and low from JSON data
            if stock_symbol in stock_data:
                day_range_high = stock_data[stock_symbol]['Day Range High']
                day_range_low = stock_data[stock_symbol]['Day Range Low']

                if latestPrice > day_range_high:
                    message = f"{stock_symbol} crossed Previous Day High by : {latestPrice}"

                if latestPrice < day_range_low:
                    message = f"{stock_symbol} crossed Previous Day Low by : {latestPrice}"

            # Check if the stock_symbol has an entry in the last_condition_time dictionary
            if stock_symbol not in last_condition_time:
                last_condition_time[stock_symbol] = {'high': 0, 'low': 0}

            # Check both the conditions
            if stock_symbol in stock_data:
                if latestPrice > day_range_high and row['Close'] > high_of_opening_range:
                    # Check if it's been at least 60 seconds since the last high condition
                    if current_time - last_condition_time[stock_symbol]['high'] >= 21600:
                        message = f"Both high's are crossed by {stock_symbol} at {time.ctime()}"
                        print(message)
                        send_slack_notification(message)
                        last_condition_time[stock_symbol]['high'] = current_time

                if latestPrice < day_range_low and row['Close'] < low_of_opening_range:
                    # Check if it's been at least 60 seconds since the last low condition
                    if current_time - last_condition_time[stock_symbol]['low'] >= 21600:
                        message = f"Both low's are crossed by {stock_symbol} at {time.ctime()}"
                        print(message)
                        send_slack_notification(message)
                        last_condition_time[stock_symbol]['low'] = current_time

        except Exception as e:
            print(f"Error fetching data for {stock_symbol}: {e}")



    def main(self):
        while True:
            for stock_symbol in self.stock_list:
                if isinstance(stock_symbol, str):  # Check if stock_symbol is a string
                    self.check_entry_conditions(stock_symbol, self.last_alert_time, self.last_condition_time, self.send_slack_notification)
                else:
                    print(f"Invalid stock symbol: {stock_symbol}")
            time.sleep(check_interval_seconds)  # Check every 5 minutes (adjust as needed)

if __name__ == "__main__":

    # Define the symbols of the NSE-listed stocks you want to track
    stock_list = ['EICHERMOT.NS', 'BAJFINANCE.NS', 'DELTACORP.NS', 'TATACONSUM.NS', 'TRENT.NS', 
                'MCX.NS','TATASTEEL.NS', 'BERGEPAINT.NS', 'MANAPPURAM.NS', 'ESCORTS.NS', 'PNB.NS',
                'MARUTI.NS', 'DIXON.NS', 'BAJAJFINSV.NS', 'BALRAMCHIN.NS', 'JUBLFOOD.NS', 'TVSMOTOR.NS', 
                'POWERGRID.NS', 'RBLBANK.NS', 'ASIANPAINT.NS', 'CANBK.NS', 'TITAN.NS', 'DRREDDY.NS', 
                'TCS.NS', 'WIPRO.NS', 'ULTRACEMCO.NS', 'APOLLOHOSP.NS', 'IRCTC.NS', 'HDFCLIFE.NS', 'SAIL.NS',
                'LT.NS', 'IBULHSGFIN.NS', 'COALINDIA.NS', 'BEL.NS', 'RELIANCE.NS', 'HAL.NS',
                'INFY.NS', 'HDFCAMC.NS',

                'CANFINHOME.NS', 'GODREJPROP.NS', 'OFSS.NS', 'LTTS.NS', 'RAMCOCEM.NS', 'CROMPTON.NS', 
                'DALBHARAT.NS', 'SUNTV.NS', 'JSWSTEEL.NS', 'CANFINHOME.NS'
                ]
    

    stock_monitor = StockMonitor(stock_list)
    stock_monitor.main()
