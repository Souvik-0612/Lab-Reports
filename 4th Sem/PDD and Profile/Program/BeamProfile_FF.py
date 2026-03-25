# Importing some useful library
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scienceplots
plt.style.use(['science', 'notebook', 'grid'])

# Data Extraction from the xlsx file
df = pd.read_excel("PROFILE Group 2.xlsx", sheet_name=1)
x = np.array(df["Off Axis [mm]"])
y = np.array(df["Inline dose"])
y = y / max(y) * 100

#Data analysis 
x50L = 0; x50R = 0; x80L = 0; x80R = 0; I80R = []; I80L = []
n = int(len(x)/2)
for i in range(len(x)):
    #Geometric field size
    if y[i] > 50:
        x50L = x[i] + ((x[i] - x[i-1])/(y[i] - y[i-1]))*(50 - y[i])
    if y[-i] > 50:
        x50R = x[-i] + ((x[-i] - x[-i-1])/(y[-i] - y[-i-1]))*(50 - y[-i])
        break

FieldWidth = x50R - x50L

Dmax = 0; Dmin = 100
xR = []; leftPenumbra = []; xL = []; rightPenumbra = []; IIx = []
for i in range(len(x)):
    # Flatness
    if abs(x[i]) <= 0.4*FieldWidth:
        if Dmax < y[i]:
            Dmax = y[i]
        if Dmin > y[i]:
            Dmin = y[i]
    # Penumbra
    if i < int(len(x)/2) and 17 <= y[i] <= 83:
        xL.append(x[i])
        leftPenumbra.append(y[i])
    if i > int(len(x)/2) and 17 <= y[i] <= 83:
        xR.append(x[i])
        rightPenumbra.append(y[i])

LeftPenumbra = abs(xL[-1] - xL[0]) # Left penumbra width
RightPenumbra = abs(xR[-1] - xR[0]) # Right penumbra width


y50 = y[y > 50]
n = int(len(y50)/2); h = abs(x[-1] - x[0])
AreaL = 0.5*h*(y50[0] + y50[n] + 2*sum(y50[1:n]))
AreaR = 0.5*h*(y50[n+1] + y50[-1] + 2*sum(y50[n+1:-1]))
Symmetry = abs(AreaL - AreaR)/(AreaL + AreaR) * 100



flatness = (Dmax - Dmin) / (Dmax + Dmin) * 100
print("Flatness: ", flatness)
print("Symmetry: ", Symmetry)
print("Left Penumbra: ", LeftPenumbra)
print("Right Penumbra: ", RightPenumbra)




#Plotting
fig, ax = plt.subplots(figsize=(15, 8))
ax.plot(x, y)
plt.fill_between(xL, leftPenumbra, 0, color='lightcoral', alpha=0.35)
plt.fill_between(xR, rightPenumbra, 0, color='skyblue', alpha=0.35)
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
    f"Left penumbra: {LeftPenumbra:.2f} mm\n"
    f"Right penumbra: {RightPenumbra:.2f} mm"
)
ax.text(0.02, 0.98, info_text, transform=ax.transAxes, va='top', ha='left',
        fontsize=11, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='black'))
ax.set_xlabel("Distance from central axis (mm)")
ax.set_ylabel("Relative dose (%)")
plt.savefig("Figures/Profile/InlineProfile.pdf", dpi=300, bbox_inches='tight')
plt.show()