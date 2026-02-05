%% Hypothesis 2: Analysing the fluctuation of research publications by uni ranges
close all; clc; clear;

%% 1. Load data
dataTrends = readtable('h2_uni_range_trends.csv');
dataHeatmap = readtable('h2_heatmap_data.csv');

cyanDark  = [0, 0.45, 0.55];  % Tier 1
cyanMed   = [0, 0.65, 0.75];  % Tier 2
cyanLight = [0.3, 0.8, 0.8];  % Tier 3

%% Figure 1: Grouped Bar Charts (Total Volume Comparison)
categories = {'total_cs', 'total_med', 'total_bus'};
catLabels = {'Computer Science', 'Medicine', 'Business'};
tiers = unique(dataTrends.uni_range);

barData = [];
for i = 1:length(tiers)
    temp = dataTrends(strcmp(dataTrends.uni_range, tiers{i}), :);
    barData(i, :) = [sum(temp.total_cs), sum(temp.total_med), sum(temp.total_bus)];
end

figure('Name', 'Research Volume by Tier', 'Color', 'w', 'Units', 'centimeters', 'Position', [1, 1, 20, 15]);
b = bar('barData', 'FaceColor', 'flat');

b(1).FaceColor = cyanDark;  % Tier 1
b(2).FaceColor = cyanMed;   % Tier 2
b(3).FaceColor = cyanLight; % Tier 3

set(gca, 'XTickLabel', catLabels, 'FontSize', 11, 'Box', 'off');
title('Total Research Output by University Ranking Tier (2006-2025)', 'FontSize', 13, 'FontWeight', 'bold');
ylabel('Total Publications (Cumulative)');
legend(tiers, 'Location', 'northwest', 'Box', 'off');
grid on;

%% Figure 2: Enhanced Binned Research Intensity Heatmap
figure('Name', 'Binned Research Intensity', 'Color', 'w', 'Units', 'centimeters', 'Position', [1, 1, 22, 14]);

h = heatmap(dataHeatmap, 'publication_year', 'rank_bin', ...
    'ColorVariable', 'total_pubs', ...
    'FontSize', 10);

% Manually order the Y-axis so 51-100 follows 1-50 correctly
h.YDisplayData = {'1-50', '51-100', '101-150', '151-200', '201-250', ...
                  '251-300', '301-350', '351-400', '401-450'};

% --- ENHANCED CONTRAST (SENSITIVITY) ---
% We use a log-like color scaling or manually set limits to show more detail.
h.ColorLimits = [min(dataHeatmap.total_pubs), max(dataHeatmap.total_pubs) * 0.85];

% Custom High-Contrast Palette (Deep Blue to Neon Cyan to White)
h.Colormap = [parula(256)];

% Formatting
h.Title = 'Longitudinal Research Concentration by Ranking Brackets (2006-2025)';
h.XLabel = 'Year';
h.YLabel = 'University Ranking Range';
h.CellLabelFormat = '%.0f'; 
h.GridVisible = 'on';
