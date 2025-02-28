import pandas as pd
from datetime import datetime, timedelta

# Load the CSV data for 2024
csv_file_path = 'JSON DATA/XAU_5m_data_2024.csv'
data = pd.read_csv(csv_file_path, delimiter=',')

# Print the column names to verify
print("Columns in the CSV:", data.columns)

# Convert 'Date' column to datetime
# Assuming the 'Date' column is in the format 'YYYY-MM-DD HH:MM:SS'
data['Date'] = pd.to_datetime(data['Date'])

# Debugging: Print the first few rows of the data
print("Data for 2024:")
print(data.head())

# Convert UTC+2 to IST (UTC+5:30)
data['Date'] = data['Date'] + timedelta(hours=3, minutes=30)

# Debugging: Print the first few rows of the data
print("Data for 2024:")
print(data.head())

# Filter data for the year 2024
data = data[data['Date'].dt.year == 2024]

# Debugging: Print the first few rows of the filtered data
print("Filtered data for 2024:")
print(data.head())

# At the start of the script, after loading the data
print("\nSample of raw data from CSV:")
print(data.head(20))  # Print first 20 rows to see the time intervals

# Define ORB session times in IST
def get_session_times():
    return {
        'Tokyo': {'start': datetime.strptime('05:30', '%H:%M').time(), 'end': datetime.strptime('09:00', '%H:%M').time()},
        'London': {'start': datetime.strptime('13:30', '%H:%M').time(), 'end': datetime.strptime('16:00', '%H:%M').time()},
        'New York': {'start': datetime.strptime('18:30', '%H:%M').time(), 'end': datetime.strptime('21:00', '%H:%M').time()}
    }

# Filter data for each ORB session
def filter_orb_data(data):
    session_times = get_session_times()
    orb_data = {}
    for date in data['Date'].dt.normalize().unique():
        day_data = data[data['Date'].dt.normalize() == date]
        for session_name, times in session_times.items():
            session_data = day_data[(day_data['Date'].dt.time >= times['start']) & (day_data['Date'].dt.time < times['end'])]
            if len(session_data) >= 6:
                orb_high = session_data['High'].iloc[:6].max()
                orb_low = session_data['Low'].iloc[:6].min()
                print(f"{date.date()} {session_name} session ORB High: {orb_high}, ORB Low: {orb_low}")
            if session_name not in orb_data:
                orb_data[session_name] = session_data
            else:
                orb_data[session_name] = pd.concat([orb_data[session_name], session_data])
    return orb_data

# Filter the data for ORB sessions
orb_data = filter_orb_data(data)

# Function to backtest ORB strategy
def backtest_orb(data):
    session_times = get_session_times()
    results = []

    # Iterate over each day
    for date in data['Date'].dt.normalize().unique():
        day_data = data[data['Date'].dt.normalize() == date]
        print(f"\nProcessing date: {date.date()}")
        print(f"Total candles for the day: {len(day_data)}")

        # Iterate over each session
        for session_name, times in session_times.items():
            # Get all session data
            session_data = day_data[(day_data['Date'].dt.time >= times['start']) & 
                                  (day_data['Date'].dt.time < times['end'])]

            # Debugging: Print session data length and time range
            print(f"\n{date.date()} {session_name} session:")
            print(f"Session time range: {times['start']} to {times['end']}")
            print(f"Number of candles: {len(session_data)}")
            if len(session_data) > 0:
                print("First candle time:", session_data.iloc[0]['Date'])
                print("Last candle time:", session_data.iloc[-1]['Date'])

            # Ensure there are more than 6 candles (6 for ORB + at least 1 for breakout)
            if len(session_data) <= 6:
                print(f"Skipping {session_name} session on {date.date()} due to insufficient data.")
                continue

            # Calculate ORB high and low from first 6 candles
            orb_high = session_data['High'].iloc[:6].max()
            orb_low = session_data['Low'].iloc[:6].min()

            # Debugging: Print ORB high and low
            print(f"{date.date()} {session_name} session ORB High: {orb_high}, ORB Low: {orb_low}")

            # Check for breakouts in remaining candles
            remaining_candles = session_data.iloc[6:]
            print(f"Checking {len(remaining_candles)} candles for breakouts")

            for _, row in remaining_candles.iterrows():
                print(f"Checking price at {row['Date']}: Close={row['Close']}, ORB High={orb_high}, ORB Low={orb_low}")
                
                if row['Close'] > orb_high:
                    # Buy signal
                    entry_price = row['Close']
                    sl = orb_low
                    tp = entry_price + (entry_price - sl)  # 1:1 TP
                    profit_loss = tp - entry_price
                    results.append({
                        'session': session_name,
                        'type': 'Buy',
                        'entry': entry_price,
                        'sl': sl,
                        'tp': tp,
                        'date': row['Date'],
                        'profit_loss': profit_loss
                    })
                    print(f"Buy signal at {row['Date']}: Entry {entry_price}, SL {sl}, TP {tp}")
                    break
                elif row['Close'] < orb_low:
                    # Sell signal
                    entry_price = row['Close']
                    sl = orb_high
                    tp = entry_price - (sl - entry_price)  # 1:1 TP
                    profit_loss = entry_price - tp
                    results.append({
                        'session': session_name,
                        'type': 'Sell',
                        'entry': entry_price,
                        'sl': sl,
                        'tp': tp,
                        'date': row['Date'],
                        'profit_loss': profit_loss
                    })
                    print(f"Sell signal at {row['Date']}: Entry {entry_price}, SL {sl}, TP {tp}")
                    break

    return results

# Run backtest
results = backtest_orb(data)

# Convert results to DataFrame
results_df = pd.DataFrame(results)

# Create performance summary
if not results_df.empty:
    # Calculate session-wise statistics
    session_stats = results_df.groupby('session').agg({
        'type': 'count',
        'profit_loss': ['sum', 'mean']
    }).round(2)

    # Create a summary DataFrame
    summary_df = pd.DataFrame({
        'Summary_Metric': [
            'Total_Trades',
            'Total_Profit_Loss',
            'Buy_Trades',
            'Sell_Trades',
            '---Session_Stats---',
            *[f"{session}_{metric}" for session in session_stats.index for metric in ['trades', 'total_pl', 'avg_pl']]
        ],
        'Value': [
            len(results_df),
            results_df['profit_loss'].sum().round(2),
            len(results_df[results_df['type'] == 'Buy']),
            len(results_df[results_df['type'] == 'Sell']),
            '-------------------',
            *[val for session in session_stats.index for val in [
                session_stats.loc[session, ('type', 'count')],
                session_stats.loc[session, ('profit_loss', 'sum')],
                session_stats.loc[session, ('profit_loss', 'mean')]
            ]]
        ]
    })

    # Save individual trades and summary to separate sheets in Excel
    with pd.ExcelWriter('orb_backtest_results.xlsx') as writer:
        results_df.to_excel(writer, sheet_name='Trades', index=False)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

    # Print the summary
    print("\n=== Strategy Performance Summary ===")
    print(summary_df)
else:
    print("No trades were executed during the backtest period")
    # Create empty Excel file with headers
    with pd.ExcelWriter('orb_backtest_results.xlsx') as writer:
        pd.DataFrame(columns=['session', 'type', 'entry', 'sl', 'tp', 'date', 'profit_loss']).to_excel(writer, sheet_name='Trades', index=False)
        pd.DataFrame(columns=['Summary_Metric', 'Value']).to_excel(writer, sheet_name='Summary', index=False) 