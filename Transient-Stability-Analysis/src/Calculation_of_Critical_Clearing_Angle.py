##################################################################
### ELECTRICAL ENERGY SYSTEMS STABILITY ANALYSIS            ######
### Analysis: Calculation of Critical Clearing Angle        ######
##################################################################

# --- 0. IMPORTING LIBRARIES ---
import numpy as np

# --- 1. PARAMETERS ---
Pm = 2.50
delta0_deg = 15
delta0 = np.deg2rad(delta0_deg)

# Power Values
Pmax_pre = Pm / np.sin(delta0)
Pmax_fault = 0
Pmax_post = 0.70 * Pmax_pre

# --- 2. CRITICAL ANGLE CALCULATION (Numerical) ---
# Step 1: Maximum Swing Angle (delta_max)
# delta_max = 180 - arcsin(Pm / Pmax_post)
delta_max_rad = np.pi - np.arcsin(Pm / Pmax_post)

# Step 2: Critical Clearing Angle (delta_cr)
# Formula: cos(d_cr) = [Pm*(d_max - d0) + Pmax3*cos(d_max)] / Pmax3
numerator = Pm * (delta_max_rad - delta0) + Pmax_post * np.cos(delta_max_rad)
denominator = Pmax_post
cos_delta_cr = numerator / denominator

delta_cr_rad = np.arccos(cos_delta_cr)
delta_cr_deg = np.rad2deg(delta_cr_rad)

# --- 3. PRINTING RESULTS ---
print("-" * 40)
print(f"CALCULATION RESULTS (G3 Parameters)")
print("-" * 40)
print(f"Maximum Swing Angle (delta_max): {np.rad2deg(delta_max_rad):.4f} Degrees")
print(f"Critical Clearing Angle (delta_cr) : {delta_cr_deg:.4f} Degrees")
print("-" * 40)