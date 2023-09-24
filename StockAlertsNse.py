import time
from datetime import time as dt_time
from datetime import datetime, timedelta
from nsetools import Nse
import requests

# Define the Slack webhook URL
slack_webhook_url = 'https://hooks.slack.com/services/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'

# Define the send_slack_notification function
# def send_slack_notification(message):
#     try:
#         payload = {
#             'text': message,
#         }

#         response = requests.post(slack_webhook_url, json=payload)

#         if response.status_code == 200:
#             print('Notification sent successfully to Slack')
#         else:
#             print('Failed to send notification to Slack')
#             print(response.text)

#     except Exception as e:
#         print(f"Error sending Slack notification: {e}")

# Define the symbols of the NSE-listed stocks you want to track
stock_list = ['HDFCBANK', 'MCX', 'TCS', 'TITAN', 'APOLLOTYRE',
              'AUBANK', 'HCLTECH', 'M&M', 'POWERGRID', 'BIOCON', 'UPL',
              'ULTRACEMCO', 'BAJAJ-AUTO', 'POLYCAB', 'M&MFIN', 'TECHM', 'PNB',
              'RELIANCE', 'HINDALCO', 'AXISBANK', 'GLENMARK', 'VEDL', 'PFC',
              'TATASTEEL', 'JSWSTEEL', 'HAL', 'BANDHANBNK', 'MARUTI', 'DRREDDY', 'CANBK',
              'SBIN', 'IBULHSGFIN', 'RECLTD', 'FEDERALBNK']

# Create a dictionary to store the last alert time for each stock
last_alert_time = {stock: None for stock in stock_list}

# Create a dictionary to store the entry conditions flag for each stock
entry_conditions_met = {stock: False for stock in stock_list}

nse = Nse()

def check_entry_conditions(stock_symbol):
    try:
        # Fetch real-time stock data
        stock_info = nse.get_quote(stock_symbol)

        latestPrice = stock_info['lastPrice']
        stock_name = stock_info['companyName']

        if not entry_conditions_met[stock_symbol]:
            if float(latestPrice) > float(stock_info['dayHigh']):
                message = f"Alert: High crossed by {stock_name} : {latestPrice} for stock symbol {stock_symbol} on {datetime.now().strftime('%H:%M %m-%d')}"
                print(message)
                # send_slack_notification(message)
                entry_conditions_met[stock_symbol] = True

    except Exception as e:
        print(f"Error fetching data for {stock_symbol}: {e}")

def main(stock_list):
    while True:
        for stock_symbol in stock_list:
            check_entry_conditions(stock_symbol)
        time.sleep(120)  # Check every 2 minutes (adjust as needed)

if __name__ == "__main__":
    main(stock_list)
