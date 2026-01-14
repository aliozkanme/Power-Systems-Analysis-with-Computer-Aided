> 🇺🇸 **[Click for English Version / İngilizce Versiyon İçin Tıklayınız](README.md)**

---
# Eşit Alan Kriteri ve Zaman Bölgesi Simülasyonları Kullanılarak Çok Makineli Güç Sistemlerinde Geçici Hal Kararlılığının Analizi: Üç Jeneratörlü Bir Sistem Vaka Çalışması

<img alt="Creative Commons Licence" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" height="20"/> <img src="https://img.shields.io/badge/license-Apache%202.0-blue" alt="license"/> [![ResearchGate](https://img.shields.io/badge/ResearchGate-Read%20Paper-green?logo=researchgate)](https://www.researchgate.net/publication/399759430_Analysis_of_Transient_Stability_in_Multi_Machine_Power_Systems_Using_Equal_Area_Criterion_and_Time_Domain_Simulations_Case_Study_of_a_Three_Generator_System?_sg%5B0%5D=KtPtKUvNB7fa_BL7hwQ_DeT8I_oPCzbV-UTvH_ik7YzlJSmftrIHEHpsJs0aF1T-iR33bo--uHLf8oykMa7ShstRivG6joBhIbvWktqn.09lUoo70uXKn0KWgRjmJuanRLXwWzGkxijSmh-QxCN17T5BZ8Q2BVwkQeSTm0EDlgl2YRVKP48Il2iqj_RnbkA&_tp=eyJjb250ZXh0Ijp7ImZpcnN0UGFnZSI6ImhvbWUiLCJwYWdlIjoicHJvZmlsZSIsInByZXZpb3VzUGFnZSI6InByb2ZpbGUiLCJwb3NpdGlvbiI6InBhZ2VDb250ZW50In19) <img src="https://img.shields.io/github/last-commit/https://github.com/aliozkanme/Power-Systems-Analysis-with-Computer-Aided/tree/main/Transient-Stability-Analysis" alt="last commit"/> 

---

Bu proje, üç fazlı bir kısa devre arızasına maruz kalan çok makineli bir güç sisteminin geçici hal kararlılığını incelemektedir. Analiz, teorik hesaplama için **Eşit Alan Kriteri'ni (EAK)** kullanmakta ve sonuçları hem **MATLAB (ODE45)** hem de **Python (SciPy)** ortamlarında zaman bölgesi simülasyonları kullanarak doğrulamaktadır.

## 🎓 Proje Bilgileri

| Alan | Detaylar |
| :--- | :--- |
| **Konu** | Güç Sistemi Kararlılığı & Koruma Koordinasyonu |
| **Analiz Yöntemleri** | Eşit Alan Kriteri, Zaman Bölgesi İntegrasyonu (Runge-Kutta) |
| **Araçlar** | Manuel Hesaplama, MATLAB, Python |
| **Yazar** | Ali Özkan |

## 📄 Problem Tanımı

Çalışma, üç senkron generatör tarafından beslenen bir iletim bölgesini modellemektedir. Generatör terminallerinden 15 km uzaklıktaki 154 kV'luk çift devreli bir iletim hattında bir **3-Fazlı Kısa Devre Arızası** meydana gelmektedir.

Amaç, farklı arıza temizleme süreleri ($t_c$) altında sistemin senkronizasyonu yeniden kazanma yeteneğini (Geçici Hal Kararlılığı) analiz etmek ve **Kritik Temizleme Açısını ($\delta_{cr}$)** belirlemektir.

### Sistem Parametreleri (G3)

Belirli proje kısıtlamalarına dayanarak, kritik generatör (G3) aşağıdaki karakteristiklere sahiptir:

* **Eylemsizlik Sabiti ($H$):** $25.0 \text{ s}$
* **Mekanik Güç Girişi ($P_m$):** $2.50 \text{ pu}$
* **Sistem Frekansı:** $50 \text{ Hz}$
* **Başlangıç Rotor Açısı ($\delta_0$):** $15^\circ$

### Amaç

Bu projenin temel amacı, üç fazlı kısa devre arızasına maruz kalan çok makineli bir güç sisteminin **geçici hal kararlılığını** kapsamlı bir şekilde analiz etmektir. Çalışma, kritik bir rüzgar generatörünün (G3) dinamik davranışına odaklanmakta ve şunları amaçlamaktadır:

* **Kararlılık Sınırlarını Belirlemek:** Teorik **Eşit Alan Kriteri'ni (EAK)** kullanarak **Kritik Temizleme Açısını ($\delta_{cr}$)** ve **Kritik Temizleme Süresini ($t_{cr}$)** hesaplamak.
* **Koruma Koordinasyonunu Doğrulamak:** Hızlı ve yedek koruma şemalarına karşılık gelen standart arıza temizleme süreleri ($t_c = 0.12s$ ve $t_c = 0.21s$) altında sistemin senkronizasyonu yeniden kazanma yeteneğini değerlendirmek.
* **Algoritmaları Çapraz Doğrulamak:** Dinamik modellerin doğruluğunu sağlamak için hem **MATLAB** hem de **Python**'da sayısal çözüm algoritmalarını (Runge-Kutta) uygulamak ve karşılaştırmak.
* **Kararsızlığı Göstermek:** Koruma sınırları aşıldığında senkronizm kaybını görselleştirmek için bir "Kopma" (runaway) senaryosu ($t_c = 0.50s$) simüle etmek.

## 🧮 Matematiksel Arka Plan

Rotor açısının dinamikleri, doğrusal olmayan **Salınım Denklemi** (Swing Equation) tarafından yönetilir:

$$
\frac{2H}{\omega_s} \frac{d^2\delta}{dt^2} = P_m - P_e
$$

Burada $P_e$, güç-açı karakteristiği ile tanımlanan elektriksel güç çıkışıdır:
$$
P_e = P_{max} \sin(\delta)
$$

### Eşit Alan Kriteri (EAK)
Diferansiyel denklemi çözmeden kararlılığı belirlemek için EAK, yavaşlatıcı alanın ($A_2$), arıza sırasında kazanılan hızlandırıcı alandan ($A_1$) büyük veya ona eşit olması gerektiğini belirtir.

**Kritik Temizleme Açısı ($\delta_{cr}$)** şu şekilde hesaplanır:

$$
\cos \delta_{cr} = \frac{P_m}{P_{max3}} (\delta_{max} - \delta_0) + \cos \delta_{max}
$$

## ⚙️ Metodoloji & Çözümler

Bu proje üç aşamalı bir doğrulama yaklaşımı kullanır:

1.  **Manuel Hesaplama:** Sistem parametrelerinin türetilmesi, şebekenin tek makine-sonsuz bara (SMIB) modeline indirgenmesi ve $\delta_{cr}$ değerinin analitik olarak hesaplanması.
2.  **MATLAB Simülasyonu:** Salınım denklemi dinamiklerini zaman içinde simüle etmek için `ode45` çözücüsünün kullanılması.
3.  **Python Simülasyonu:** MATLAB sonuçlarını çapraz doğrulamak ve alan analizi için sayısal integrasyon gerçekleştirmek amacıyla `scipy.integrate.odeint` ve `numpy.trapz` kullanılması.

### Sistem Topolojisi
Sistem iki gruptan oluşur:
1.  **Grup A:** Termik + Hidro Jeneratörler (Bağdaşık/Kararlı).
2.  **Grup B:** Rüzgar Jeneratörü (G3) - **Bağımsız & Kritik**.

*G3 sistemin geri kalanına karşı bağımsız olarak salındığından, kararlılık analizi G3'ün sistem barasına göre dinamiğine odaklanır.*

![Sistem Tek Hat Şeması](images/system_topology.png)

### Analiz Edilen Senaryolar

| Durum | Temizleme Süresi ($t_c$) | Koruma Tipi | Sonuç |
| :--- | :---: | :--- | :--- |
| **Durum 1** | $0.12 \text{ s}$ | Hızlı Koruma | ✅ **Kararlı** |
| **Durum 2** | $0.21 \text{ s}$ | Yedek Koruma | ✅ **Kararlı** |
| **Durum 3** | $0.50 \text{ s}$ | Gecikmeli (Teorik) | ❌ **Kararsız (Kontrolden Çıkma)** |

## 💻 Simülasyon Kodları & Uygulama

Temel analiz mantığı, sayısal doğruluğu sağlamak için hem **MATLAB** hem de **Python**'da paralel uygulamalar içeren `src` dizini altında düzenlenmiştir. Bu betikler, zaman bölgesi simülasyonlarını (`ode45`/`odeint`), kritik temizleme açısı hesaplamalarını ve karakteristik eğrilerin oluşturulmasını ele alarak teorik sonuçların sağlam bir çapraz doğrulamasını sağlar.

### Analiz: generatör-3 (G3) Zaman Bölgesi Simülasyonu

Kararlılık analizinin güvenilirliğini sağlamak için, zaman bölgesi simülasyonları iki farklı programlama ortamında (**MATLAB** ve **Python**) bağımsız olarak uygulanmıştır. Her iki betik de kritik **generatör 3 (G3)** için doğrusal olmayan **Salınım Denklemini** modeller ve sistemi Hızlı ($t_c=0.12s$) ve Yedek ($t_c=0.21s$) koruma senaryoları altında simüle eder.

#### MATLAB Kodu

[](Generator_G3_Time_Domain_Simulation_tr.m)

#### Python Kodu

[](Generator_G3_Time_Domain_Simulation_tr.py)

### Analiz: MATLAB ve Python Sonuçlarının Karşılaştırılması

Python'un `odeint` çözücüsü kullanılarak yedek koruma senaryosu ($t_c=0.21s$) için sistem dinamiklerini çözer ve sonucu MATLAB `ode45` çözümünden türetilen örnek noktalarla üst üste bindirir. Ortaya çıkan grafikte gözlemlenen mükemmel örtüşme, her iki hesaplama yönteminin de aynı rotor açısı yörüngelerini ürettiğini doğrular.

#### Python Kodu

[](Comparison_of_MATLAB_and_Python_Results_tr.py)

### Analiz: Güç - Açı Karakteristik Eğrileri

Sistemin statik kararlılığının görsel bir temsilini sağlamak için, ilgili betik **Güç-Açı ($\delta - P$)** karakteristik eğrilerini oluşturur. Elektriksel güç çıkışını rotor açısına karşı üç farklı şebeke durumu için çizer: **Arıza Öncesi**, **Arıza Sırası** ve **Arıza Sonrası**. Bu görselleştirme, Eşit Alan Kriteri analizi için gerekli olan başlangıç çalışma noktasını ($\delta_0$) ve maksimum güç aktarım kapasitelerini ($P_{max}$) vurgular.

#### MATLAB Kodu

[](Power_Angle_Characteristic_Curves_tr.m)

### Analiz: Sayısal İntegrasyon (trapz) Yöntemi Kullanılarak Eşit Alan Kriteri Hesabı

Teorik kararlılık sınırlarını sayısal olarak doğrulamak için, ilgili betik Python kullanarak **Eşit Alan Kriteri'ni (EAK)** uygular. Yedek koruma senaryosu ($t_c=0.21s$) için spesifik temizleme açısını ($\delta_{cl}$) belirler ve Hızlandırıcı ($A_1$) ve Mevcut Yavaşlatıcı ($A_2$) alanlarını hesaplamak için **Yamuk (Trapez) İntegrasyon yöntemini** (`numpy.trapz`) kullanarak enerji dengesi üzerinden sistemin kararlılık marjını doğrular.

#### Python Kodu

[](Calculation_of_Equal_Area_Criterion_tr.py)

### Analiz: Kritik Temizleme Açısı Hesabı

Sistemin kesin kararlılık sınırını belirlemek için, ilgili betik **Kritik Temizleme Açısını ($\delta_{cr}$)** analitik olarak hesaplar. **Eşit Alan Kriteri**'ne dayalı türetilmiş matematiksel formülü uygulayarak, sistem senkronizmini kaybetmeden önceki kesin maksimum izin verilen rotor açısını ($\approx 90.25^\circ$) belirler.

#### Python Kodu

[](Calculation_of_Critical_Clearing_Angle_tr.py)

### Analiz: Kararsızlık (KONTROLDEN ÇIKMA) Senaryosu (Ekstra Analiz)

Gecikmeli arıza temizlemenin sonuçlarını göstermek için, ilgili betik arıza temizleme süresinin ($t_c=0.50s$) hesaplanan kritik sınırı ($t_{cr} \approx 0.41s$) kasıtlı olarak aştığı bir "Kontrolden Çıkma" (Runaway) senaryosunu simüle eder. Elde edilen simülasyon, rotor açısının kararlı bir dengeye dönmeden monoton bir şekilde artmasıyla senkronizm kaybını görsel olarak doğrular.

#### Matlab Kodu

[](Instability_RUNAWAY_Scenario_tr.m)

## 📊 Sonuçlar

### 1. Güç-Açı Karakteristikleri
Sistemin güç aktarım kapasitesi arıza sırasında sıfıra yakın bir seviyeye düşer ve hat açıldıktan sonra arıza öncesi kapasitenin %70'ine toparlanır. Mekanik güç hattı, arıza sonrası güç eğrisini kestiği için statik kararlılık doğrulanmıştır.
* $P_{max\_pre} \approx 9.66 \text{ pu}$
* $P_{max\_post} \approx 6.76 \text{ pu}$

![Güç Açı Eğrisi](images/Power_Angle_Characteristic_Curves.png)

### 2. Zaman Bölgesi Simülasyonu (Kararlılık)
Hem **MATLAB** hem de **Python** simülasyonları, $t_c = 0.12s$ ve $t_c = 0.21s$ için rotor açısının salındığını ancak sönümlenerek kararlı kaldığını doğrulamaktadır. Yüksek eylemsizlik ($H=25s$) sağlam bir kararlılık marjı sağlar.

![Zaman Bölgesi Simülasyonu](images/Generator_G3_Time_Domain_Simulation_matlab.png)

### 3. Algoritmaların Karşılaştırılması
MATLAB (`ode45`) ve Python (`odeint`) sonuçları üst üste bindirilmiştir. Yörüngeler mükemmel bir şekilde örtüşmekte olup, her iki dilde oluşturulan sayısal modellerin doğruluğunu kanıtlamaktadır.

![Karşılaştırma Grafiği](images/Comparison_of_MATLAB_and_Python_Results.png)

### 4. Kritik Temizleme Açısı Hesabı
Kritik Temizleme Açısı, EAK kullanılarak analitik olarak hesaplanmış ve Python'da sayısal integrasyon (Trapz yöntemi) ile doğrulanmıştır.
* **Hesaplanan $\delta_{cr}$:** $\approx 90.25^\circ$

![Eşit Alan Hesabı](images/Calculation_of_Equal_Area_Criterion.png)

Detaylı hesaplama çıktısı:

![Kritik Açı Çıktısı](images/Calculation_of_Critical_Clearing_Angle.png)

### 5. Kararsızlık (Kontrolden Çıkma) Senaryosu
"Senkronizm Kaybını" göstermek için $0.50s$ süreli bir arıza uygulanmıştır. Bu süre kritik süreyi ($t_{cr} \approx 0.41s$) aştığı için, rotor açısı monoton olarak artmakta ve sistem kararsızlığına yol açmaktadır.

![Kontrolden Çıkma Senaryosu](images/Instability_RUNAWAY_Scenario.png)

## 📜 Sonuç & Tartışma

Bu çalışma, üç fazlı kısa devre arızası altındaki çok makineli bir güç sisteminin geçici hal kararlılığını başarıyla modellemiştir. Kapsamlı analiz aşağıdaki temel sonuçlara yol açmıştır:

* **Modellerin Doğrulanması:** Eşit Alan Kriteri'ne dayalı manuel hesaplamalar, MATLAB dinamik simülasyonları ve Python sayısal integrasyon algoritmaları arasında yüksek derecede tutarlılık gözlemlenmiştir. Analitik olarak hesaplanan kritik temizleme açısı ($\delta_{cr} \approx 90.24^\circ$), simülasyon çıktılarıyla mükemmel bir şekilde eşleşmiştir.
* **Sistem Kararlılığı:** Sistem, kritik rüzgar jeneratörünün (G3) yüksek eylemsizlik sabitine ($H=25s$) atfedilen sağlam bir kararlılık marjı sergilemektedir. Rotor açısı, her iki standart koruma süresi ($0.12s$ ve $0.21s$) için kararlı bölge içinde kalmıştır.
* **Kritik Sınırlar:** Analiz, $t_c=0.50s$ senaryosunda gösterildiği gibi kritik temizleme süresinin aşılmasının monoton kararsızlığa yol açtığını doğrulamıştır. Bu durum, ardışık arızaları ve potansiyel elektrik kesintilerini (blackout) önlemek için hızlı arıza temizlemenin ve doğru röle koordinasyonunun kritik gerekliliğini vurgulamaktadır.