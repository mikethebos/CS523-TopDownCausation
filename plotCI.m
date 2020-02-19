clear 
clc
TD = readmatrix('TD_data.csv');
BU = readmatrix('BU_data.csv');

% Values of epsilon: ranging from 0 to 1 at increments of 0.05
epsvals = [0:0.025:1];

%Calculate mean and standard deviation of both TD and BU data
muTD = mean(TD,2);
muBU = mean(BU,2);
sdTD = std(TD, 0, 2);
sdBU = std(BU, 0, 2);

% Calculate 95% confidence intervals around the mean for TD and BU
cisTD = zeros(length(epsvals), 2);
cisBU = zeros(length(epsvals), 2);
%2.045 from a t-distribution table for 95% confidence and 30 samples
cisTD(:, 1) = muTD - 2.045*(sdTD./sqrt(length(TD(1,:))));
cisTD(:, 2) = muTD + 2.045*(sdTD./sqrt(length(TD(1,:))));
cisBU(:, 1) = muBU - 2.045*(sdBU./sqrt(length(BU(1,:))));
cisBU(:, 2) = muBU + 2.045*(sdBU./sqrt(length(BU(1,:))));

%Plot the mean and CI for TD and BU data
augx =[epsvals, fliplr(epsvals)];
augy_TD =[cisTD(:,1)', flipud(cisTD(:,2))'];
augy_BU =[cisBU(:,1)', flipud(cisBU(:,2))'];
hold on
plot(epsvals, muTD, 'r', 'linewidth', 1);
plot(epsvals, muBU, 'b', 'linewidth', 1);
fill(augx, augy_TD, 1,'facecolor', 'r', 'edgecolor', 'none', 'facealpha', 0.4);
fill(augx, augy_BU, 1,'facecolor', 'c', 'edgecolor', 'none', 'facealpha', 0.4);
xticks([0:0.1:1]);
hold off

%Used for plotting each point
% plot(epsvals, transpose(TD(:,1)), 'g');
% hold on
% plot(epsvals, transpose(BU(:,1)), 'Color', [1 .5 .5]);
% for i = 2:30
%     plot(epsvals, transpose(TD(:, i)), 'g', 'HandleVisibility', 'off');
%     plot(epsvals, transpose(BU(:, i)), 'Color', [1, .5, .5], 'HandleVisibility', 'off');
% end
% plot(epsvals, muTD, 'Color', [0 0.5 0], 'LineWidth', 3);
% plot(epsvals, muBU, 'Color', [1 0 0], 'LineWidth', 3);
%title('Top-Down and Bottom-Up Transfer Entropy');

% Sets figure parameters
xlabel('global coupling coefficient (\epsilon)');
ylabel('transfer entropy (TE)');
legend('Average T_{M\rightarrow X}', 'Average T_{X\rightarrow M}', '95% CI for T_{M\rightarrow X}', '95% CI for T_{X\rightarrow M}');
