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

    if strategy == "first":
        # Invest monthly on the first trading day of each month
        previous_month = data.index[0].month
        for date in data.index:
            if date.month != previous_month:
                shares += monthly_investment / data.loc[date]
                total_investment += monthly_investment
                previous_month = date.month
            portfolio_values.at[date, 'Portfolio Value'] = shares * data.loc[date]
            portfolio_values.at[date, 'Total Invested'] = total_investment

    elif strategy == "random":
        last_investment_date = data.index[0]
        for date in data.index:
            if date.month != last_investment_date.month:
                available_days = data.index[data.index.month == date.month]
                if not available_days.empty:
                    random_day = random.choice(available_days)
                    shares += monthly_investment / data.loc[random_day]
                    total_investment += monthly_investment
                    last_investment_date = random_day
            portfolio_values.at[date, 'Portfolio Value'] = shares * data.loc[date]
            portfolio_values.at[date, 'Total Invested'] = total_investment

    elif strategy == "losing":
        previous_month = data.index[0].month
        previous_year = data.index[0].year
        falling_days = 0
        invested = False
        for date in data.index:
            if date.month != previous_month:
                if not invested:
                    last_day_of_previous_month = data[(data.index.year == previous_year) & (data.index.month == previous_month)].index[-1]
                    shares += monthly_investment / data.loc[last_day_of_previous_month]
                    total_investment += monthly_investment
                previous_month = date.month
                previous_year = date.year
                falling_days = 0
                invested = False

            if date > data.index[0]:
                if float(data.loc[date]) < float(data.loc[data.index[data.index.get_loc(date) - 1]]):
                    falling_days += 1
                else:
                    falling_days = 0

            if falling_days >= 4 and not invested:
                shares += monthly_investment / data.loc[date]
                total_investment += monthly_investment
                invested = True

            portfolio_values.at[date, 'Portfolio Value'] = shares * float(data.loc[date])
            portfolio_values.at[date, 'Total Invested'] = total_investment
    
    elif strategy == "buythedip":
        recent_peak = float(first_price)  # first_price is already computed from data
        for date in data.index:
            current_price = float(data.loc[date])  # Get scalar value from the Series
            
            # Check if the current price has dropped by 5% or more from the recent peak
            if current_price < recent_peak * 0.95:
                shares += monthly_investment / current_price  # Invest at the current price
                total_investment += monthly_investment         # Increase total investment
                recent_peak = current_price                     # Reset the peak to current price
            
            portfolio_values.at[date, 'Portfolio Value'] = shares * current_price
            portfolio_values.at[date, 'Total Invested'] = total_investment

    return portfolio_values.index, portfolio_values['Portfolio Value'], portfolio_values['Total Invested']
