import yfinance as yf
import warnings
import json
import time
from datetime import datetime, time as dt_time
import requests

# Ignore FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Define the Slack webhook URL
slack_webhook_url = 'https://hooks.slack.com/services/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'

# Load the stock data from the JSON file
def load_stock_data_from_json(json_file):
    try:
        with open(json_file, 'r') as file:
            stock_data = json.load(file)
        return stock_data
    except FileNotFoundError:
        print("JSON file not found.")
        return {}
    
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
stock_list = ['M&M.NS', 'TCS.NS', 'MCX.NS', 'UBL.NS', 
              'L&TFH.NS', 'ONGC.NS', 'TATAPOWER.NS', 'ADANIPORTS.NS', 'INDIGO.NS', 'JINDALSTEL.NS',
              'HINDPETRO.NS', 'BAJAJFINSV.NS', 'ASIANPAINT.NS', 'DLF.NS', 'TATAMOTORS.NS', 'IRCTC.NS', 
              'ADANIENT.NS', 'BAJFINANCE.NS', 'IDFCFIRSTB.NS', 'ASHOKLEY.NS', 'SAIL.NS', 'HCLTECH.NS', 
              'PNB.NS', 'INFY.NS', 'BALRAMCHIN.NS', 'TITAN.NS', 'TATASTEEL.NS', 'AUROPHARMA.NS',
              'RBLBANK.NS', 'GMRINFRA.NS', 'APOLLOTYRE.NS', 'INDIACEM.NS', 'IOC.NS', 
              ]

# Check for price movements and send alerts
def check_price_movements(stock_data, stock_list):
    while True:
        current_time = datetime.now().time()
        # Check if it's after 9:15 AM
        if current_time >= dt_time(9, 15):
            for stock_symbol, data in stock_data.items():
                if stock_symbol in stock_list:  # Check if the stock is in stock_list
                    closing_price = data.get('Closing Price')
                    if closing_price is not None:
                        # Calculate the percentage change from the opening price (9:15 AM)
                        opening_price = data.get('Day Range High')
                        if opening_price is not None:
                            percentage_change = ((closing_price - opening_price) / opening_price) * 100
                            
                            if abs(percentage_change) >= 2:
                                message = f"ATR for {stock_symbol} has moved more than 2%."
                                print(message)
                                send_slack_notification(message)

                            if abs(percentage_change) <= 2:
                                message = f"ATR for {stock_symbol} has moved more than -2%."
                                print(message)
                                send_slack_notification(message)

        # Sleep for a while (adjust the interval as needed)
        time.sleep(30)  

if __name__ == "__main__":
    json_file = "stock_data_2023-10-08.json"  # Replace with the actual file name
    stock_data = load_stock_data_from_json(json_file)
    check_price_movements(stock_data, stock_list)
