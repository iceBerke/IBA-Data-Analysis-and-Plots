# Python script used to plot SPCC data for manual channel selection
# Logarithmic scale

# Script developed with the help of Claude.AI
# Last updated: 08/01/2026

import numpy as np
import matplotlib.pyplot as plt
import mplcursors
from matplotlib.widgets import Cursor
from pathlib import Path

data_dir = Path(r"C:\Users\berke\Desktop\IBA\data_analysis\2025-12-Poly-Lysine test")
file_path = data_dir / "A0112003.spcc"

# Check extension before loading
if file_path.suffix == ".spcc":
    data = np.loadtxt(file_path)
    filename = file_path.stem
    print(f"Loaded {filename}")
else:
    print(f"Error: Expected .spcc file, got {file_path.suffix}")
    exit()

x = data[:, 0]
y = data[:, 1]

fig, ax = plt.subplots()
ax.plot(x, y, label='Spectrum')

# Set logarithmic scale for y-axis
ax.set_yscale('log')

# Draw y=0 line (Note: won't be visible on log scale since log(0) is undefined)
# ax.axhline(0, color='black', linestyle='--', linewidth=0.8, alpha=0.7, label='y=0')

plt.xlabel("Channel")
plt.ylabel("Counts (log scale)")
plt.title(f"{filename} - SPCC Data")
plt.legend()
plt.grid(True, alpha=0.3)

plt.xlim(360,400)
#plt.xlim(585,605)

mplcursors.cursor(hover=True)
plt.show()
