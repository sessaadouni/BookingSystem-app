import matplotlib.pyplot as plt # type: ignore
import pandas as pd

# Data from performance reports
small_data = {
  "Group": ["JSON", "MONGO_JSON", "MongoDB", "REDIS_JSON"],
  "Average_CPU_Usage": [12.03, 5.77, 16.27, 14.34],
  "Average_Memory_Used": [0.00, 0.06, 0.06, 0.06],
}

big_data = {
  "Group": ["MONGO_JSON", "MongoDB", "REDIS_JSON"],
  "Average_CPU_Usage": [8.41, 9.30, 11.17],
  "Average_Memory_Used": [25.49, 0.81, 25.72],
}

# Create a DataFrame
df = pd.DataFrame(big_data)

# Plot CPU and Memory Usage by Group
plt.figure(figsize=(14, 10))

# Subplot 1: CPU Usage
plt.subplot(2, 1, 1)
bars = plt.bar(df["Group"], df["Average_CPU_Usage"], color='blue', alpha=0.7)
plt.title("Average CPU Usage by Group")
plt.ylabel("CPU Usage (%)")
plt.xticks(rotation=45, ha='right')

# Add percentages on top of bars
for bar in bars:
  height = bar.get_height()
  plt.text(bar.get_x() + bar.get_width() / 2.0, height, f"{height:.2f}%", ha='center', va='bottom')

# Subplot 2: Memory Usage
plt.subplot(2, 1, 2)
bars = plt.bar(df["Group"], df["Average_Memory_Used"], color='green', alpha=0.7)
plt.title("Average Memory Usage by Group")
plt.xlabel("Group")
plt.ylabel("Memory Usage (MB)")
plt.xticks(rotation=45, ha='right')

# Add memory usage values on top of bars
for bar in bars:
  height = bar.get_height()
  plt.text(bar.get_x() + bar.get_width() / 2.0, height, f"{height:.2f} MB", ha='center', va='bottom')

# Adjust layout and save plot
plt.tight_layout()
plt.savefig('resources_comparison_global_metrics.png', dpi=300)
plt.show()
