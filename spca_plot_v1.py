# Python script used to plot SPCA data for manual channel selection

# Script developed with the help of Claude.AI
# Last updated: 09/01/2026

import numpy as np
import matplotlib.pyplot as plt
import mplcursors
from matplotlib.widgets import Cursor
from pathlib import Path

data_dir = Path(r"C:\Users\berke\Desktop\IBA\data_analysis\2025-12-Poly-Lysine test")
file_path = data_dir / "A0112000.spca"

# Check extension before loading
if file_path.suffix == ".spca":
    data = np.loadtxt(file_path)
    filename = file_path.stem
    print(f"Loaded {filename}")
else:
    print(f"Error: Expected .spca file, got {file_path.suffix}")
    exit()

x = data[:, 0]
y = data[:, 1]

fig, ax = plt.subplots()
ax.plot(x, y, label='Spectrum')

# Draw y=0 line
ax.axhline(0, color='black', linestyle='--', linewidth=0.8, alpha=0.7, label='y=0')

plt.xlabel("Channel")
plt.ylabel("Counts")
plt.title(f"{filename} - SPCA Data")
plt.legend()

#plt.xlim(0, 200)      # set x limits
#plt.ylim(0, 1e5)       # set y limits

mplcursors.cursor(hover=True)
plt.show()

