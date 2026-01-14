##################################################################
### ELECTRICAL ENERGY SYSTEMS STABILITY ANALYSIS            ######
### Analysis: Calculation of Equal Area Criterion using     ######
### numerical integration (trapz) method                    ######
##################################################################

# --- 0. IMPORTING LIBRARIES ---
import numpy as np
from scipy.integrate import odeint

# --- 1. SYSTEM PARAMETERS ---
H = 25.0
Pm = 2.50
delta0 = np.deg2rad(15) # Radians

# Pmax Values
Pmax_pre = Pm / np.sin(delta0)
Pmax_fault = 0
Pmax_post = 0.70 * Pmax_pre

# Critical Parameters
omega_s = 2 * np.pi * 50
tc = 0.21 # Clearing time to be analyzed

# --- 2. FINDING CLEARING ANGLE (Simulation) ---
# First, running a short simulation to find the angle at time tc
def swing_fault(y, t):
    delta, w = y
    Pe = Pmax_fault * np.sin(delta)
    return [w, (omega_s / (2*H)) * (Pm - Pe)]

t_fault = np.linspace(0, tc, 100)
sol = odeint(swing_fault, [delta0, 0], t_fault)
delta_cl = sol[-1, 0] # Angle at clearing time (Radians)
delta_cl_deg = np.rad2deg(delta_cl)

print(f"Clearing Time (tc): {tc} s")
print(f"Clearing Angle (delta_cl): {delta_cl_deg:.2f} Degrees")

# --- 3. CALCULATION OF AREAS (TRAPZ Method) ---

# A1: Accelerating Area (delta0 -> delta_cl)
# Integral: (Pm - Pe_fault) d_delta
d_range1 = np.linspace(delta0, delta_cl, 1000)
Pe_fault_curve = np.zeros_like(d_range1) # Pmax_fault = 0
A1 = np.trapz(Pm - Pe_fault_curve, d_range1)

# A2_max: Available Decelerating Area (delta_cl -> delta_max_theoretical)
# delta_max_theoretical: Unstable point where Pm intersects with Pmax_post (pi - arcsin(...))
delta_max_theo = np.pi - np.arcsin(Pm / Pmax_post)
delta_max_deg = np.rad2deg(delta_max_theo)

# Integral: (Pe_post - Pm) d_delta
d_range2 = np.linspace(delta_cl, delta_max_theo, 1000)
Pe_post_curve = Pmax_post * np.sin(d_range2)
A2_available = np.trapz(Pe_post_curve - Pm, d_range2)

# --- 4. PRINTING RESULTS ---
print("-" * 30)
print(f"Accelerating Area (A1)          : {A1:.4f}")
print(f"Available Decelerating Area (A2): {A2_available:.4f}")
print("-" * 30)

if A2_available > A1:
    print("RESULT: SYSTEM IS STABLE since A2 > A1.")
    margin = A2_available - A1
    print(f"Stability Margin (Energy)       : {margin:.4f}")
else:
    print("RESULT: SYSTEM IS UNSTABLE since A2 < A1.")