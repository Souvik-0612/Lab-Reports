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
y = y / max(y) * 100


# InflextionPoints_Y = []
# InflextionPoints_X = []
# x0 = 0; y0 = 0
# for i in range(len(x)):
#     if abs(y[i] - y[i-1]) > 12:
#         x0 = x[i-1]
#         y0 = y[i-1]

plt.plot(x, y, "o")
plt.title("Beam Profile")
plt.xlabel("Off Axis [mm]")
plt.ylabel("Inline dose")
plt.show()