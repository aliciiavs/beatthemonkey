import pandas as pd
from tqdm import tqdm
from simulate_investment import simulate_investment  # Adjust this import as needed

# Define simulation scenarios
scenarios = {
    'A': {"initial": 100, "monthly": 100, "years": 2},
    'B': {"initial": 2000, "monthly": 250, "years": 2},
    'C': {"initial": 2000, "monthly": 250, "years": 15},
    'D': {"initial": 100, "monthly": 100, "years": 15},
}

# Define strategies to test
strategies = [
    "first",
    "losing",
    "growing",
    "buythedip",
    "0.98buythedip",
    "complexbuythedip"
]

# Define assets to test
assets = ["^GSPC","^IXIC", "GC=F"]

# Simulation configuration
num_seeds = 100
results = []

# Loop through each combination of Scenario, Strategy, and Asset
for scenario_name, params in tqdm(scenarios.items(), desc="Scenarios"):
    for strategy in tqdm(strategies, leave=False, desc="Strategies"):
        for asset in assets:
            for seed in range(1, num_seeds + 1):
                try:
                    idx, portfolio_values, total_invested, random_values = simulate_investment(
                        stock=asset,
                        initial_amount=params["initial"],
                        monthly_investment=params["monthly"],
                        strategy=strategy,
                        years=params["years"],
                        current_seed=seed
                    )
                    final_date = idx[-1].date()
                    final_value = portfolio_values.iloc[-1]
                    total_inv = total_invested.iloc[-1]
                    random_final = random_values.iloc[-1]
                    
                    results.append({
                        "Scenario": scenario_name,
                        "Asset": asset,
                        "Strategy": strategy,
                        "Seed": seed,
                        "Final Date": final_date,
                        "Final Value": round(final_value, 2),
                        "Total Invested": round(total_inv, 2),
                        "Random Final": round(random_final, 2)
                    })
                except Exception as e:
                    results.append({
                        "Scenario": scenario_name,
                        "Asset": asset,
                        "Strategy": strategy,
                        "Seed": seed,
                        "Error": str(e)
                    })

# Convert results to DataFrame and save as CSV
df_results = pd.DataFrame(results)
csv_path = "investment_simulation_results.csv"
df_results.to_csv(csv_path, index=False)
print(f"✅ All done. Results saved to {csv_path}")
