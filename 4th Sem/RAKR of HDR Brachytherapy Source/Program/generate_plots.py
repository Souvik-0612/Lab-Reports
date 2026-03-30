import numpy as np
import matplotlib.pyplot as plt

# Data for Dwell Position vs Current
dwell_pos = np.array([131.9, 131.4, 130.9, 130.4, 129.9, 129.4, 128.9, 128.4, 127.9, 127.4, 126.9, 126.4, 125.9, 125.4, 124.9, 124.4, 123.9, 123.4, 122.9, 122.4, 121.9])
current = np.array([44.033, 45.63, 47.08, 48.34, 49.37, 50.19, 50.815, 51.242, 51.49, 51.56, 51.48, 51.22, 50.79, 50.16, 49.33, 48.25, 46.91, 45.25, 43.26, 40.91, 38.24])

# Plot 1: Sweet Spot
plt.figure(figsize=(10, 6))
plt.plot(dwell_pos, current, marker='o', linestyle='-', color='b')
plt.title('Well Chamber Sweet Spot: Current vs Dwell Position')
plt.xlabel('Dwell Position (cm)')
plt.ylabel('Current (nA)')
plt.grid(True)
plt.axvline(x=127.4, color='r', linestyle='--', label='Sweet Spot (127.4 cm)')
plt.legend()
plt.gca().invert_xaxis() # Usually dwell positions decrease as it goes deeper
plt.savefig('/Users/souvik/Desktop/Lab-Reports/4th Sem/RAKR of HDR Brachytherapy Source/Figures/sweet_spot_plot.png', dpi=300, bbox_inches='tight')
plt.close()

# Data for Time Linearity
set_time = np.array([60, 120, 180, 240, 300])
measured_time = np.array([60.27, 120.24, 180.20, 240.19, 300.23])

# Fit line
m, c = np.polyfit(set_time, measured_time, 1)

# Plot 2: Time Linearity
plt.figure(figsize=(10, 6))
plt.scatter(set_time, measured_time, color='red', label='Data points')
plt.plot(set_time, m*set_time + c, color='blue', label=f'Fit: y = {m:.4f}x + {c:.4f}')
plt.title('Time Linearity and End Error')
plt.xlabel('Set Time (sec)')
plt.ylabel('Measured Time (sec)')
plt.grid(True)
plt.legend()
plt.savefig('/Users/souvik/Desktop/Lab-Reports/4th Sem/RAKR of HDR Brachytherapy Source/Figures/time_linearity_plot.png', dpi=300, bbox_inches='tight')
plt.close()

print("Plots generated successfully.")
