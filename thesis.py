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

portfolio_dates, portfolio_values, total_invested = simulate_investment.simulate_investment(
                stock, initial_amount, monthly_investment, strategy, years
            )

inflated_total = inflation.calculate_value(portfolio_dates, total_invested)

print(inflated_total)