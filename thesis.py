import yfinance as yf
import simulate_investment
import connect

# List of stocks and strategies
stock = "^GSPC"
strategy = "losing"

# Simulate the investment for each stock and strategy
initial_amount = 200
monthly_investment = 200
years=10
preset_id=0

# Simulate the investment
a,b,c=connect.fetch_preset_table(stock, initial_amount, monthly_investment, strategy, years)
print(a)