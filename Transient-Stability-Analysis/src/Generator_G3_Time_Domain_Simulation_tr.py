##################################################################
### ELEKTRİK ENERJİSİ SİSTEMLERİ KARARLILIK ANALİZİ			######
### Analiz: Generatör-3 (G3) Zaman Tanım Alanı Simülasyonu	######
##################################################################

# --- 0. KULLANILACAK KÜTÜPHANELER TANITILIYOR ---
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# --- 1. SİSTEM PARAMETRELERİ (Manuel Hesaplamalardan) ---
S_base = 100        # MVA
f = 50              # Hz
omega_s = 2 * np.pi * f # Senkron Açısal Hız (314.16 rad/s)

# G3 Parametreleri
H = 25.0            # s
Pm = 2.50           # pu
delta0_deg = 15     # Derece
delta0 = np.deg2rad(delta0_deg) # Radyan

# Güç Transfer Kapasiteleri (Pmax)
# Pre-Fault: Pm = Pmax * sin(delta0) formülünden geri hesaplama
Pmax_pre = Pm / np.sin(delta0)  # ~9.66 pu
Pmax_fault = 0                  # Arıza Sırası (Tam Kısa Devre)
Pmax_post = 0.70 * Pmax_pre     # Arıza Sonrası (%70 Kapasite)

# Zaman Tanımları
t_final = 2.0
t_steps = np.linspace(0, t_final, 2000) # Çözünürlük için 2000 adım

# --- 2. SWING DENKLEMİ FONKSİYONU ---
def swing_equation(y, t, tc):
    delta, omega_dev = y
    
    # Elektriksel Güç (Pe) Duruma Göre Seçimi
    if t < 0:
        Pe = Pmax_pre * np.sin(delta) # Arıza Öncesi
    elif t <= tc:
        Pe = Pmax_fault * np.sin(delta) # Arıza Sırası (Pe=0)
    else:
        Pe = Pmax_post * np.sin(delta)  # Arıza Sonrası (Hat Açıldı)
        
    # Durum Denklemleri
    # d(delta)/dt = omega_dev
    # d(omega)/dt = (omega_s / 2H) * (Pm - Pe)
    d_delta = omega_dev
    d_omega = (omega_s / (2 * H)) * (Pm - Pe)
    
    return [d_delta, d_omega]

# --- 3. SİMÜLASYON (ODEINT ÇÖZÜMÜ) ---
y0 = [delta0, 0] # Başlangıç Koşulları [Açı, Hız Sapması]

# Durum 1: tc = 0.12 s (Hızlı Koruma)
tc1 = 0.12
sol1 = odeint(swing_equation, y0, t_steps, args=(tc1,))
delta1_deg = np.rad2deg(sol1[:, 0])

# Durum 2: tc = 0.21 s (Yedek Koruma)
tc2 = 0.21
sol2 = odeint(swing_equation, y0, t_steps, args=(tc2,))
delta2_deg = np.rad2deg(sol2[:, 0])

# --- 4. GRAFİK ÇİZİMİ ---
plt.figure(figsize=(10, 8))
plt.suptitle("G3 Swing Eğrisi Analizi")

# Grafik 1: tc = 0.12s
plt.subplot(2, 1, 1)
plt.plot(t_steps, delta1_deg, 'b-', linewidth=2, label='Python Çözümü')
plt.axvline(x=tc1, color='r', linestyle='--', label=f'Arıza Temizleme (tc={tc1}s)')
plt.title(f'Durum 1: tc = {tc1} s (Hızlı Koruma)')
plt.ylabel('Rotor Açısı (Derece)')
plt.grid(True)
plt.legend(loc='upper right')

# Grafik 2: tc = 0.21s
plt.subplot(2, 1, 2)
plt.plot(t_steps, delta2_deg, 'r-', linewidth=2, label='Python Çözümü')
plt.axvline(x=tc2, color='b', linestyle='--', label=f'Arıza Temizleme (tc={tc2}s)')
plt.title(f'Durum 2: tc = {tc2} s (Yedek Koruma)')
plt.xlabel('Zaman (s)')
plt.ylabel('Rotor Açısı (Derece)')
plt.grid(True)
plt.legend(loc='upper right')

plt.tight_layout()
plt.show()