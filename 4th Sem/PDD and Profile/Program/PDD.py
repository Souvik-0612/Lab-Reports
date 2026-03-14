# Importing some useful library
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scienceplots
plt.style.use(['science', 'notebook', 'grid'])

# Data Extraction from the xlsx file
df = pd.read_excel("PDD and Profile/Program/PDD & PROFILE.xlsx", sheet_name=1)
x = np.array(df["Depth"])
y = np.array(df["Depth dose"])

# Percentage depth dose
PDD = y/max(y)*100

# To find the surface PD(Percentage dose), dmax, D10(Dose at 10 cm depth), D20
# variable initilization
SPD = 0 # surface PD
dmax = 0; D10 = 0;D20 = 0
for i in range(len(PDD)):
    if PDD[i] == 100:
        dmax = x[i]
    if x[i] == 0:
        SPD = PDD[i]
    if x[i] == 100: # 100 mm
        D10 = PDD[i]
    if x[i] == 200: # 200 mm
        D20 = PDD[i]
        

#Plotting
plt.figure(figsize=(15, 8))
plt.title(r"PDD profile of 10MV SSD=100, Water Phantom, F.S= 10x10cm$^2$", fontsize=20)
plt.plot(x, PDD)
bbox = dict(boxstyle="round", fc="0.8")
plt.scatter([0, dmax, 100, 200], [SPD, 100, D10, D20], color='red', zorder=3)
plt.annotate(f"Surface PD: {SPD:.2f}%", xy=(0, SPD), xytext=(25, SPD + 8),bbox=bbox,
             arrowprops=dict(arrowstyle="->", lw=1.5), fontsize=11)
plt.annotate(f"Dmax: {dmax:.2f} mm", xy=(dmax, 100), xytext=(dmax + 20, 95),bbox=bbox,
             arrowprops=dict(arrowstyle="->", lw=1.5), fontsize=11)
plt.annotate(f"PD10: {D10:.2f}%", xy=(100, D10), xytext=(120, D10 + 8),bbox=bbox,
             arrowprops=dict(arrowstyle="->", lw=1.5), fontsize=11)
plt.annotate(f"PD20: {D20:.2f}%", xy=(200, D20), xytext=(220, D20 + 8),bbox=bbox,
             arrowprops=dict(arrowstyle="->", lw=1.5), fontsize=11)
plt.ylabel("PDD(%)")
plt.xlabel("Depth(mm)")
plt.savefig("PDD and Profile/Program/PDD_10MV.pdf", dpi=300, bbox_inches='tight')
plt.show()