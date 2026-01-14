##################################################################
### ELECTRICAL ENERGY SYSTEMS STABILITY ANALYSIS            ######
### Analysis: Generator-3 (G3) Time Domain Simulation       ######
##################################################################

# --- 0. IMPORTING LIBRARIES ---
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# --- 1. SYSTEM PARAMETERS (From Manual Calculations) ---
S_base = 100        # MVA
f = 50              # Hz
omega_s = 2 * np.pi * f # Synchronous Angular Speed (314.16 rad/s)

# G3 Parameters
H = 25.0            # s
Pm = 2.50           # pu
delta0_deg = 15     # Degrees
delta0 = np.deg2rad(delta0_deg) # Radians

# Power Transfer Capabilities (Pmax)
# Pre-Fault: Back-calculated from Pm = Pmax * sin(delta0)
Pmax_pre = Pm / np.sin(delta0)  # ~9.66 pu
Pmax_fault = 0                  # During Fault (Solid Short Circuit)
Pmax_post = 0.70 * Pmax_pre     # Post-Fault (70% Capacity)

# Time Definitions
t_final = 2.0
t_steps = np.linspace(0, t_final, 2000) # 2000 steps for resolution

# --- 2. SWING EQUATION FUNCTION ---
def swing_equation(y, t, tc):
    delta, omega_dev = y
    
    # Electrical Power (Pe) Selection based on State
    if t < 0:
        Pe = Pmax_pre * np.sin(delta) # Pre-Fault
    elif t <= tc:
        Pe = Pmax_fault * np.sin(delta) # During Fault (Pe=0)
    else:
        Pe = Pmax_post * np.sin(delta)  # Post-Fault (Line Opened)
        
    # State Equations
    # d(delta)/dt = omega_dev
    # d(omega)/dt = (omega_s / 2H) * (Pm - Pe)
    d_delta = omega_dev
    d_omega = (omega_s / (2 * H)) * (Pm - Pe)
    
    return [d_delta, d_omega]

# --- 3. SIMULATION (ODEINT SOLUTION) ---
y0 = [delta0, 0] # Initial Conditions [Angle, Speed Deviation]

# Case 1: tc = 0.12 s (Fast Protection)
tc1 = 0.12
sol1 = odeint(swing_equation, y0, t_steps, args=(tc1,))
delta1_deg = np.rad2deg(sol1[:, 0])

# Case 2: tc = 0.21 s (Backup Protection)
tc2 = 0.21
sol2 = odeint(swing_equation, y0, t_steps, args=(tc2,))
delta2_deg = np.rad2deg(sol2[:, 0])

# --- 4. PLOTTING ---
plt.figure(figsize=(10, 8))
plt.suptitle("G3 Swing Curve Analysis")

# Graph 1: tc = 0.12s
plt.subplot(2, 1, 1)
plt.plot(t_steps, delta1_deg, 'b-', linewidth=2, label='Python Solution')
plt.axvline(x=tc1, color='r', linestyle='--', label=f'Fault Clearing (tc={tc1}s)')
plt.title(f'Case 1: tc = {tc1} s (Fast Protection)')
plt.ylabel('Rotor Angle (Degrees)')
plt.grid(True)
plt.legend(loc='upper right')

# Graph 2: tc = 0.21s
plt.subplot(2, 1, 2)
plt.plot(t_steps, delta2_deg, 'r-', linewidth=2, label='Python Solution')
plt.axvline(x=tc2, color='b', linestyle='--', label=f'Fault Clearing (tc={tc2}s)')
plt.title(f'Case 2: tc = {tc2} s (Backup Protection)')
plt.xlabel('Time (s)')
plt.ylabel('Rotor Angle (Degrees)')
plt.grid(True)
plt.legend(loc='upper right')

plt.tight_layout()
plt.show()