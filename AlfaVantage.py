import requests
import pandas as pd
from datetime import datetime, timedelta

# Replace 'YOUR_API_KEY' with your actual Alpha Vantage API key
api_key = 'JQYSMHKOW5VA33TF'

# Define the symbol for the NSE stock you want to track
symbol = 'TCS.NS'  # Example: TCS Ltd.

# Calculate the date of the previous trading day (excluding weekends)
current_date = datetime.now().date()
previous_trading_day = current_date - timedelta(days=1)

# Format the date in YYYY-MM-DD format
previous_trading_day_str = previous_trading_day.strftime('%Y-%m-%d')

# Define the Alpha Vantage API endpoint for daily data
endpoint = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={api_key}'

# Make the API request to Alpha Vantage
response = requests.get(endpoint)

if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Extract daily data for the previous trading day
    if 'Time Series (Daily)' in data:
        daily_data = data['Time Series (Daily)']
        
        # Find the entry for the previous trading day
        previous_day_entry = daily_data.get(previous_trading_day_str)
        
        if previous_day_entry:
            # Extract the high and low values
            previous_day_high = float(previous_day_entry['2. high'])
            previous_day_low = float(previous_day_entry['3. low'])

            print(f"Previous Trading Day ({previous_trading_day_str}) High for {symbol}: {previous_day_high}")
            print(f"Previous Trading Day ({previous_trading_day_str}) Low for {symbol}: {previous_day_low}")

            # Create a DataFrame
            df = pd.DataFrame({
                'Symbol': [symbol],
                'Date': [previous_trading_day_str],
                'High': [previous_day_high],
                'Low': [previous_day_low]
            })

            # Save the data to an Excel file
            excel_file_name = f"{symbol}_previous_day_data.xlsx"
            df.to_excel(excel_file_name, index=False)

            print(f"Data saved to {excel_file_name}")
        else:
            print(f"No data available for {symbol} on {previous_trading_day_str}")
    else:
        print("Daily data not found in the response.")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
