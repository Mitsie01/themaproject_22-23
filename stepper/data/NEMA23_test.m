r_wheel = 0.035;

data = readtable('data_files/NEMA23_2A-22-2.csv');

U = table2array(data(:,2));
I = table2array(data(:,3));
f = table2array(data(:,4));
steps = table2array(data(:,5));
m_d = table2array(data(:,6));
m_u = table2array(data(:,7));

P = U.*I;
w = (f./steps)*2*pi;
Ftot = (m_d - m_u).*9.81;
T = Ftot.*r_wheel;

plot(w,T,'-o')