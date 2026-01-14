##################################################################
### ELEKTRİK ENERJİSİ SİSTEMLERİ KARARLILIK ANALİZİ			######
### Analiz: Eşik alan kriterini sayısal integrasyon (trapz) ######
### yöntemiyle hesaplanması                             	######
##################################################################

# --- 0. KULLANILACAK KÜTÜPHANELER TANITILIYOR ---
import numpy as np
from scipy.integrate import odeint

# --- 1. SİSTEM PARAMETRELERİ ---
H = 25.0
Pm = 2.50
delta0 = np.deg2rad(15) # Radyan

# Pmax Değerleri
Pmax_pre = Pm / np.sin(delta0)
Pmax_fault = 0
Pmax_post = 0.70 * Pmax_pre

# Kritik Parametreler
omega_s = 2 * np.pi * 50
tc = 0.21 # Analiz edilecek temizleme süresi

# --- 2. TEMİZLEME AÇISINI BULMA (Simülasyon) ---
# Önce tc anındaki açıyı bulmak için kısa bir simülasyon yapıyoruz
def swing_fault(y, t):
    delta, w = y
    Pe = Pmax_fault * np.sin(delta)
    return [w, (omega_s / (2*H)) * (Pm - Pe)]

t_fault = np.linspace(0, tc, 100)
sol = odeint(swing_fault, [delta0, 0], t_fault)
delta_cl = sol[-1, 0] # Temizleme anındaki açı (Radyan)
delta_cl_deg = np.rad2deg(delta_cl)

print(f"Temizleme Süresi (tc): {tc} s")
print(f"Temizleme Açısı (delta_cl): {delta_cl_deg:.2f} Derece")

# --- 3. ALANLARIN HESAPLANMASI (TRAPZ Yöntemi) ---

# A1: Hızlandırıcı Alan (delta0 -> delta_cl)
# İntegral: (Pm - Pe_fault) d_delta
d_range1 = np.linspace(delta0, delta_cl, 1000)
Pe_fault_curve = np.zeros_like(d_range1) # Pmax_fault = 0
A1 = np.trapz(Pm - Pe_fault_curve, d_range1)

# A2_max: Mevcut Yavaşlatıcı Alan (delta_cl -> delta_max_theoretical)
# delta_max_theoretical: Pm ile Pmax_post'un kesiştiği kararsız nokta (pi - arcsin(...))
delta_max_theo = np.pi - np.arcsin(Pm / Pmax_post)
delta_max_deg = np.rad2deg(delta_max_theo)

# İntegral: (Pe_post - Pm) d_delta
d_range2 = np.linspace(delta_cl, delta_max_theo, 1000)
Pe_post_curve = Pmax_post * np.sin(d_range2)
A2_available = np.trapz(Pe_post_curve - Pm, d_range2)

# --- 4. SONUÇLARIN YAZDIRILMASI ---
print("-" * 30)
print(f"Hızlandırıcı Alan (A1)      : {A1:.4f}")
print(f"Mevcut Yavaşlatıcı Alan (A2): {A2_available:.4f}")
print("-" * 30)

if A2_available > A1:
    print("SONUÇ: A2 > A1 olduğu için SİSTEM KARARLIDIR.")
    margin = A2_available - A1
    print(f"Kararlılık Marjı (Enerji)   : {margin:.4f}")
else:
    print("SONUÇ: A2 < A1 olduğu için SİSTEM KARARSIZDIR.")