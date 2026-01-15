# Python script for NRA edge analysis - ONE REGION AT A TIME
# Finds maximum negative slope (steepest descent point)

# Uses Gaussian Filter for smoothing the data in the ROI

# Script developed with the help of Claude.AI
# Last updated: 09/01/2026

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
from pathlib import Path

# ============= CONFIGURATION =============
data_dir = Path(r"C:\Users\berke\Desktop\IBA\data_analysis\2025-12-Poly-Lysine test")
file_path = data_dir / "A0112000.spca"

# ============= DEFINE YOUR REGION OF INTEREST =============
# Work on ONE region at a time
#REGION_START = 1340
#REGION_END = 1390
REGION_START = 260
REGION_END = 320
REGION_LABEL = "N15_reaction"  # Give it a meaningful name

# Smoothing parameters (only applied to the region of interest)
SMOOTHING_SIGMA = 2     # Gaussian smoothing parameter (higher = more smooth)

# ============= FUNCTIONS =============
def find_max_negative_slope(x, y, region_start, region_end):
    """Find the point of maximum negative slope (steepest descent)"""
    # Extract region
    mask = (x >= region_start) & (x <= region_end)
    x_region = x[mask]
    y_region = y[mask]
    
    if len(x_region) < 10:
        print("⚠ Region too small!")
        return None
    
    # Smooth ONLY the region
    y_smooth = gaussian_filter1d(y_region, sigma=SMOOTHING_SIGMA)
    
    # Calculate derivative (slope)
    dy = np.gradient(y_smooth, x_region)
    
    # Find the most negative slope (steepest descent)
    max_neg_slope_idx = np.argmin(dy)
    max_neg_slope_channel = x_region[max_neg_slope_idx]
    max_neg_slope_value = dy[max_neg_slope_idx]
    
    return {
        'channel': max_neg_slope_channel,
        'slope': max_neg_slope_value,
        'x_region': x_region,
        'y_region': y_region,
        'y_smooth': y_smooth,
        'derivative': dy,
        'idx': max_neg_slope_idx
    }

# ============= LOAD DATA =============
if file_path.suffix == ".spca":
    data = np.loadtxt(file_path)
    filename = file_path.stem
    print(f"✓ Loaded: {filename}")
    print(f"✓ Original file unchanged: {file_path}\n")
else:
    print(f"Error: Expected .spca file, got {file_path.suffix}")
    exit()

x = data[:, 0]
y = data[:, 1]  # RAW data - no smoothing

# ============= ANALYZE REGION =============
print("="*70)
print(f"ANALYZING: {REGION_LABEL}")
print(f"Region: Channels {REGION_START} - {REGION_END}")
print("="*70)

result = find_max_negative_slope(x, y, REGION_START, REGION_END)

if result:
    print(f"\n✓ Maximum negative slope found!")
    print(f"   Channel: {result['channel']:.2f}")
    print(f"   Slope:   {result['slope']:.3f} counts/channel")
    print("\n" + "="*70)
    print(f"📋 RESULT FOR CALIBRATION: Channel = {result['channel']:.2f}")
    print("="*70)
else:
    print("\n✗ Could not find edge in this region")
    exit()

# ============= WINDOW 1: FULL SPECTRUM (RAW DATA) =============
fig1 = plt.figure(figsize=(14, 6))
ax1 = fig1.add_subplot(111)

# Plot RAW data - no smoothing
ax1.plot(x, y, 'b-', linewidth=1, label='Spectrum')
ax1.axhline(0, color='black', linestyle='--', linewidth=0.8, alpha=0.5, label='y=0')

# Highlight the region of interest
ax1.axvspan(REGION_START, REGION_END, alpha=0.3, color='yellow', 
            label=f'Region of Interest: {REGION_LABEL}')

# Mark the detected edge on full spectrum
edge_idx = np.argmin(np.abs(x - result['channel']))
ax1.axvline(result['channel'], color='red', linestyle='--', linewidth=2, 
            alpha=0.7, label=f"Max Neg Slope: {result['channel']:.2f}")
ax1.plot(result['channel'], y[edge_idx], 'r*', markersize=15, zorder=5)

ax1.set_xlabel("Channel", fontsize=12)
ax1.set_ylabel("Counts", fontsize=12)
ax1.set_title(f"{filename} - Full Spectrum (Raw Data)", fontsize=14, fontweight='bold')
ax1.legend(loc='best', fontsize=10)
ax1.grid(True, alpha=0.3)

# ============= WINDOW 2: ZOOMED REGION ANALYSIS (SMOOTHED) =============
fig2 = plt.figure(figsize=(14, 10))

# Top subplot: Raw vs Smoothed spectrum with edge
ax2a = fig2.add_subplot(2, 1, 1)

ax2a.plot(result['x_region'], result['y_region'], 'o', color='lightblue', 
         alpha=0.5, markersize=5, label='Raw Data')
ax2a.plot(result['x_region'], result['y_smooth'], 'b-', linewidth=2.5, 
         label='Smoothed Data (for analysis)')

# Mark the maximum negative slope point
edge_ch = result['channel']
edge_y = result['y_smooth'][result['idx']]

ax2a.axvline(edge_ch, color='red', linestyle='--', linewidth=3, 
            alpha=0.8, label=f'Max Negative Slope')
ax2a.plot(edge_ch, edge_y, 'r*', markersize=20, zorder=5)

# Annotation box
textstr = f"Channel: {edge_ch:.2f}\nSlope: {result['slope']:.3f}"
ax2a.text(0.05, 0.95, textstr, transform=ax2a.transAxes,
         verticalalignment='top', bbox=dict(boxstyle='round', 
         facecolor='yellow', alpha=0.8), fontsize=12, fontweight='bold')

ax2a.set_xlabel("Channel", fontsize=12)
ax2a.set_ylabel("Counts", fontsize=12)
ax2a.set_title(f"{REGION_LABEL} - Spectrum and Edge Detection", 
              fontsize=13, fontweight='bold')
ax2a.legend(loc='best', fontsize=10)
ax2a.grid(True, alpha=0.3)
ax2a.set_xlim(REGION_START, REGION_END)

# Bottom subplot: Derivative (slope)
ax2b = fig2.add_subplot(2, 1, 2)

ax2b.plot(result['x_region'], result['derivative'], 'purple', linewidth=2, 
         label='Derivative (slope)')
ax2b.axhline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)

# Mark the maximum negative slope
ax2b.axvline(edge_ch, color='red', linestyle='--', linewidth=3, alpha=0.8)
ax2b.plot(edge_ch, result['slope'], 'r*', markersize=20, zorder=5,
         label=f'Max Negative Slope: {result["slope"]:.3f}')

ax2b.set_xlabel("Channel", fontsize=12)
ax2b.set_ylabel("Slope (dY/dX)", fontsize=12)
ax2b.set_title("Derivative - Steepest Descent = Most Negative Point", 
              fontsize=13, fontweight='bold')
ax2b.legend(loc='best', fontsize=10)
ax2b.grid(True, alpha=0.3)
ax2b.set_xlim(REGION_START, REGION_END)

fig2.tight_layout()

# Show both windows
plt.show()

print(f"\n✓ Analysis complete for {REGION_LABEL}")
print(f"✓ Use channel {result['channel']:.2f} for your calibration curve")
