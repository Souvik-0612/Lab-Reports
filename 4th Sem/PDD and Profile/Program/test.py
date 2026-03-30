# Importing some useful library
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import scienceplots
plt.style.use(['science', 'notebook', 'grid'])

# Data Extraction from the xlsx file
df = pd.read_excel("PROFILE Group 2.xlsx", sheet_name=1)
x = np.array(df["Off Axis [mm]"])
y = np.array(df["Inline dose"])
y = y / y[x==0] * 100

# interpolation
f = interp1d(x, y, kind='cubic')
xnew = np.linspace(x[0], x[-1], num=10000, endpoint=True)
ynew = f(xnew)

#Data analysis

# Pnumbra lateral distance between 20% and 80% dose
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
center_idx = np.argmin(np.abs(xnew))

# Left side from center outward (toward negative x)
left_x = xnew[:center_idx + 1][::-1]
left_y = ynew[:center_idx + 1][::-1]

# Right side from center outward (toward positive x)
right_x = xnew[center_idx:]
right_y = ynew[center_idx:]

# Left and right 80% and 20% positions
x80_left = find_crossing_x(left_x, left_y, 80)
x20_left = find_crossing_x(left_x, left_y, 20)
x80_right = find_crossing_x(right_x, right_y, 80)
x20_right = find_crossing_x(right_x, right_y, 20)

# Penumbra width = lateral distance between 80% and 20% dose
left_penumbra = abs(x20_left - x80_left)
right_penumbra = abs(x20_right - x80_right)

print(f"Left penumbra (80%-20%): {left_penumbra:.3f} mm")
print(f"Right penumbra (80%-20%): {right_penumbra:.3f} mm")




# Plotting the data
plt.figure(figsize=(10, 6))
plt.plot(x, y, "o")     #, label='Data Points'
plt.plot(xnew, ynew)    #, label='Cubic Spline Interpolation'
plt.title('Beam Profile')
plt.xlabel('Off Axis [mm]')
plt.ylabel('Inline dose [%]')

# Shade penumbra area under the curve (between 80% and 20% crossing points)
left_mask = (xnew >= min(x80_left, x20_left)) & (xnew <= max(x80_left, x20_left))
right_mask = (xnew >= min(x80_right, x20_right)) & (xnew <= max(x80_right, x20_right))

plt.fill_between(xnew[left_mask], ynew[left_mask], 0, color='tab:orange', alpha=0.35, label='Left penumbra area')
plt.fill_between(xnew[right_mask], ynew[right_mask], 0, color='tab:green', alpha=0.35, label='Right penumbra area')

# Optional markers for 80% and 20% crossing points on each side
plt.scatter([x80_left, x20_left, x80_right, x20_right], [80, 20, 80, 20], color='red', zorder=3)

plt.legend()
plt.show()