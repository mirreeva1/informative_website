import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV data into a DataFrame
df = pd.read_csv("data/processed/cleaned.csv", sep=";")

# Filter the DataFrame for the year 2024
df_2024 = df[df["Edition"] == 2024]

# Convert the "Total" column to numeric values
df_2024["Total"] = pd.to_numeric(df_2024["Total"], errors="coerce")

# Sort the DataFrame by the "Total" column in descending order
df_sorted = df_2024.sort_values(by="Total", ascending=False)

# Select the top 10 rows
top_10 = df_sorted.head(10)

# Create a bubble chart
fig, ax = plt.subplots(figsize=(12, 8))

# Set the background color of the chart
fig.patch.set_facecolor("#f5f5f5")

# Create bubbles for each country
bubbles = ax.scatter(top_10.index, top_10["Total"], s=top_10["Total"]*50, alpha=0.8, cmap="viridis")

# Set the labels and title
ax.set_xlabel("Country")
ax.set_ylabel("Total Score")
ax.set_title("Top 10 Freest Countries in 2024")

# Set the x-axis labels to the country names
ax.set_xticks(top_10.index)
ax.set_xticklabels(top_10["Country"], rotation=45, ha="right")

# Add a color bar
cbar = fig.colorbar(bubbles, ax=ax, orientation="vertical", shrink=0.8)
cbar.set_label("Total Score")

# Add labels for each bubble
for i, (country, total) in enumerate(zip(top_10["Country"], top_10["Total"])):
    ax.text(i, total, f"{country}\n{total:.1f}", ha="center", va="center", fontsize=10)

plt.tight_layout()
plt.show()