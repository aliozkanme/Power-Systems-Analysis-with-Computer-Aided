%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% ELEKTRİK ENERJİSİ SİSTEMLERİ KARARLILIK ANALİZİ			%%%%%%
%%% Analiz: Kararsızlık (RUNAWAY) Senaryosu (Ek Analiz)		%%%%%%
%%% Not: Asıl senaryolarda sistem kararlı kaldığı için,		%%%%%%
%%%	kararsızlığı göstermek amacıyla tc süresi teorik kritik %%%%%%
%%% sürenin üzerine (0.50s) çıkarılmıştır.					%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% ANALİZ ÖNCESİNDE PROGRAM TEMİZLENİYOR
clc; clear; close all;

%% 1. PARAMETRELERİN TANIMLANMASI
f = 50;
omega_s = 2*pi*f;

% G3 Parametreleri
H = 25.0;           
Pm = 2.50;          
delta0_deg = 15;            
delta0 = deg2rad(delta0_deg);

% Güç Değerleri
Pmax_pre = Pm / sin(delta0); 
Pmax_fault = 0;              
Pmax_post = 0.70 * Pmax_pre; 

% Simülasyon Ayarları
t_final = 2.5;      % Kopmayı görmek için süreyi biraz uzattık
tc_unstable = 0.50; % Kritik sürenin (0.41s) üzerinde bir değer seçtik

%% 2. ÇÖZÜM
options = odeset('RelTol',1e-4,'AbsTol',1e-6);
[t, y] = ode45(@(t,y) swing_equation_local(t, y, Pm, H, omega_s, Pmax_pre, Pmax_fault, Pmax_post, tc_unstable), [0 t_final], [delta0; 0], options);

%% 3. GRAFİK
figure('Name', 'Kararsızlık (Kopma) Analizi', 'Color', 'white');
plot(t, rad2deg(y(:,1)), 'r-', 'LineWidth', 2);
hold on;

% Çizgiler (Eski MATLAB sürümleri için line komutu kullanılır)
% xline(tc_unstable, ...) yerine manuel çizim:
plot([tc_unstable tc_unstable], ylim, 'k--', 'LineWidth', 1.5); 
% yline(180, ...) yerine manuel çizim:
plot(xlim, [180 180], 'b:', 'LineWidth', 2);

title(['Kararsızlık (Runaway) Örneği: tc = ' num2str(tc_unstable) 's']);
xlabel('Zaman (s)');
ylabel('Rotor Açısı (\delta) [Derece]');
grid on;
legend('Rotor Açısı', 'Arıza Temizleme Anı', 'Kararlılık Sınırı (180^o)', 'Location', 'northwest');

%% 4. FONKSİYON
function dydt = swing_equation_local(t, y, Pm, H, ws, Pmax1, Pmax2, Pmax3, tc)
    delta = y(1);
    omega_dev = y(2);
    
    if t < 0
        Pe = Pmax1 * sin(delta);
    elseif t <= tc
        Pe = Pmax2 * sin(delta); % Arıza anı
    else
        Pe = Pmax3 * sin(delta); % Arıza sonrası
    end
    
    d_delta = omega_dev;
    d_omega = (ws / (2 * H)) * (Pm - Pe);
    
    dydt = [d_delta; d_omega];
end