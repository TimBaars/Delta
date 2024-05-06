import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data into a DataFrame
data = pd.read_csv('robot_speeds_times.csv')

# Sort data by weight to ensure consistent coloring and grouping in the plot
data.sort_values('Weight (kg)', inplace=True)

# Create a line plot
plt.figure(figsize=(10, 6))
for label, grp in data.groupby('Weight (kg)'):
    # Sort the group by speed to ensure the line plot makes sense
    grp = grp.sort_values('Speed (mm/s)')
    plt.plot(grp['Speed (mm/s)'], grp['Time (seconds)'], marker='o', label=f'{label} kg')

plt.xlabel('Speed (mm/s)')
plt.ylabel('Time (seconds)')
plt.title('Robot Performance by Speed and Weight')
plt.legend(title='Payload Weight')
plt.grid(True)
plt.show()
