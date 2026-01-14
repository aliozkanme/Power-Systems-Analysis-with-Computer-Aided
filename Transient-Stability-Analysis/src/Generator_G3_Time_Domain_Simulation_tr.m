%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% ELEKTRİK ENERJİSİ SİSTEMLERİ KARARLILIK ANALİZİ			%%%%%%
%%% Analiz: Generatör-3 (G3) Zaman Tanım Alanı Simülasyonu	%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% ANALİZ ÖNCESİNDE PROGRAM TEMİZLENİYOR
clc; clear; close all;

%% 1. SİSTEM PARAMETRELERİ
f = 50;             % Hz
omega_s = 2*pi*f;   % Senkron Açısal Hız (rad/s)

% G3 Parametreleri
H = 25.0;           % s (Sistem Bazında)
Pm = 2.50;          % pu

% Başlangıç Koşulları
delta0_deg = 15;            % Derece
delta0 = deg2rad(delta0_deg); % Radyan

% Güç Transfer Kapasiteleri (Pmax)
% Pre-Fault: Pm = Pmax * sin(delta0) -> Pmax = 2.50 / sin(15)
Pmax_pre = Pm / sin(delta0); 
Pmax_fault = 0;              % Arıza anı (Kısa devre)
Pmax_post = 0.70 * Pmax_pre; % Arıza sonrası (%70 kapasite)

% Arıza Temizleme Süreleri (Senaryolar)
tc_case1 = 0.12;    % s (Hızlı Koruma)
tc_case2 = 0.21;    % s (Yedek Koruma)
t_final = 2.0;      % Simülasyon süresi

%% 2. DİFERANSİYEL DENKLEM ÇÖZÜMÜ (ODE45)
options = odeset('RelTol',1e-4,'AbsTol',1e-6);

% Durum 1: tc = 0.12 s Çözümü
[t1, y1] = ode45(@(t,y) swing_equation(t, y, Pm, H, omega_s, Pmax_pre, Pmax_fault, Pmax_post, tc_case1), [0 t_final], [delta0; 0], options);

% Durum 2: tc = 0.21 s Çözümü
[t2, y2] = ode45(@(t,y) swing_equation(t, y, Pm, H, omega_s, Pmax_pre, Pmax_fault, Pmax_post, tc_case2), [0 t_final], [delta0; 0], options);

%% 3. GRAFİK ÇİZİMİ
figure('Name', 'G3 Kararlılık Analizi', 'Color', 'white');

% Grafik 1: tc = 0.12s
subplot(2,1,1);
plot(t1, rad2deg(y1(:,1)), 'b-', 'LineWidth', 2); hold on;
xline(tc_case1, 'r--', 'LineWidth', 1.5, 'Label', ['tc=' num2str(tc_case1) 's']);
yline(180, 'k:', 'LineWidth', 1); % Kararsızlık sınırı
title(['Durum 1: tc = 0.12 s (Hızlı Koruma)']);
ylabel('Rotor Açısı (\delta) [Derece]'); grid on;

% Grafik 2: tc = 0.21s
subplot(2,1,2);
plot(t2, rad2deg(y2(:,1)), 'r-', 'LineWidth', 2); hold on;
xline(tc_case2, 'b--', 'LineWidth', 1.5, 'Label', ['tc=' num2str(tc_case2) 's']);
title(['Durum 2: tc = 0.21 s (Yedek Koruma)']);
xlabel('Zaman (s)'); ylabel('Rotor Açısı (\delta) [Derece]'); grid on;

sgtitle('G3 Swing Eğrisi Analizi');

%% 4. FONKSİYON TANIMI (Swing Denklemi)
function dydt = swing_equation(t, y, Pm, H, ws, Pmax1, Pmax2, Pmax3, tc)
    delta = y(1);      % Rotor Açısı
    omega_dev = y(2);  % Hız Sapması
    
    % Arıza durumuna göre P_elektriksel seçimi
    if t < 0
        Pe = Pmax1 * sin(delta);
    elseif t <= tc
        Pe = Pmax2 * sin(delta); % Arıza Süresince (Pe=0)
    else
        Pe = Pmax3 * sin(delta); % Arıza Sonrası
    end
    
    % Diferansiyel Denklemler
    d_delta = omega_dev;
    d_omega = (ws / (2 * H)) * (Pm - Pe);
    
    dydt = [d_delta; d_omega];
end