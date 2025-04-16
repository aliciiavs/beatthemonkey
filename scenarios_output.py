import pandas as pd

# Load your CSV
df = pd.read_csv("investment_simulation_results.csv")

# Ensure the numeric columns are treated as such (just in case)
df["Final Value"] = pd.to_numeric(df["Final Value"], errors='coerce')
df["Random Final"] = pd.to_numeric(df["Random Final"], errors='coerce')

# Drop rows with missing or invalid data in comparison columns
df = df.dropna(subset=["Final Value", "Random Final"])

# Create a new column to indicate success (1 if Final > Random, else 0)
df["Success"] = (df["Final Value"] > df["Random Final"]).astype(int)

# Group by Scenario, Asset, Strategy and calculate mean success (proportion)
result = df.groupby(["Scenario", "Asset", "Strategy"])["Success"].mean().reset_index()

# Optional: Rename the column for clarity
result.rename(columns={"Success": "Proportion Final > Random"}, inplace=True)

# Save the result to a new CSV
result.to_csv("no_name_strategy_success_rates.csv", index=False)

# Print the result
print(result)
