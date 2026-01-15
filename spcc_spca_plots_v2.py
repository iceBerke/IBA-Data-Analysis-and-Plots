# Python script for NRA edge analysis - ONE REGION AT A TIME
# Finds maximum negative slope (steepest descent point)

# Based on spca_plot_v5 (also uses Savitzky-Golay filter)
# Meant for spcc and spca files (no difference between them anyways 
# in terms of file structure)
# WITH UNCERTAINTY ESTIMATION 

# Script developed with the help of Claude.AI
# Last updated: 09/01/2026

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from pathlib import Path

# ============= CONFIGURATION =============
data_dir = Path(r"C:\Users\berke.santos\Documents\CEMHTI\IBA\Analysis\2025-12-Poly-Lysine test\Raw_Data")
file_path = data_dir / "A0112000.spca"

# ============= DEFINE YOUR REGION OF INTEREST =============
# Work on ONE region at a time
#REGION_START = 1340
#REGION_END = 1390
REGION_START = 260
REGION_END = 320
REGION_LABEL = "N15_reaction"  # Give it a meaningful name

# Smoothing parameters (Savitzky-Golay filter - only applied to region)
SMOOTHING_WINDOW = 11    # Main window size (must be odd number)
SMOOTHING_ORDER = 3      # Polynomial order (2 or 3 typically work well)

# Uncertainty estimation - test multiple window sizes
TEST_WINDOWS = [9, 11, 13]  # Will test stability across these window sizes

# ============= FUNCTIONS =============
def validate_savgol_params(window, order, n_points):
    """Validate Savitzky-Golay filter parameters"""
    errors = []
    
    # Check if window is odd
    if window % 2 == 0:
        errors.append(f"Window size must be odd (currently {window}). Try {window+1} or {window-1}")
    
    # Check if window is smaller than data
    if window > n_points:
        errors.append(f"Window size ({window}) must be <= number of points ({n_points})")
        errors.append(f"Either increase your region size or decrease window size to {n_points if n_points % 2 == 1 else n_points-1}")
    
    # Check if polyorder is less than window
    if order >= window:
        errors.append(f"Polynomial order ({order}) must be < window size ({window}). Try order={window-1}")
    
    return errors

def find_max_negative_slope(x, y, region_start, region_end, window_size, poly_order, verbose=False):
    """Find the point of maximum negative slope (steepest descent)"""
    # Extract region
    mask = (x >= region_start) & (x <= region_end)
    x_region = x[mask]
    y_region = y[mask]
    
    n_points = len(x_region)
    
    if n_points < 10:
        if verbose:
            print(f"⚠ Region too small! Only {n_points} points found.")
            print(f"   Need at least 10 points for analysis.")
        return None
    
    # Validate Savitzky-Golay parameters
    param_errors = validate_savgol_params(window_size, poly_order, n_points)
    
    if param_errors:
        if verbose:
            print("❌ SAVITZKY-GOLAY PARAMETER ERROR:")
            for error in param_errors:
                print(f"   • {error}")
        return None
    
    # Smooth ONLY the region using Savitzky-Golay filter
    y_smooth = savgol_filter(y_region, window_length=window_size, polyorder=poly_order)
    
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

# ============= UNCERTAINTY ESTIMATION =============
print("="*70)
print(f"ANALYZING: {REGION_LABEL}")
print(f"Region: Channels {REGION_START} - {REGION_END}")
print("="*70)
print("\n🔍 Testing stability across different smoothing parameters...")
print(f"Testing window sizes: {TEST_WINDOWS}")
print("-"*70)

edge_channels = []
valid_windows = []

for window in TEST_WINDOWS:
    result_test = find_max_negative_slope(x, y, REGION_START, REGION_END, 
                                          window, SMOOTHING_ORDER, verbose=False)
    if result_test:
        edge_channels.append(result_test['channel'])
        valid_windows.append(window)
        marker = "←" if window == SMOOTHING_WINDOW else " "
        print(f"   Window={window:2d}: Channel {result_test['channel']:.1f}  {marker}")
    else:
        print(f"   Window={window:2d}: Failed")

if len(edge_channels) < 2:
    print("\n❌ Not enough valid results for uncertainty estimation.")
    print("   Try adjusting TEST_WINDOWS or region size.")
    exit()

# Calculate statistics
mean_channel = np.mean(edge_channels)
std_channel = np.std(edge_channels)
min_channel = np.min(edge_channels)
max_channel = np.max(edge_channels)
spread = max_channel - min_channel

print("-"*70)
print(f"\n📊 UNCERTAINTY ANALYSIS:")
print(f"   Mean channel:     {mean_channel:.2f}")
print(f"   Std deviation:    {std_channel:.2f} channels")
print(f"   Range:            {min_channel:.1f} - {max_channel:.1f} (spread = {spread:.1f})")

# Assess confidence
if spread <= 1.0:
    confidence = "HIGH ✓"
    message = "Edge position is very stable - high confidence result!"
elif spread <= 2.0:
    confidence = "GOOD"
    message = "Edge position is reasonably stable."
elif spread <= 3.0:
    confidence = "MODERATE ⚠"
    message = "Some variability detected. Consider checking region boundaries."
else:
    confidence = "LOW ⚠⚠"
    message = "High variability! Check: noisy data, poor region choice, or weak edge."

print(f"   Confidence:       {confidence}")
print(f"   Assessment:       {message}")

# ============= MAIN ANALYSIS WITH PRIMARY WINDOW =============
print("\n" + "="*70)
print(f"PRIMARY ANALYSIS (Window={SMOOTHING_WINDOW})")
print("="*70)

result = find_max_negative_slope(x, y, REGION_START, REGION_END, 
                                 SMOOTHING_WINDOW, SMOOTHING_ORDER, verbose=True)

if result:
    print(f"\n✓ Maximum negative slope found!")
    print(f"   Channel: {result['channel']:.2f}")
    print(f"   Slope:   {result['slope']:.3f} counts/channel")
    print("\n" + "="*70)
    print(f"📋 RESULT FOR CALIBRATION:")
    print(f"   Channel = {result['channel']:.1f} ± {std_channel:.1f}")
    print("="*70)
else:
    print("\n✗ Analysis failed. Please check the error messages above.")
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
            alpha=0.7, label=f"Max Neg Slope: {result['channel']:.1f} ± {std_channel:.1f}")
ax1.plot(result['channel'], y[edge_idx], 'r*', markersize=15, zorder=5)

# Show uncertainty range
if spread > 0:
    ax1.axvspan(min_channel, max_channel, alpha=0.2, color='red', 
                label=f'Uncertainty range')

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
         label=f'Smoothed Data (Window={SMOOTHING_WINDOW})')

# Mark the maximum negative slope point
edge_ch = result['channel']
edge_y = result['y_smooth'][result['idx']]

ax2a.axvline(edge_ch, color='red', linestyle='--', linewidth=3, 
            alpha=0.8, label=f'Max Negative Slope')
ax2a.plot(edge_ch, edge_y, 'r*', markersize=20, zorder=5)

# Show uncertainty range
if spread > 0:
    ax2a.axvspan(min_channel, max_channel, alpha=0.2, color='red', 
                label=f'±{std_channel:.1f} ch uncertainty')

# Annotation box
textstr = f"Channel: {edge_ch:.1f} ± {std_channel:.1f}\nSlope: {result['slope']:.3f}\nConfidence: {confidence}"
ax2a.text(0.05, 0.95, textstr, transform=ax2a.transAxes,
         verticalalignment='top', bbox=dict(boxstyle='round', 
         facecolor='yellow', alpha=0.8), fontsize=11, fontweight='bold')

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

# Show uncertainty range
if spread > 0:
    ax2b.axvspan(min_channel, max_channel, alpha=0.2, color='red')

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
print(f"✓ Use channel {result['channel']:.1f} ± {std_channel:.1f} for your calibration curve")
