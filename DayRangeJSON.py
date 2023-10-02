import yfinance as yf
import time
from datetime import datetime, time as dt_time
import warnings
import json

# Ignore FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Define the symbols of the NSE-listed stocks you want to track
stock_list = ['HDFCBANK.NS', 'ICICIBANK.NS', 'AXISBANK.NS', 'SBIN.NS', 'BAJFINANCE.NS', 'BAJAJFINSV.NS', 
              'HDFCAMC.NS', 'SHRIRAMFIN.NS', 'ICICIGI.NS', 'SBILIFE.NS', 'MUTHOOTFIN.NS', 'CHOLAFIN.NS', 
              'PEL.NS', 'HDFCLIFE.NS', 'ICICIPRULI.NS', 'M&MFIN.NS', 'IBULHSGFIN.NS', 'CANBK.NS', 
              'FEDERALBNK.NS','AUBANK.NS', 'PNB.NS', 'KOTAKBANK.NS', 'BANKBARODA.NS', 'BANDHANBNK.NS', 
              'INDUSINDBK.NS', 'RBLBANK.NS', 'IOB.NS', 'INDIANB.NS', 'UCOBANK.NS', 'PSB.NS', 'CENTRALBK.NS', 
              'MAHABANK.NS','BANKINDIA.NS', 'UNIONBANK.NS', 'J&KBANK.NS', 'BAJAJ-AUTO.NS', 'HEROMOTOCO.NS', 
              'M&M.NS','BHARATFORG.NS', 'MARUTI.NS', 'TATAMOTORS.NS', 'EICHERMOT.NS', 'MOTHERSON.NS', 'MRF.NS',
              'EXIDEIND.NS', 'BALKRISIND.NS', 'AMARAJABAT.NS', 'TVSMOTOR.NS', 'BOSCHLTD.NS', 'ASHOKLEY.NS', 
              'ESCORTS.NS', 'DABUR.NS', 'HINDUNILVR.NS', 'MCDOWELL-N.NS', 'ITC.NS', 'BRITANNIA.NS', 'TATACONSUM.NS',
              'NESTLEIND.NS', 'GODREJCP.NS', 'COLPAL.NS', 'UBL.NS', 'MARICO.NS', 'JUBLFOOD.NS', 'TECHM.NS', 
              'INFY.NS', 'HCLTECH.NS', 'LTTS.NS', 'TCS.NS', 'BSOFT.NS', 'LTIM.NS', 'WIPRO.NS', 'PERSISTENT.NS', 
              'OFSS.NS', 'NAUKRI.NS', 'MPHASIS.NS', 'COFORGE.NS', 'TV18BRDCST.NS', 'NETWORK18.NS', 'ZEEL.NS', 
              'PVRINOX.NS', 'SUNTV.NS', 'VEDL.NS', 'JSWSTEEL.NS', 'HINDALCO.NS', 'COALINDIA.NS', 'NMDC.NS', 
              'TATASTEEL.NS', 'JINDALSTEL.NS', 'HINDZINC.NS', 'NATIONALUM.NS', 'SAIL.NS', 'HINDCOPPER.NS', 
              'GLENMARK.NS', 'LALPATHLAB.NS', 'METROPOLIS.NS', 'BIOCON.NS', 'ZYDUSLIFE.NS', 'DRREDDY.NS', 
              'CIPLA.NS', 'SUNPHARMA.NS', 'ALKEM.NS', 'APLLTD.NS', 'DIVISLAB.NS', 'GRANULES.NS', 'LUPIN.NS', 
              'TORNTPHARM.NS', 'LAURUSLABS.NS', 'AUROPHARMA.NS', 'YESBANK.NS', 'IDFCFIRSTB.NS', 'PHOENIXLTD.NS', 
              'GODREJPROP.NS', 'DLF.NS', 'SUNTECK.NS', 'HEMIPROP.NS', 'OBEROIRLTY.NS', 'BRIGADE.NS', 'IBREALEST.NS',
              'PRESTIGE.NS', 'SOBHA.NS', 'ADANIGREEN.NS', 'GSPL.NS', 'HINDPETRO.NS', 'POWERGRID.NS', 'GUJGASLTD.NS',
              'IOC.NS', 'BPCL.NS', 'PETRONET.NS', 'RELIANCE.NS', 'ONGC.NS', 'GAIL.NS', 'NTPC.NS','MGL.NS', 'IGL.NS', 
              'TATAPOWER.NS', 'TORNTPOWER.NS', 'ADANIENSOL.NS', 

              'DIXON.NS', 'INDIACEM.NS', 'GMRINFRA.NS', 'IDFC.NS', 'ASTRAL.NS', 
              'INDHOTEL.NS', 'GNFC.NS', 'TATACHEM.NS', 'HAVELLS.NS', 'CROMPTON.NS', 'IRCTC.NS', 'UPL.NS', 
              'INDUSTOWER.NS', 'MANAPPURAM.NS', 'APOLLOHOSP.NS', 'APOLLOTYRE.NS', 'DEEPAKNTR.NS', 'BALRAMCHIN.NS',
              'PFC.NS', 'HAL.NS', 'SBICARD.NS', 'MCX.NS', 'PIIND.NS', 'SHREECEM.NS', 'PAGEIND.NS',
              'INDIAMART.NS', 'AMBUJACEM.NS', 'SRF.NS', 'COROMANDEL.NS', 'RAMCOCEM.NS', 'NAVINFLUOR.NS',
              'ABCAPITAL.NS', 'ABB.NS', 'JKCEMENT.NS', 'BATAINDIA.NS', 'ABBOTINDIA.NS', 'MFSL.NS',
              'CUMMINSIND.NS', 'SIEMENS.NS', 'IEX.NS', 'ATUL.NS', 'ACC.NS', 'DELTACORP.NS', 'CONCOR.NS',
            
              ]

# Initialize a dictionary to store the stock data
stock_data = {}

def check_day_range(stock_symbol):
    try:
        # Fetch historical stock data
        stock = yf.Ticker(stock_symbol)

        # Get historical data for the stock with 1-day interval
        data = stock.history(period="1d", interval="1m")

        # Define the time for 9:15 AM
        target_time = dt_time(9, 15)

        # Filter data after 9:15
        data_after_915 = data[data.index.time >= target_time]

        # Check if there is data available after 9:15
        if not data_after_915.empty:
            # Calculate the opening range (high and low) after 9:15
            day_range_high = data_after_915['High'].max()
            day_range_low = data_after_915['Low'].min()

            # Store the data in the stock_data dictionary
            stock_data[stock_symbol] = {
                'Day Range High': day_range_high,
                'Day Range Low': day_range_low
            }

            # Print the stock symbol and its opening range after 9:15
            # print(f"{stock_symbol} Day Range High:", day_range_high)
            # print(f"{stock_symbol} Day Range Low:", day_range_low)
        else:
            print(f"No data available for {stock_symbol} after 9:15 AM.")

    except Exception as e:
        print(f"Error fetching data for {stock_symbol}: {e}")

def save_stock_data_to_json():
    try:
        # Get the current time
        current_time = datetime.now().time()

        # Check if it's 14:30
        if current_time >= dt_time(15, 30):

            # Get today's date in "YYYY-MM-DD" format
            today_date = datetime.now().strftime("%Y-%m-%d")
            
            # Define the file name with today's date
            file_name = f"stock_data_{today_date}.json"
            
            # Save the stock data to a JSON file
            with open(file_name, 'w') as json_file:
                json.dump(stock_data, json_file, indent=4)
            print("Stock data saved to stock_data.json")
    
    except Exception as e:
        print(f"Error saving stock data to JSON: {e}")

def main(stock_list):
    while True:
        for stock_symbol in stock_list:
            check_day_range(stock_symbol)
        
        # Check and save data at 14:30
        save_stock_data_to_json()

        time.sleep(3600)  # Check every 5 minutes (adjust as needed)

if __name__ == "__main__":
    main(stock_list)
