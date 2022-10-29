%% Initial setup

clear all
clc

global rad 
rad = 2*pi/360;                         % From degrees to radians

%% Environment variables

m = 25;                                 % vehicle mass (kg)
rw = 0.03;                              % wheel radius (m)
theta = 41*rad;                         % incline angle (rad)

Tm = 4.5;                                 % motor torque (N/m)
rpm = 630;                             % rotations per minute

%% Calculate forces

Fz = m*9.81;                            % gravitational force (N)

Fnx = Fz*sin(theta)*cos(theta);         % normal force x component (N)
Fny = Fz*cos(theta)^2;                  % normal force y component (N)

T = sqrt(Fnx^2+(-Fz+Fny)^2)*rw;         % torque (N/m)

a = ((Tm/rw)-T/rw)/m;

c = 2*pi*rw;

v = (rpm/60)*c;

%% Print values

fprintf("Torque required: %.2f N/m\n", T);
fprintf("Accelleration: %.2f m/s^2\n", a);
fprintf("Maximum speed: %.2f m/s  -  %.2f km/h\n", v, v*3.6);

