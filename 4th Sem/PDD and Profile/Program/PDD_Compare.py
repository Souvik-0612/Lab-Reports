# Importing some useful library
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scienceplots
plt.style.use(['science', 'notebook', 'grid'])

# Data Extraction from the xlsx file
df0 = pd.read_excel("PDD and Profile/Program/PDD & PROFILE.xlsx", sheet_name=0)
df1 = pd.read_excel("PDD and Profile/Program/PDD & PROFILE.xlsx", sheet_name=1)
x0 = np.array(df0["Depth"])
y0 = np.array(df0["Depth dose"])
x1 = np.array(df1["Depth"])
y1 = np.array(df1["Depth dose"])

# Percentage depth dose
PDD0 = y0/max(y0)*100
PDD1 = y1/max(y1)*100

#Plotting
plt.figure(figsize=(15, 8))
plt.title(r"Comparison of PDD profiles of 6MV and 10MV", fontsize=20)
plt.plot(x0, PDD0, label="6MV")
plt.plot(x1, PDD1, label="10MV")
plt.legend()
plt.ylabel("PDD(%)")
plt.xlabel("Depth(mm)")
plt.savefig("PDD and Profile/Program/PDD_Compare.pdf", dpi=300, bbox_inches='tight')
plt.show()