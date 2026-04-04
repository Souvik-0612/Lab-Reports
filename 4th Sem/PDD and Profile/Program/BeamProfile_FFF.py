# Importing some useful library
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scienceplots
plt.style.use(['science', 'notebook', 'grid'])

# Data Extraction from the xlsx file
df = pd.read_excel("PROFILE Group 2.xlsx", sheet_name=2)
x = np.array(df["Off Axis [mm]"])
y = np.array(df["Inline dose"])
y = y / y[x ==0] * 100

IPy = []; IPx = []
for i in range(len(x)-1):
    if abs(y[i+1] - y[i]) > 4:
        IPx.append(x[i])
        IPy.append(y[i])
IPy = np.array(IPy); IPx = np.array(IPx)
IPx_neg = IPx[IPx < 0]
IPy_neg = IPy[IPx < 0]

IPx_pos = IPx[IPx > 0]
IPy_pos = IPy[IPx > 0]
print(sum(IPx_neg)/len(IPx_neg), sum(IPy_neg)/len(IPy_neg))
print(sum(IPx_pos)/len(IPx_pos), sum(IPy_pos)/len(IPy_pos))

plt.plot(x, y, "o")
plt.plot(IPx_neg, IPy_neg, "ro")
plt.plot(IPx_pos, IPy_pos, "go")
# plt.plot(sum(IPx_neg)/len(IPx_neg), sum(IPy_neg)/len(IPy_neg), "ro")
plt.title("Beam Profile")
plt.xlabel("Off Axis [mm]")
plt.ylabel("Inline dose")
plt.show()