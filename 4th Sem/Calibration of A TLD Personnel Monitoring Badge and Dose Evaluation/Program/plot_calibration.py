import numpy as np
import matplotlib.pyplot as plt

# Data from the table
currents = np.array([20, 40, 80, 160, 200])
avg_dose = np.array([0.26, 0.46, 0.93, 1.805, 2.255])

# Create the plot
plt.figure(figsize=(10, 6))
plt.scatter(currents, avg_dose, color='steelblue', label='Experimental Data')

# Fit a line
m, c = np.polyfit(currents, avg_dose, 1)
plt.plot(currents, m*currents + c, color='steelblue', alpha=0.5, linestyle='--', label=f'y = {m:.4f}x + {c:.4f}')

# Formatting
plt.title('Calibration Curve')
plt.xlabel('X Ray tube current (mA)')
plt.ylabel('X-ray dose (mGy)')
plt.xlim(0, 250)
plt.ylim(0, 2.5)
plt.grid(True, linestyle='-', alpha=0.5, color='lightgray')

# Add R^2 value
correlation_matrix = np.corrcoef(currents, avg_dose)
correlation_xy = correlation_matrix[0,1]
r_squared = correlation_xy**2

plt.text(150, 2.1, f'y = {m:.4f}x + {c:.4f}\n$R^2$ = {r_squared:.4f}', fontsize=10, ha='center')

plt.savefig('/Users/souvik/Desktop/Lab-Reports/4th Sem/Calibration of A TLD Personnel Monitoring Badge and Dose Evaluation/Figures/calibration_curve.png', dpi=300, bbox_inches='tight')
print("Plot saved.")
