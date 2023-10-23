import yfinance as yf
import pandas as pd
import numpy as np
# import matplotlib as plt

# -------- Getting data for individual stock -----------
# Reliance = yf.download('RELIANCE.NS', start='2023-09-20', end='2023-09-24')
# print(Reliance)

# -------- Getting data for multiple stock -----------
stocksList = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS']
stocks = yf.download(stocksList, start='2023-10-04', end='2023-10-05')
# print(stocks)

# ----------- Saving the Data into a excel file ------------
stocks.to_csv("stocksData.csv")
stocksData = pd.read_csv("stocksData.csv")
# print(stocksData)

# ------------editing the file --------------
# ------------- for getting the heading right ------------
stocksData = pd.read_csv("stocksData.csv", header=[0,1])
# print(stocksData)

# ------------- for getting the headings correct and date to the first coumn --------
stocksData = pd.read_csv("stocksData.csv", header=[0,1], index_col=[0])
print(stocksData)