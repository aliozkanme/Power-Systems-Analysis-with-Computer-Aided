##################################################################
### ELEKTRİK ENERJİSİ SİSTEMLERİ KARARLILIK ANALİZİ			######
### Analiz: Kritik Temizleme Açısının Hesaplanması        	######
##################################################################

# --- 0. KULLANILACAK KÜTÜPHANELER TANITILIYOR ---
import numpy as np

# --- 1. PARAMETRELER ---
Pm = 2.50
delta0_deg = 15
delta0 = np.deg2rad(delta0_deg)

# Güç Değerleri
Pmax_pre = Pm / np.sin(delta0)
Pmax_fault = 0
Pmax_post = 0.70 * Pmax_pre

# --- 2. KRİTİK AÇI HESABI (Sayısal) ---
# Adım 1: Maksimum Salınım Açısı (delta_max)
# delta_max = 180 - arcsin(Pm / Pmax_post)
delta_max_rad = np.pi - np.arcsin(Pm / Pmax_post)

# Adım 2: Kritik Temizleme Açısı (delta_cr)
# Formül: cos(d_cr) = [Pm*(d_max - d0) + Pmax3*cos(d_max)] / Pmax3
numerator = Pm * (delta_max_rad - delta0) + Pmax_post * np.cos(delta_max_rad)
denominator = Pmax_post
cos_delta_cr = numerator / denominator

delta_cr_rad = np.arccos(cos_delta_cr)
delta_cr_deg = np.rad2deg(delta_cr_rad)

# --- 3. SONUÇLARIN YAZDIRILMASI ---
print("-" * 40)
print(f"HESAPLAMA SONUÇLARI (G3 Parametreleri)")
print("-" * 40)
print(f"Maksimum Salınım Açısı (delta_max): {np.rad2deg(delta_max_rad):.4f} Derece")
print(f"Kritik Temizleme Açısı (delta_cr) : {delta_cr_deg:.4f} Derece")
print("-" * 40)