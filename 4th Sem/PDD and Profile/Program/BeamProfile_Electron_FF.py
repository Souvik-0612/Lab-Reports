# Importing some useful library
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import scienceplots
plt.style.use(['science', 'notebook', 'grid'])

# Data Extraction from the xlsx file
df = pd.read_excel("PROFILE Group 2.xlsx", sheet_name=3)
x = np.array(df["Off Axis [mm]"])
y = np.array(df["Inline dose"])
y = y / y[x==0] * 100


#Data analysis 
x50L = 0; x50R = 0; x80L = 0; x80R = 0; I80R = []; I80L = []; x90L = 0; x90R = 0
n = int(len(x)/2)

for i in range(len(x)):
    #Geometric field size
    if y[i] > 50:
        x50L = x[i] + ((x[i] - x[i-1])/(y[i] - y[i-1]))*(50 - y[i])
    if y[-i] > 50:
        x50R = x[-i] + ((x[-i] - x[-i-1])/(y[-i] - y[-i-1]))*(50 - y[-i])
        break

FieldWidth = x50R - x50L
flatnessL = x90L - x50L; flatnessR = x90R - x50R
flatness = (flatnessL + flatnessR)/2

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
center_idx = np.argmin(np.abs(x))

# Left side from center outward (toward negative x)
left_x = x[:center_idx + 1][::-1]
left_y = y[:center_idx + 1][::-1]

# Right side from center outward (toward positive x)
right_x = x[center_idx:]
right_y = y[center_idx:]

# Left and right 80% and 20% positions
x80_left = find_crossing_x(left_x, left_y, 80)
x20_left = find_crossing_x(left_x, left_y, 20)
x80_right = find_crossing_x(right_x, right_y, 80)
x20_right = find_crossing_x(right_x, right_y, 20)

# Penumbra width = lateral distance between 80% and 20% dose
left_penumbra = abs(x20_left - x80_left)
right_penumbra = abs(x20_right - x80_right)



y50 = y[y > 50]
n = int(len(y50)/2); h = abs(x[1] - x[0])
AreaL = 0.5*h*(y50[0] + y50[n] + 2*sum(y50[1:n]))
AreaR = 0.5*h*(y50[n+1] + y50[-1] + 2*sum(y50[n+1:-1]))
Symmetry = abs(AreaL - AreaR)/(AreaL + AreaR) * 100


print("Flatness: ", flatness)
print("Symmetry: ", Symmetry)
print(f"Left penumbra (80%-20%): {left_penumbra:.3f} mm")
print(f"Right penumbra (80%-20%): {right_penumbra:.3f} mm")




#Plotting
fig, ax = plt.subplots(figsize=(15, 8))
ax.plot(x, y, label="Beam Profile")
plt.plot([-FieldWidth/2, FieldWidth/2], [50, 50], color='red', linestyle='--', label='50% Line')
plt.plot([-FieldWidth/2, -FieldWidth/2], [0, 102], color='green', linestyle='--')
plt.plot([FieldWidth/2, FieldWidth/2], [0, 102], color='green', linestyle='--')
plt.plot([0, 0], [0, 105], color='blue', linestyle='--')
plt.plot([0.4*FieldWidth, 0.4*FieldWidth], [0, 102], color='orange', linestyle='--')
plt.plot([-0.4*FieldWidth, -0.4*FieldWidth], [0, 102], color='orange', linestyle='--')
info_text = (
    f"Field size: {FieldWidth:.2f} mm\n"
    f"Symmetry: {Symmetry:.2f} %\n"
    f"Flatness: {flatness:.2f} %\n"
    f"Left penumbra: {left_penumbra:.2f} mm\n"
    f"Right penumbra: {right_penumbra:.2f} mm"
)

ax.text(0.02, 0.98, info_text, transform=ax.transAxes, va='top', ha='left',
        fontsize=11, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='black'))
ax.set_xlabel("Distance from central axis (mm)")
ax.set_ylabel("Relative dose (%)")
plt.savefig("Figures/Profile/6MeV(10 by 10)/InlineProfile.pdf", dpi=300, bbox_inches='tight')
plt.show()