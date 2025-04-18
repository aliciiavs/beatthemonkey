import yfinance as yf
import simulate_investment
#import connect
import inflation

# List of stocks and strategies
stock = "^GSPC"
strategy = "losing"

# Simulate the investment for each stock and strategy
initial_amount = 201
monthly_investment = 200
years=10
preset_id=1
current_seed = 1

portfolio_dates, portfolio_values, total_invested, random_portfolio_values = simulate_investment.simulate_investment(
                stock, initial_amount, monthly_investment, strategy, years, current_seed
            )

print(random_portfolio_values)