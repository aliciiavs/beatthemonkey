import pandas as pd
import matplotlib.pyplot as plt
import os


def calculate_value(portfolio_dates, initial_investment, monthly_investment):
    """
    Adjusts the invested value over time based on monthly inflation rates using the formula:
    
    New Value = Previous Value * (1 - Inflation Rate) + Monthly Investment
    
    This function assumes:
    - portfolio_dates is an iterable of dates (e.g. business days)
    - initial_investment is the amount invested on the first date.
    - monthly_investment is added on the first business day of each new month.
    
    The inflation data is loaded from an Excel file ("IPC_1961_to_2025.xlsx", sheet "IPC_change")
    which has columns: 'Año', 'Mes', 'Inflation_Rate'.
    (If the inflation rate is given as a percentage, convert it to a decimal.)
    
    Returns:
      pd.DataFrame: A DataFrame with Date, Total Invested, and Adjusted Value.
    """
    # Get the current working directory where the script is running
    current_directory = os.getcwd()

    # Automatically construct the full path to the file
    file_path = os.path.join(current_directory, "data", "IPC_1961_to_2025.xlsx")

    # Now, use the file path
    data = pd.read_excel(file_path, sheet_name="IPC_change")

    # Load the inflation data
    data.columns = ['Año', 'Mes', 'Inflation_Rate']
    
    # If inflation rates are given as percentages, uncomment this line:
    # data['Inflation_Rate'] = data['Inflation_Rate'] / 100
    
    # Create a DataFrame for the portfolio dates and the constant total invested (initial investment for every date)
    portfolio_df = pd.DataFrame({'Date': portfolio_dates})
    portfolio_df['Total Invested'] = [initial_investment] * len(portfolio_dates)
    portfolio_df['Adjusted Value'] = None
    
    # Extract year and month for merging with inflation data
    portfolio_df['Año'] = portfolio_df['Date'].dt.year
    portfolio_df['Mes'] = portfolio_df['Date'].dt.month

    # Sort by date
    portfolio_df = portfolio_df.sort_values('Date').reset_index(drop=True)
    
    # Initialize the adjusted value on the first day
    current_value = initial_investment
    portfolio_df.loc[0, 'Adjusted Value'] = current_value
    
    # Loop through the dates starting from the second date
    for i in range(1, len(portfolio_df)):
        current_date = portfolio_df.loc[i, 'Date']
        prev_date = portfolio_df.loc[i-1, 'Date']
        
        # By default, keep current value for days that are not the first business day of a new month.
        new_value = current_value

        # Check if this is the first day of a new month compared to the previous day
        if current_date.month != prev_date.month:
            # Increase the total invested by the monthly investment
            portfolio_df.loc[i, 'Total Invested'] = portfolio_df.loc[i-1, 'Total Invested'] + monthly_investment
            # Get the inflation rate for the current month
            infl_row = data[(data['Año'] == current_date.year) & (data['Mes'] == current_date.month)]
            rate = infl_row['Inflation_Rate'].iloc[0] if not infl_row.empty else 0
            rate = rate/100
            # Apply the formula: New Value = (Previous Value * (1 - rate)) + monthly_investment
            new_value = current_value * (1 - rate) + monthly_investment
        else:
            # If not a new month, carry over the previous Total Invested value
            portfolio_df.loc[i, 'Total Invested'] = portfolio_df.loc[i-1, 'Total Invested']
        
        # Update the current value and record in DataFrame
        current_value = new_value
        portfolio_df.loc[i, 'Adjusted Value'] = new_value

    return portfolio_df[['Date', 'Total Invested', 'Adjusted Value']]
