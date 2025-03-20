import pyodbc
import pandas as pd
import random
from datetime import datetime, timedelta
import yfinance as yf
from sqlalchemy import create_engine
from simulate_investment import simulate_investment

# Define your connection details here
def create_connection():
    try:
        # Establish connection to SQL Server
        connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'+
                                     'Server=LAPTOP-K7M6RL21;'+
                                     'Database=finance;'+
                                     'Trusted_Connection=Yes')
        connection.autocommit = True
        print("Connection successful!")
        return connection
    except pyodbc.Error as ex:
        print('Connection failed:', ex)
        return None

# Function to generate and insert preset results into the database
def generate_preset_results():
    connection = create_connection()
    if not connection:
        return

    cursor = connection.cursor()

    # Step 1: Check if the Presets table has any data
    cursor.execute("SELECT COUNT(*) FROM Presets")
    preset_count = cursor.fetchone()[0]

    if preset_count == 0:
        print("No presets found in the database. Please add some preset data manually.")
        return

    # Step 2: Fetch preset configurations from the database
    cursor.execute("SELECT Preset_ID, Start_Year, Stock, Initial_Investment, Monthly_Investment, Strategy FROM Presets")
    presets = cursor.fetchall()

    # Step 3: Recalculate investment results for each preset configuration
    new_results = []
    today = datetime.now().date()

    for preset in presets:
        preset_id, start_year, stock, initial, monthly, strategy = preset

        # Calculate start date based on the number of years
        start_date = datetime(today.year - start_year, today.month, today.day)  # Example start date
        end_date = today

        # Use your existing simulate_investment function
        dates, portfolio_value, total_invested = simulate_investment(stock, initial, monthly, strategy, start_year)

        # Print the results to ensure they are being returned correctly
        print(f"Results for {stock} with strategy {strategy}: {dates}, {portfolio_value}, {total_invested}")

        # Step 4: Store the results in a list for bulk insertion
        for date, value, invested in zip(dates, portfolio_value, total_invested):
            new_results.append((date, preset_id, invested, value))

    # Step 5: Insert the calculated data into the SQL table
    if new_results:
        try:
            cursor.executemany(
                "INSERT INTO Preset_Results (Date, Preset_ID, Total_Invested, Total_Earned) VALUES (?, ?, ?, ?)",
                new_results
            )
            print("New data inserted successfully.")
        except pyodbc.Error as ex:
            print("Error inserting data:", ex)
        finally:
            connection.commit()  # Commit the changes to the database

    connection.close()

# Run this function every night to refresh the data
generate_preset_results()
