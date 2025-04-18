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
        linewidths=0.5
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
        palette="CMRmap",
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
import matplotlib.pyplot as plt
import seaborn as sns

def plot_mean_final_value_per_strategy():
    # Load dataset
    df = pd.read_csv("investment_simulation_results.csv")

    # Define strategies and their corresponding labels
    strategies = [
        "first",
        "losing",
        "growing",
        "buythedip",
        "0.98buythedip",
        "complexbuythedip"
    ]

    strategy_labels = {
        "first": "Dollar-Cost Averaging",
        "losing": "Losing Streak",
        "growing": "Momentum Snap-In",
        "buythedip": "5% Buy-The-Dip",
        "0.98buythedip": "Complex 2% Drop Buy-The-Dip",
        "complexbuythedip": "Hybrid Buy-The-Dip",
        "random": "Random Strategy"
    }

    # List to hold the combined data
    combined_data = []

    # Process each strategy
    for strategy in strategies:
        strat_avg = (
            df[df["Strategy"] == strategy]
            .groupby(["Scenario"])["Final Value"]
            .mean()
            .reset_index()
            .rename(columns={"Final Value": "Average Final Value"})
        )
        strat_avg["Type"] = strategy
        combined_data.append(strat_avg)

    # Process the random strategy
    rand_avg = (
        df.groupby(["Scenario"])["Random Final"]
        .mean()
        .reset_index()
        .rename(columns={"Random Final": "Average Final Value"})
    )
    rand_avg["Type"] = "random"
    combined_data.append(rand_avg)

    # Combine all data
    combined = pd.concat(combined_data, ignore_index=True)

    # Map strategy names to labels
    combined["Type"] = combined["Type"].map(strategy_labels)

    # Plot
    plt.figure(figsize=(14, 8))
    ax = sns.barplot(
        data=combined,
        x="Scenario",
        y="Average Final Value",
        hue="Type",
        palette="Set2"
    )

    # Aesthetics
    plt.title("Average Final Value per Strategy and Scenario", fontsize=14)
    plt.ylabel("Average Final Portfolio Value", fontsize=12)
    plt.xlabel("Scenario", fontsize=12)
    plt.legend(title="Strategy", bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
    plt.tight_layout()
    plt.show()

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def get_scenario_avg_heatmap_excluding():
    # Load the data
    df = pd.read_csv("strategy_success_rates.csv")

    # Optional: Clean asset names
    df["Asset"] = df["Asset"].replace({
        "^GSPC": "S&P500",
        "^IXIC": "NASDAQ",
        "GC=F": "Gold"
    })

    # Exclude 'buythedip' and 'losing' strategies
    df = df[~df["Strategy"].isin(["5% Buy-The-Dip", "Complex 2% Buy-The-Dip"])]

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
        annot_kws={"size": 10}
    )

    # Aesthetics
    plt.title("Average Success Rate per Scenario (Excluding Zero Success Strategies)", fontsize=12)
    plt.yticks([], [])  # Hide y-axis since it's just a single row
    plt.xlabel("Scenario", fontsize=10)
    plt.tight_layout()

    # Show the heatmap
    plt.show()

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_avg_earnings_per_scenario_excluding():
    # Load the dataset
    df = pd.read_csv("investment_simulation_results.csv")  # use your actual file name

    # Rename asset codes for readability
    df["Asset"] = df["Asset"].replace({
        "^GSPC": "S&P500",
        "^IXIC": "NASDAQ",
        "GC=F": "Gold"
    })

    # Exclude 'buythedip' and 'losing' strategies
    df = df[~df["Strategy"].isin(["buythedip", "0.98buythedip"])]

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
    plt.title("Average Earnings per Scenario: Strategy vs Random (Excluding Zero Success Strategies)", fontsize=14)
    plt.ylabel("Average Final Portfolio Value", fontsize=12)
    plt.xlabel("Scenario", fontsize=12)
    plt.legend(title="Type", loc="best")
    plt.tight_layout()

    # Show it
    plt.show()
