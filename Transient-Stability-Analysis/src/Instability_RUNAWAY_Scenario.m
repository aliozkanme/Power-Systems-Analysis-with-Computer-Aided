%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% ELECTRICAL ENERGY SYSTEMS STABILITY ANALYSIS            %%%%%%
%%% Analysis: Instability (RUNAWAY) Scenario (Extra Analysis)%%%%%
%%% Note: Since the system remains stable in main scenarios,%%%%%%
%%% tc is increased above theoretical critical time (0.50s) %%%%%%
%%% to demonstrate instability.                             %%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% CLEARING PROGRAM BEFORE ANALYSIS
clc; clear; close all;

%% 1. DEFINITION OF PARAMETERS
f = 50;
omega_s = 2*pi*f;

% G3 Parameters
H = 25.0;           
Pm = 2.50;          
delta0_deg = 15;            
delta0 = deg2rad(delta0_deg);

% Power Values
Pmax_pre = Pm / sin(delta0); 
Pmax_fault = 0;              
Pmax_post = 0.70 * Pmax_pre; 

% Simulation Settings
t_final = 2.5;      % Extended time to observe runaway
tc_unstable = 0.50; % Selected value above critical time (0.41s)

%% 2. SOLUTION
options = odeset('RelTol',1e-4,'AbsTol',1e-6);
[t, y] = ode45(@(t,y) swing_equation_local(t, y, Pm, H, omega_s, Pmax_pre, Pmax_fault, Pmax_post, tc_unstable), [0 t_final], [delta0; 0], options);

%% 3. GRAPH
figure('Name', 'Instability (Runaway) Analysis', 'Color', 'white');
plot(t, rad2deg(y(:,1)), 'r-', 'LineWidth', 2);
hold on;

% Lines (line command is used for older MATLAB versions)
% Manual drawing instead of xline(tc_unstable, ...):
plot([tc_unstable tc_unstable], ylim, 'k--', 'LineWidth', 1.5); 
% Manual drawing instead of yline(180, ...):
plot(xlim, [180 180], 'b:', 'LineWidth', 2);

title(['Instability (Runaway) Example: tc = ' num2str(tc_unstable) 's']);
xlabel('Time (s)');
ylabel('Rotor Angle (\delta) [Degrees]');
grid on;
legend('Rotor Angle', 'Fault Clearing Time', 'Stability Limit (180^o)', 'Location', 'northwest');

%% 4. FUNCTION
function dydt = swing_equation_local(t, y, Pm, H, ws, Pmax1, Pmax2, Pmax3, tc)
    delta = y(1);
    omega_dev = y(2);
    
    if t < 0
        Pe = Pmax1 * sin(delta);
    elseif t <= tc
        Pe = Pmax2 * sin(delta); % During Fault
    else
        Pe = Pmax3 * sin(delta); % Post-Fault
    end
    
    d_delta = omega_dev;
    d_omega = (ws / (2 * H)) * (Pm - Pe);
    
    dydt = [d_delta; d_omega];
end