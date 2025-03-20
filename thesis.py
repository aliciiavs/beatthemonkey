import yfinance as yf
import simulate_investment

# List of stocks and strategies
stock = "^GSPC"
strategy = "losing"

# Simulate the investment for each stock and strategy
initial_amount = 200
monthly_investment = 200
years=10

# Simulate the investment
a,b,c=simulate_investment.simulate_investment(stock, initial_amount, monthly_investment, strategy, years)
print(a)