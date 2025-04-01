import pandas as pd

def calculate_value(portfolio_dates, total_invested):
    # Load the Excel file
    data = pd.read_excel("data/IPC_1961_to_2025.xlsx")  # Ensure the file path is correct

    # Ensure the column names match the actual Excel structure
    data.columns = ['Año', 'Mes', 'Inflation_Rate']  # Adjust column names if needed

    # Convert portfolio_dates to a DataFrame
    inflation_values = pd.DataFrame(index=portfolio_dates, columns=['Adjusted Value'])
    inflation_values['Adjusted Value'] = total_invested  # Start with initial investment

    # Iterate over the portfolio dates
    for date in portfolio_dates:
        for _, row in data.iterrows():  # Loop through the inflation data
            if date.month == row['Mes'] and date.year == row['Año']:
                # Adjust investment based on inflation
                inflation_values.loc[date, 'Adjusted Value'] *= (1 - row['Inflation_Rate'])

    return inflation_values
