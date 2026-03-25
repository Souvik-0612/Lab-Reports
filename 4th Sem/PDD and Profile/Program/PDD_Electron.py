# Importing some useful library
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scienceplots
plt.style.use(['science', 'notebook', 'grid'])

# Data Extraction from the xlsx file
df = pd.read_excel("PDD Group 2.xlsx", sheet_name=3)
x = np.array(df["Depth[mm]"])
y = np.array(df["Depth dose"])

# Percentage depth dose
PDD = y/max(y)*100

# To find the surface PD(Percentage dose), dmax, D10(Dose at 10 cm depth), D20
# variable initilization
SPD = 0 # surface PD
dmax = 0; x90 = 0; x50 = 0; PDD90 = 0; PDD50 = 0; PDDm = 0; xm = 0
for i in range(len(PDD)):
    if x[i] == 0:
        SPD = PDD[i]

    if PDD[i] == 100:
        dmax = x[i]
    
    if PDD[i] > 90:
        x90 = x[i] + ((x[i-1] - x[i])/(PDD[i-1] - PDD[i]))*(90 - PDD[i]) # Straight line interpolation
    if PDD[i] > 80:
        x80 = x[i] + ((x[i-1] - x[i])/(PDD[i-1] - PDD[i]))*(80 - PDD[i]) # Straight line interpolation
    if PDD[i] > 50:
        x50 = x[i] + ((x[i-1] - x[i])/(PDD[i-1] - PDD[i]))*(50 - PDD[i]) # Straight line interpolation
        PDD50 = PDD[i]
        m = (PDD[i] - PDD[i-1])/(x[i] - x[i-1])

    if abs(PDD[i]- PDD[i-1]) > 0.01:
        xm = x[i]; PDDm = PDD[i]
        

xx = np.linspace(15, 32, 1000)
yy = PDD50 + m*(xx - x50)
c1 = PDD50 - m*x50
c2 = PDDm
xp = (c2 - c1)/m
xq = (100 - c1)/m 



#Plotting
plt.figure(figsize=(15, 8))
plt.title(r"PDD profile of 6 MeV SSD=100, Water Phantom, F.S= 10x10cm$^2$", fontsize=20)
plt.plot(x, PDD)
plt.plot(xx, yy)

plt.plot(x[0], PDD[0], "o") #Surface PDD
plt.plot(dmax, 100, "o") # Dmax
plt.plot([0, x50], [100, 100], "k", alpha=0.35)

plt.plot([0, x90], [90, 90], "k", alpha=0.35)
plt.plot([x90, x90], [0, 90], "k", alpha=0.35)
plt.plot([x90], [90], "o") #R90


plt.plot([0, x80], [80, 80], "k", alpha=0.35)
plt.plot([x80, x80], [0, 80], "k", alpha=0.35)
plt.plot([x80], [80], "o") #R80

plt.plot([0, x50], [50, 50], "k", alpha=0.35)
plt.plot([x50, x50], [0, 50], "k", alpha=0.35)
plt.plot([x50], [50], "o") #R50

plt.plot([0, xm, x[-1]], [PDDm, PDDm, PDDm], "k", alpha=0.35)
plt.plot([xp], [PDDm], "o") #Rp

plt.plot([xq], [100], "o") #Rq

surface_label = f"Surface PDD ({PDD[0]:.2f})%"
dmax_label = f"dmax ({dmax:.2f} mm)"
x90_label = f"R90 ({x90:.2f} mm)"
x80_label = f"R80 ({x80:.2f} mm)"
x50_label = f"R50 ({x50:.2f} mm)"
xp_label = f"Rp ({xp:.2f} mm)"
xq_label = f"Rq ({xq:.2f} mm)"

plt.annotate(surface_label, xy=(x[0], PDD[0]), xytext=(x[0] , PDD[0] -10),
             arrowprops=dict(arrowstyle="->", lw=1.0), fontsize=11)
plt.annotate(dmax_label, xy=(dmax, 100), xytext=(dmax - 3.0, 105.0),
             arrowprops=dict(arrowstyle="->", lw=1.0), fontsize=11)
plt.annotate(x90_label, xy=(x90, 90), xytext=(x90 + 2.0, 94.0),
             arrowprops=dict(arrowstyle="->", lw=1.0), fontsize=11)
plt.annotate(x80_label, xy=(x80, 80), xytext=(x80 + 2.0, 84.0),
             arrowprops=dict(arrowstyle="->", lw=1.0), fontsize=11)
plt.annotate(x50_label, xy=(x50, 50), xytext=(x50 + 2.0, 54.0),
             arrowprops=dict(arrowstyle="->", lw=1.0), fontsize=11)
plt.annotate(xp_label, xy=(xp, PDDm), xytext=(xp + 2.0, PDDm + 10.0),
             arrowprops=dict(arrowstyle="->", lw=1.0), fontsize=11)
plt.annotate(xq_label, xy=(xq, 100), xytext=(xq + 2.0, 103.0),
             arrowprops=dict(arrowstyle="->", lw=1.0), fontsize=11)

plt.ylabel("PDD(%)")
plt.xlabel("Depth(mm)")
plt.savefig("Figures/PDD/PDD_6MeV_Electron.pdf", dpi=300, bbox_inches='tight')
plt.show()