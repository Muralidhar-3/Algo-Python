import pandas as pd
from datetime import datetime

# Load the CSV data
csv_file_path = 'JSON DATA/XAU_5m_data.csv'
data = pd.read_csv(csv_file_path, delimiter=';')

# Convert 'Date' column to datetime
data['Date'] = pd.to_datetime(data['Date'])

# Partition data by year
years = data['Date'].dt.year.unique()

for year in years:
    # Filter data for the current year
    year_data = data[data['Date'].dt.year == year]
    
    # Save the partitioned data to a new CSV file
    output_file_path = f'JSON DATA/XAU_5m_data_{year}.csv'
    year_data.to_csv(output_file_path, index=False)
    print(f'Saved data for {year} to {output_file_path}') 