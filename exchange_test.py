import yfinance as yf
import pandas as pd

# Define the stock ticker and the currency pair
stock_ticker = "AAPL"  # Example: Apple Inc.
exchange_rate_ticker = "EURUSD=X"

# Define the date range for the historical data
start_date = "2023-01-01"
end_date = "2023-12-31"

# Get historical stock data for a stock traded in dollars
stock_data = yf.download(stock_ticker, start=start_date, end=end_date)

# Get historical exchange rate data for EUR/USD
exchange_rate_data = yf.download(exchange_rate_ticker, start=start_date, end=end_date)

# Merge stock data with exchange rate data
merged_data = pd.merge(stock_data['Close'], exchange_rate_data['Close'], left_index=True, right_index=True)
merged_data.columns = ['Stock_Price_USD', 'EUR_USD']

# Convert stock prices to euros
merged_data['Stock_Price_EUR'] = merged_data['Stock_Price_USD'] / merged_data['EUR_USD']

# Print the resulting DataFrame
print(merged_data.head())
