%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% ELEKTRİK ENERJİSİ SİSTEMLERİ KARARLILIK ANALİZİ			%%%%%%
%%% Analiz: Güç - Açı (Power-Angle) Karakteristik Eğrileri	%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% ANALİZ ÖNCESİNDE PROGRAM TEMİZLENİYOR
clc; clear; close all;

%% 1. PARAMETRELER (Manuel Hesaplamalardan)
Pm = 2.50;          % Mekanik Güç (pu)
delta0_deg = 15;    % Arıza Öncesi Açı (Derece)

% Güç Transfer Kapasiteleri (Pmax)
% Arıza Öncesi: Pm = Pmax * sin(15) -> Pmax = 9.66
Pmax_pre = 9.66; 
Pmax_fault = 0;     % Arıza Sırası (Tam Kısa Devre)
Pmax_post = 6.76;   % Arıza Sonrası (%70 Kapasite)

%% 2. EĞRİLERİN OLUŞTURULMASI
delta_deg = 0:0.1:180;        % 0 ile 180 derece arası açı vektörü
delta_rad = deg2rad(delta_deg);

% Elektriksel Güç Denklemleri (Pe = Pmax * sin(delta))
Pe_pre = Pmax_pre * sin(delta_rad);   % Eğri 1: Arıza Öncesi
Pe_fault = zeros(size(delta_deg));    % Eğri 2: Arıza Sırası (0)
Pe_post = Pmax_post * sin(delta_rad); % Eğri 3: Arıza Sonrası

%% 3. GRAFİK ÇİZİMİ
figure('Name', 'Güç-Açı Karakteristiği', 'Color', 'white');
hold on; grid on;

% Mekanik Güç Hattı (Pm)
yline(Pm, 'k--', 'LineWidth', 2, 'DisplayName', ['Pm = ' num2str(Pm) ' pu']);

% Güç Eğrileri
plot(delta_deg, Pe_pre, 'b-', 'LineWidth', 2, 'DisplayName', 'Arıza Öncesi');
plot(delta_deg, Pe_post, 'g-', 'LineWidth', 2, 'DisplayName', 'Arıza Sonrası');
plot(delta_deg, Pe_fault, 'r-', 'LineWidth', 2, 'DisplayName', 'Arıza Sırası');

% Kritik Noktaların İşaretlenmesi
% Başlangıç Açısı (delta0)
plot(delta0_deg, Pm, 'ko', 'MarkerFaceColor', 'k', 'MarkerSize', 8, 'HandleVisibility', 'off');
text(delta0_deg, Pm+0.5, ['\delta_0=' num2str(delta0_deg) '^o'], 'FontSize', 10, 'FontWeight', 'bold');

% Eksen ve Başlık Ayarları
xlabel('Rotor Açısı (\delta) [Derece]');
ylabel('Güç (P) [pu]');
title(['Güç - Açı Karakteristik Eğrileri']);
legend('Location', 'northeast');
xlim([0 180]);
ylim([0 Pmax_pre+1]); % Grafiği biraz yukarıdan kes

% Opsiyonel: Alanları Göstermek İçin Bölge Taraması (Estetik)
% (Raporun kalitesini artırmak için eklenebilir)
area(delta_deg, Pe_fault, 'FaceColor', 'r', 'FaceAlpha', 0.1, 'EdgeColor', 'none', 'HandleVisibility', 'off'); 

hold off;