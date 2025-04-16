import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def get_heatmap():
    # Load your data
    df = pd.read_csv("strategy_success_rates.csv")

    # Optional: Rename assets for readability
    df["Asset"] = df["Asset"].replace({"^GSPC": "S&P500", "^IXIC": "NASDAQ", "GC=F": "Gold"})

    # Pivot for heatmap: rows = Strategy, columns = Scenario, values = Success Rate
    pivot_table = df.pivot_table(
        index=["Strategy", "Asset"],
        columns="Scenario",
        values="Beats the Random in what %?"
    )

    # Plot the heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(
        pivot_table, 
        annot=True, 
        fmt=".2f", 
        cmap="YlGnBu", 
        vmin=0, 
        vmax=1, 
        linewidths=0.5,
        annot_kws={"size": 8}  # smaller text inside boxes
    )

    # Plot aesthetics
    plt.title("Heatmap: Strategy Success Rate by Scenario and Asset", fontsize=12)
    plt.ylabel("Strategy & Asset", fontsize=10)
    plt.xlabel("Scenario", fontsize=10)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.tight_layout()

    # Show it
    plt.show()

def get_barchart():
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt

    # Load your results CSV
    df = pd.read_csv("strategy_success_rates.csv")

    # Rename columns for clarity in plot
    df.rename(columns={"Beats the Random in what %?": "Success Rate"}, inplace=True)

    # Optional: Make asset names prettier if needed
    df["Asset"] = df["Asset"].replace({"^GSPC": "S&P500", "^IXIC": "NASDAQ", "GC=F": "Gold"})
    df["Strategy (Asset)"] = df["Strategy"] + " (" + df["Asset"] + ")"

    # Check for duplicates and remove them
    df = df.drop_duplicates()

    # In case there are still multiple rows with the same combination of Scenario and Strategy, 
    # aggregate them by taking the mean of the Success Rate.
    df = df.groupby(["Scenario", "Strategy"])["Success Rate"].mean().reset_index()

    # Create bar plot
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=df,
        x="Scenario",
        y="Success Rate",
        hue="Strategy",
        palette="viridis",
        errorbar=None
    )

    # Plot aesthetics
    plt.title("How Often Each Strategy Beats the Random Baseline")
    plt.ylabel("Success Rate of Beating Random")
    plt.ylim(0, 1)
    plt.legend(title="Strategy")
    plt.tight_layout()

    # Show the plot
    plt.show()

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def get_scenario_avg_heatmap():
    # Load the data
    df = pd.read_csv("strategy_success_rates.csv")

    # Optional: Clean asset names
    df["Asset"] = df["Asset"].replace({
        "^GSPC": "S&P500",
        "^IXIC": "NASDAQ",
        "GC=F": "Gold"
    })

    # Rename column for clarity
    df.rename(columns={"Beats the Random in what %?": "Success Rate"}, inplace=True)

    # Group by Scenario only and take mean success rate
    scenario_avg = df.groupby("Scenario")["Success Rate"].mean().reset_index()

    # Turn it into a format suitable for heatmap (1 row, multiple columns)
    pivot = scenario_avg.pivot_table(index=None, columns="Scenario", values="Success Rate")

    # Plot heatmap
    plt.figure(figsize=(10, 1.5))  # Make it short since it’s a 1-row heatmap
    sns.heatmap(
        pivot,
        annot=True,
        fmt=".2f",
        cmap="YlOrRd",
        vmin=0,
        vmax=1,
        linewidths=0.5,
        palette="viridis",
        annot_kws={"size": 10}
    )

    # Aesthetics
    plt.title("Average Success Rate per Scenario", fontsize=12)
    plt.yticks([], [])  # Hide y-axis since it's just a single row
    plt.xlabel("Scenario", fontsize=10)
    plt.tight_layout()

    # Show the heatmap
    plt.show()


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_avg_earnings_per_scenario():
    # Load the dataset
    df = pd.read_csv("investment_simulation_results.csv")  # use your actual file name

    # Rename asset codes for readability
    df["Asset"] = df["Asset"].replace({
        "^GSPC": "S&P500",
        "^IXIC": "NASDAQ",
        "GC=F": "Gold"
    })

    # Compute average final value (earnings) per scenario for strategy and random
    strategy_avg = df.groupby("Scenario")["Final Value"].mean().reset_index()
    random_avg = df.groupby("Scenario")["Random Final"].mean().reset_index()

    # Rename columns to merge easily
    strategy_avg.rename(columns={"Final Value": "Average Final Value"}, inplace=True)
    random_avg.rename(columns={"Random Final": "Average Final Value"}, inplace=True)

    # Add a column to distinguish them
    strategy_avg["Type"] = "Strategy"
    random_avg["Type"] = "Random"

    # Combine into one DataFrame
    combined = pd.concat([strategy_avg, random_avg])

    # Plot
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(
        data=combined,
        x="Scenario",
        y="Average Final Value",
        hue="Type",
        palette="viridis"
    )
    for container in ax.containers:
        ax.bar_label(container, fmt="%.2f", padding=3, fontsize=9)

    # Aesthetics
    plt.title("Average Earnings per Scenario: Strategy vs Random", fontsize=14)
    plt.ylabel("Average Final Portfolio Value", fontsize=12)
    plt.xlabel("Scenario", fontsize=12)
    plt.legend(title="Type", loc="best")
    plt.tight_layout()

    # Show it
    plt.show()

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_mean_final_value_per_asset():
    # Load dataset
    df = pd.read_csv("investment_simulation_results.csv")

    # Clean asset names
    df["Asset"] = df["Asset"].replace({
        "^GSPC": "S&P500",
        "^IXIC": "NASDAQ",
        "GC=F": "Gold"
    })

    # --- STRATEGY average per Scenario and Asset ---
    strat_avg = (
        df.groupby(["Scenario", "Asset"])["Final Value"]
        .mean()
        .reset_index()
        .rename(columns={"Final Value": "Average Final Value"})
    )
    strat_avg["Type"] = "Strategy"

    # --- RANDOM average per Scenario and Asset ---
    rand_avg = (
        df.groupby(["Scenario", "Asset"])["Random Final"]
        .mean()
        .reset_index()
        .rename(columns={"Random Final": "Average Final Value"})
    )
    rand_avg["Type"] = "Random"

    # Combine both
    combined = pd.concat([strat_avg, rand_avg], ignore_index=True)

    # Create a label to differentiate bars by both Type and Asset
    combined["Label"] = combined["Asset"] + " (" + combined["Type"] + ")"

    # Plot
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(
        data=combined,
        x="Scenario",
        y="Average Final Value",
        hue="Label",
        palette="Set2"
    )

    # Aesthetics
    plt.title("Average Final Value per Asset and Scenario (Strategy vs Random)", fontsize=14)
    plt.ylabel("Average Final Portfolio Value", fontsize=12)
    plt.xlabel("Scenario", fontsize=12)
    plt.legend(title="Asset (Type)", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

plot_mean_final_value_per_asset()
