# Importing some useful library
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scienceplots
plt.style.use(['science', 'notebook', 'grid'])

# Data Extraction from the xlsx file
df = pd.read_excel("PDD and Profile/Program/PDD & PROFILE.xlsx", sheet_name=2)
x = np.array(df["Distance from central axis"])
Ix = np.array(df["Inline dose value"]) #Change the column name (Inline dose value or Crossline dose value)"
Ix=Ix/max(Ix)*100   

#Analyzing profile data
xleft = 0; xright = 0    # To find the FWHM(Full width at half maximum) of the inline profile
for i in range(int(len(x)/2)):
    if abs(Ix[i]-50) <= 5:
        xleft = x[i]
    if abs(Ix[-i]-50) <= 5:
        xright = x[-i]
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

n = int(len(IIx)/2)
AreaL = IIx[0]+2*sum(IIx[1:n-1])+IIx[n]             #Trapezoidal rule for area calculation of the left half of the profile
AreaR = IIx[n+1]+2*sum(IIx[n+1:-1])+IIx[-1]
perSymmetry = (AreaL - AreaR)/(AreaL+AreaR)*100
perFlatness = (Dmax - Dmin)/(Dmax+Dmin)*100
LeftPenumbra = xL[-1] - xL[0] if len(xL) > 1 else float('nan')
RightPenumbra = xR[-1] - xR[0] if len(xR) > 1 else float('nan')



#Plotting
fig, ax = plt.subplots(figsize=(15, 8))
ax.set_title(r"10MV, Beam Profile(Inline), SSD=100CM, F.S=10X10 cm$^2$, Depth=10cm", fontsize=20)
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
plt.savefig("PDD and Profile/Program/InlineProfile.pdf", dpi=300, bbox_inches='tight')
plt.show()