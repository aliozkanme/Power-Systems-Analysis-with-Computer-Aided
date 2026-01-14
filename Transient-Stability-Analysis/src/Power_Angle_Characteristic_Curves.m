%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% ELECTRICAL ENERGY SYSTEMS STABILITY ANALYSIS            %%%%%%
%%% Analysis: Power - Angle Characteristic Curves           %%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% CLEARING PROGRAM BEFORE ANALYSIS
clc; clear; close all;

%% 1. PARAMETERS (From Manual Calculations)
Pm = 2.50;          % Mechanical Power (pu)
delta0_deg = 15;    % Pre-Fault Angle (Degrees)

% Power Transfer Capabilities (Pmax)
% Pre-Fault: Pm = Pmax * sin(15) -> Pmax = 9.66
Pmax_pre = 9.66; 
Pmax_fault = 0;     % During Fault (Solid Short Circuit)
Pmax_post = 6.76;   % Post-Fault (70% Capacity)

%% 2. GENERATION OF CURVES
delta_deg = 0:0.1:180;        % Angle vector between 0 and 180 degrees
delta_rad = deg2rad(delta_deg);

% Electrical Power Equations (Pe = Pmax * sin(delta))
Pe_pre = Pmax_pre * sin(delta_rad);   % Curve 1: Pre-Fault
Pe_fault = zeros(size(delta_deg));    % Curve 2: During Fault (0)
Pe_post = Pmax_post * sin(delta_rad); % Curve 3: Post-Fault

%% 3. GRAPH PLOTTING
figure('Name', 'Power-Angle Characteristic', 'Color', 'white');
hold on; grid on;

% Mechanical Power Line (Pm)
yline(Pm, 'k--', 'LineWidth', 2, 'DisplayName', ['Pm = ' num2str(Pm) ' pu']);

% Power Curves
plot(delta_deg, Pe_pre, 'b-', 'LineWidth', 2, 'DisplayName', 'Pre-Fault');
plot(delta_deg, Pe_post, 'g-', 'LineWidth', 2, 'DisplayName', 'Post-Fault');
plot(delta_deg, Pe_fault, 'r-', 'LineWidth', 2, 'DisplayName', 'During-Fault');

% Marking Critical Points
% Initial Angle (delta0)
plot(delta0_deg, Pm, 'ko', 'MarkerFaceColor', 'k', 'MarkerSize', 8, 'HandleVisibility', 'off');
text(delta0_deg, Pm+0.5, ['\delta_0=' num2str(delta0_deg) '^o'], 'FontSize', 10, 'FontWeight', 'bold');

% Axis and Title Settings
xlabel('Rotor Angle (\delta) [Degree]');
ylabel('Power (P) [pu]');
title(['Power - Angle Characteristic Curves']);
legend('Location', 'northeast');
xlim([0 180]);
ylim([0 Pmax_pre+1]); % Crop graph slightly from top

% Optional: Area Shading (Aesthetic)
% (Can be added to improve report quality)
area(delta_deg, Pe_fault, 'FaceColor', 'r', 'FaceAlpha', 0.1, 'EdgeColor', 'none', 'HandleVisibility', 'off'); 

hold off;