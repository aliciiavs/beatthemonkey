import yfinance as yf
import pandas as pd
import random

def simulate_investment(stock, initial_amount, monthly_investment, strategy, years, current_seed, preset_id=None):
    # Ensure the index is datetime
    yesterday = pd.Timestamp.today().normalize() - pd.DateOffset(days=1)
    earliest = yesterday - pd.DateOffset(years=years)
    
    # Fixing exchange issue (give stock in EUR)
    exchange_rate_ticker = "EURUSD=X"
    exchange_rate_data = yf.download(exchange_rate_ticker, start=earliest, end=yesterday)['Close']
    
    # Fetch data from Yahoo Finance
    stock_data = yf.download(stock, start=earliest, end=yesterday)['Close']
    stock_data.index = pd.to_datetime(stock_data.index)

    data = pd.merge(stock_data, exchange_rate_data, left_index=True, right_index=True)
    data.columns = ['Stock_Price_USD', 'EUR_USD']
    
    # Convert stock prices to euros
    data['Stock_Price_EUR'] = (data['Stock_Price_USD'] / data['EUR_USD']).astype(float)
    data = data.drop(columns=['Stock_Price_USD', 'EUR_USD'])
    #data = stock_data

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
    portfolio_values['Random Value'] = 0.0  # Initialize Total Invested column
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

    elif strategy == "growing":
        previous_month = data.index[0].month
        previous_year = data.index[0].year
        rising_days = 0
        invested = False
        for date in data.index:
            if date.month != previous_month:
                if not invested:
                    last_day_of_previous_month = data[(data.index.year == previous_year) & (data.index.month == previous_month)].index[-1]
                    shares += monthly_investment / data.loc[last_day_of_previous_month]
                    total_investment += monthly_investment
                previous_month = date.month
                previous_year = date.year
                rising_days = 0
                invested = False

            if date > data.index[0]:
                if float(data.loc[date]) > float(data.loc[data.index[data.index.get_loc(date) - 1]]):
                    rising_days += 1
                else:
                    rising_days = 0

            if rising_days >= 3 and not invested:
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

    elif strategy == "0.98buythedip":
        """
        To proceed with the simulation, a number of strategies needed to be defined. The requisites for the app were
        that the simulated movements require low effort and little time, reinforcing the idea of low-intervention
        investing strategies (buy-and-hold).

        Buy-The-Dip is a very popular beginner's strategy, however, it requires some calculations that can be provided
        by a phone application or notification. It has been well studied and it has proven to beat the market (our monkey)
        several times (ADD SOME REFERENCES, one is chill). Its logic is, when the value of our selected asset drops by a
        certain percentage, we buy. 

        In order to fit the input idea, the strategy was adapted into an easier and more specified model.
        
        Hold a budget.
        If the next day drop more than 20% then buy. Else, do not. Keep it in a count and then invest
        when it is correct to do so. If the period ends and still leftover cash, invest all. 
        """
        previous_month = data.index[0].month
        previous_year = data.index[0].year
        current_budget = 0
        for date in data.index:
            if date.month != previous_month:
                current_budget += monthly_investment
                previous_month = date.month
                previous_year = date.year
                total_investment += monthly_investment
            if date > data.index[0]:
                if current_budget > 0:
                    if float(data.loc[date]) < 0.98*float(data.loc[data.index[data.index.get_loc(date) - 1]]):
                        shares += monthly_investment / data.loc[date]
                        current_budget = current_budget - monthly_investment

            portfolio_values.at[date, 'Portfolio Value'] = shares * float(data.loc[date])
            portfolio_values.at[date, 'Total Invested'] = total_investment

        if current_budget > 0:
            print("final budgetttt", current_budget)
            final_price = float(data.iloc[-1])
            shares += current_budget / final_price
            total_investment += current_budget
            # Update the portfolio value for the final date.
            final_date = data.index[-1]
            portfolio_values.at[final_date, 'Portfolio Value'] = shares * final_price
            portfolio_values.at[final_date, 'Total Invested'] = total_investment
    elif strategy == "complexbuythedip":
        # Set fractions for baseline and opportunistic investments
        baseline_fraction = 0.3  # 30% invested on day one of the month
        opport_fraction = 0.7    # 70% available for opportunistic buying

        # Initialize state variables
        current_opport_budget = 0.0  
        current_month = data.index[0].month
        shares = initial_amount / data.iloc[0]  # initial investment at first available price
        total_investment = initial_amount

        # Loop through each date in the dataset
        for date in data.index:
            pos = data.index.get_loc(date)
            
            # New month detected: invest baseline for the month and add new opportunistic funds.
            if pos == 0 or date.month != current_month:
                # If there is leftover opportunistic budget from the previous month, invest it using the last available price.
                if pos > 0 and current_opport_budget > 0:
                    prev_day = data.index[pos - 1]
                    shares += current_opport_budget / data.loc[prev_day]
                    total_investment += current_opport_budget
                    current_opport_budget = 0.0

                # Update the current month tracker.
                current_month = date.month

                # Invest the baseline portion immediately on the first day of the month.
                baseline_investment = baseline_fraction * monthly_investment
                shares += baseline_investment / data.loc[date]
                total_investment += baseline_investment

                # Add the remaining portion of the monthly allocation to the opportunistic budget.
                current_opport_budget += opport_fraction * monthly_investment

            # Opportunistic mechanism: when at least 3 days of data are available,
            # calculate the max price in the rolling window and trigger a buy if current price is 5% below that maximum.
            if pos >= 2 and current_opport_budget > 0:
                # Get the maximum price from the current day and the two previous days.
                rolling_max = data.iloc[pos - 2: pos + 1].max()
                # If the current price is at least 5% below the rolling window maximum, invest the opportunistic budget.
                if float(data.loc[date]) < 0.95 * float(rolling_max):
                    shares += current_opport_budget / data.loc[date]
                    total_investment += current_opport_budget
                    current_opport_budget = 0.0

            # Update the portfolio metrics for the day.
            portfolio_values.at[date, 'Portfolio Value'] = shares * float(data.loc[date])
            portfolio_values.at[date, 'Total Invested'] = total_investment

        # After the loop, if there's any leftover opportunistic budget, invest it on the final day.
        if current_opport_budget > 0:
            final_price = float(data.iloc[-1])
            shares += current_opport_budget / final_price
            total_investment += current_opport_budget
            final_date = data.index[-1]
            portfolio_values.at[final_date, 'Portfolio Value'] = shares * final_price
            portfolio_values.at[final_date, 'Total Invested'] = total_investment

    # Generating Random Value
    shares = initial_amount / first_price
    total_investment = initial_amount
    last_investment_date = data.index[0]
    random.seed(current_seed)
    for date in data.index:
        if date.month != last_investment_date.month:
            available_days = data.index[data.index.month == date.month]
            if not available_days.empty:
                random_day = random.choice(available_days)
                shares += monthly_investment / data.loc[random_day]
                total_investment += monthly_investment
                last_investment_date = random_day
        portfolio_values.at[date, 'Random Value'] = shares * data.loc[date]

    return portfolio_values.index, portfolio_values['Portfolio Value'], portfolio_values['Total Invested'], portfolio_values['Random Value']
