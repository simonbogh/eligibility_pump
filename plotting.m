close all
clear all
clc


load('C:\Users\koch\Documents\Skole\Uni\Kandidat\4 Semester\svn_kandidat\Resultater\TestLevel1\DQN\softmax\Tmix\3_DQN_mix.mat')
plot(ans)
grid
legend('Tmix', 'T1room', 'Tamb')
title('Deep Q-network on Test Level 1 Model')
xlabel('Time[s]')
ylabel('Temperature')