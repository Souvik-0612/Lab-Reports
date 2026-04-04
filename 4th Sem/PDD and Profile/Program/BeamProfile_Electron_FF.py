# Importing some useful library
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline

import scienceplots
plt.style.use(['science', 'notebook', 'grid'])

# Data Extraction from the xlsx file
df = pd.read_excel("PROFILE Group 2.xlsx", sheet_name=3)
x = np.array(df["Off Axis [mm]"])
y = np.array(df["Inline dose"])

center_idx = np.argmin(np.abs(x))
y = y / y[center_idx] * 100

# Sort data for interpolation and robust crossing detection.
sort_idx = np.argsort(x)
x = x[sort_idx]
y = y[sort_idx]

spline = CubicSpline(x, y)
x_dense = np.linspace(x.min(), x.max(), 4000)
y_dense = spline(x_dense)


# Analysis helpers
def find_crossing_x(side_x, side_y, level):
	"""Return x-position where profile crosses a given dose level."""
	for i in range(len(side_y) - 1):
		y1, y2 = side_y[i], side_y[i + 1]
		if (y1 >= level and y2 <= level) or (y1 <= level and y2 >= level):
			if y2 == y1:
				return side_x[i]
			return side_x[i] + (level - y1) * (side_x[i + 1] - side_x[i]) / (y2 - y1)
	raise ValueError(f"No crossing found for {level}% dose level.")


# Split profile around central axis (x ~= 0)
center_idx = np.argmin(np.abs(x))

# Left side from center outward (toward negative x)
left_x = x[:center_idx + 1][::-1]
left_y = y[:center_idx + 1][::-1]

# Right side from center outward (toward positive x)
right_x = x[center_idx:]
right_y = y[center_idx:]

# Field size: lateral separation between 50% dose points.
x50_left = find_crossing_x(left_x, left_y, 50)
x50_right = find_crossing_x(right_x, right_y, 50)
FieldWidth = abs(x50_right - x50_left)

# Beam flatness: separation between 90% and 50% dose points on each side.
x90_left = find_crossing_x(left_x, left_y, 90)
x90_right = find_crossing_x(right_x, right_y, 90)
flatness_left = abs(x50_left - x90_left)
flatness_right = abs(x90_right - x50_right)
flatness_avg = 0.5 * (flatness_left + flatness_right)

# Penumbra lateral distance between 20% and 80% dose.
x80_left = find_crossing_x(left_x, left_y, 80)
x20_left = find_crossing_x(left_x, left_y, 20)
x80_right = find_crossing_x(right_x, right_y, 80)
x20_right = find_crossing_x(right_x, right_y, 20)

# Penumbra width = lateral distance between 80% and 20% dose
left_penumbra = abs(x20_left - x80_left)
right_penumbra = abs(x20_right - x80_right)

# Symmetry: maximum ratio of absorbed doses at symmetrical points more than 1 cm inside the 90% contour.
symmetry_half_width = min(abs(x90_left), abs(x90_right)) - 10.0
if symmetry_half_width <= 0:
    symmetry_half_width = 0.5 * min(abs(x90_left), abs(x90_right))

symmetry_x = np.linspace(0, symmetry_half_width, 600)
sym_left = np.interp(-symmetry_x, x, y)
sym_right = np.interp(symmetry_x, x, y)
sym_ratio = np.maximum(sym_left / sym_right, sym_right / sym_left)
Symmetry = float(np.max(sym_ratio))


#Plotting
fig, ax = plt.subplots(figsize=(15, 8))
ax.plot(x, y, label="Beam Profile")
ax.plot(x_dense, y_dense, color='tab:blue', linewidth=1.5, alpha=0.75)
plt.plot([x50_left, x50_right], [50, 50], color='red', linestyle='--', label='50% Line')
plt.plot([x50_left, x50_left], [0, 102], color='green', linestyle='--')
plt.plot([x50_right, x50_right], [0, 102], color='green', linestyle='--')
plt.plot([0, 0], [0, 105], color='blue', linestyle='--')

# Flatness markers at 90% and 50% dose points.
plt.plot([x90_left, x90_right], [90, 90], marker='o', color='orange', linestyle='None')
plt.plot([x50_left, x50_right], [50, 50], marker='o', color='red', linestyle='None')

# Penumbra markers at 80% and 20% dose points.
plt.plot([x80_left, x80_right], [80, 80], marker='s', color='magenta', linestyle='None')
plt.plot([x20_left, x20_right], [20, 20], marker='s', color='magenta', linestyle='None')


# Annotations.
plt.annotate(
	f"Field size = {FieldWidth:.2f} mm",
	xy=(0.5 * (x50_left + x50_right), 50),
	xytext=(0, 18),
	textcoords='offset points',
	ha='center',
	fontsize=11,
	bbox=dict(boxstyle='round,pad=0.25', facecolor='white', alpha=0.9, edgecolor='black', linewidth=0.8),
)

info_text = (
    f"Field size: {FieldWidth:.2f} mm\n"
	f"Flatness L/R: {flatness_left:.2f} / {flatness_right:.2f} mm\n"
	f"Symmetry: {Symmetry:.3f}\n"
    f"Left penumbra: {left_penumbra:.2f} mm\n"
    f"Right penumbra: {right_penumbra:.2f} mm"
)

ax.text(0.02, 0.98, info_text, transform=ax.transAxes, va='top', ha='left',
        fontsize=11, bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.9, edgecolor='black'))
ax.set_xlabel("Distance from central axis (mm)")
ax.set_ylabel("Relative dose (%)")
plt.savefig("Figures/Profile/6MeV(10 by 10)/InlineProfile.pdf", dpi=300, bbox_inches='tight')
plt.show()