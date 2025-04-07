import yfinance as yf
import pandas as pd
import random

def simulate_investment(stock, initial_amount, monthly_investment, strategy, years, preset_id=None):
    # Ensure the index is datetime
    yesterday = pd.Timestamp.today().normalize() - pd.DateOffset(days=1)
    earliest = yesterday - pd.DateOffset(years=years)
    
    # Fetch data from Yahoo Finance
    data = yf.download(stock, start=earliest, end=yesterday)['Close']
    data.index = pd.to_datetime(data.index)
    
    # Debugging step: Print data info
    print(f"Downloaded data for {stock} from {earliest.date()} to {yesterday.date()}:")
    print(data.head())
    
    # Check if data is empty
    if data.empty:
        raise ValueError(f"No data retrieved for {stock}. Check ticker symbol and date range.")
    
    # Ensure first available price exists
    first_price = data.dropna().iloc[0] if not data.dropna().empty else None
    if first_price is None:
        raise ValueError(f"No valid price data found for {stock}.")
    
    # Initialize portfolio tracking
    portfolio_values = pd.DataFrame(index=data.index)
    portfolio_values['Close'] = data
    portfolio_values['Portfolio Value'] = 0.0  # Initialize Portfolio Value column
    portfolio_values['Total Invested'] = 0.0  # Initialize Total Invested column

    shares = initial_amount / first_price  # Initial shares bought
    total_investment = initial_amount

    # Simulate Compound Interest with Monthly Investments
    if strategy in ["first", "random", "losing", "buythedip"]:
        for date in data.index:
            # Recalculate portfolio value considering reinvestment
            portfolio_value = shares * data.loc[date]
            portfolio_values.at[date, 'Portfolio Value'] = portfolio_value
            portfolio_values.at[date, 'Total Invested'] = total_investment

            # Reinvest dividends or additional capital (if any)
            # Simulate a new investment based on strategy logic
            if strategy == "first":
                if date.month != data.index[0].month:  # Invest monthly on the first day of the month
                    shares += monthly_investment / data.loc[date]
                    total_investment += monthly_investment
            elif strategy == "random":
                # Random monthly investment
                available_days = data.index[data.index.month == date.month]
                if not available_days.empty:
                    random_day = random.choice(available_days)
                    shares += monthly_investment / data.loc[random_day]
                    total_investment += monthly_investment
            elif strategy == "losing":
                # Invest if the price is falling
                if date > data.index[0]:
                    if data.loc[date] < data.loc[data.index[data.index.get_loc(date) - 1]]:
                        shares += monthly_investment / data.loc[date]
                        total_investment += monthly_investment
            elif strategy == "buythedip":
                recent_peak = data.loc[0]  # or use first available price
                if data.loc[date] < recent_peak * 0.95:
                    shares += monthly_investment / data.loc[date]
                    total_investment += monthly_investment
                    recent_peak = data.loc[date]
    
    return portfolio_values.index, portfolio_values['Portfolio Value'], portfolio_values['Total Invested']
