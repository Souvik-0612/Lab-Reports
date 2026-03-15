# Importing some useful library
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
import scienceplots
plt.style.use(['science', 'notebook', 'grid'])

# Data Extraction from the xlsx file
base_dir = Path(__file__).resolve().parent
excel_file = base_dir / "PDD & PROFILE.xlsx"
df = pd.read_excel(excel_file, sheet_name=2)
x = np.array(df["Distance from central axis"])
Ix = np.array(df["Crossline dose value"]) #Change the column name (Inline dose value or Crossline dose value)"
Ix=Ix/max(Ix)*100   

#Analyzing profile data
xleft = 0; xright = 0    # To find the FWHM(Full width at half maximum) of the inline profile
for i in range(int(len(x)/2)):
    if 55 >= Ix[i] >=45:
        xleft = x[i] - (x[i]-x[i-1])*(Ix[i]-50)/(Ix[i]-Ix[i-1])     #Linear interpolation
    if 55 >= Ix[-i]>=45:
        xright = x[-i] - (x[-i]-x[-i+1])*(Ix[-i]-50)/(Ix[-i]-Ix[-i+1])


FieldWidth = xright - xleft # Geometrical field width


Dmax = 0; Dmin = 100
IIx = []
xR = []; leftPenumbra = []; xL = []; rightPenumbra = []
for i in range(len(x)):
    if abs(x[i]) <= 0.4*FieldWidth:
        if Dmax < Ix[i]:
            Dmax = Ix[i]
        if Dmin > Ix[i]:
            Dmin = Ix[i]

    if abs(x[i])<= FieldWidth/2:
        IIx.append(Ix[i])

    if i < int(len(x)/2) and 17 <= Ix[i] <= 83:
        xL.append(x[i])
        leftPenumbra.append(Ix[i])
    if i > int(len(x)/2) and 17 <= Ix[i] <= 83:
        xR.append(x[i])
        rightPenumbra.append(Ix[i])

n = int(len(IIx)/2); h = abs(x[1]-x[0]) # Step size for numerical integration
AreaL = 0.5*h*(IIx[0]+2*sum(IIx[1:n])+IIx[n])             #Trapezoidal rule for area calculation of the left half of the profile
AreaR = 0.5*h*(IIx[n+1]+2*sum(IIx[n+1:-1])+IIx[-1])
perSymmetry = abs((AreaL - AreaR)/(AreaL+AreaR)*100)
perFlatness = abs((Dmax - Dmin)/(Dmax+Dmin)*100)
LeftPenumbra = abs(xL[-1] - xL[0]) # Left penumbra width
RightPenumbra = abs(xR[-1] - xR[0]) # Right penumbra width


#Plotting
fig, ax = plt.subplots(figsize=(15, 8))
ax.plot(x, Ix)
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
    f"Symmetry: {perSymmetry:.2f} %\n"
    f"Flatness: {perFlatness:.2f} %\n"
    f"Left penumbra: {LeftPenumbra:.2f} mm\n"
    f"Right penumbra: {RightPenumbra:.2f} mm"
)
ax.text(0.02, 0.98, info_text, transform=ax.transAxes, va='top', ha='left',
        fontsize=11, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='black'))
ax.set_xlabel("Distance from central axis (mm)")
ax.set_ylabel("Relative dose (%)")
plt.savefig(base_dir / "CrosslineProfile.pdf", dpi=300, bbox_inches='tight')
plt.show()