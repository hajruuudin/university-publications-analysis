%% Clear workspace
clear; clc;

%% Read data from CSV
T = readtable('h3_trends_1990_2025.csv');

years  = T.publication_year;
topics = T{:, 2:end};   % numeric data only

topicNames = {'Software Engineering', ...
              'Machine Learning & Data Mining', ...
              'Natural Language Processing', ...
              'Computer Networks', ...
              'Computer Communication', ...
              'Security'};

nYears = length(years);

%% Preallocate results
meanVals = mean(topics);
minVals  = min(topics);
maxVals  = max(topics);
AAGR     = zeros(1, size(topics,2));
CAGR     = zeros(1, size(topics,2));

%% Compute AAGR and CAGR
for i = 1:size(topics,2)
    values = topics(:,i);

    % Year-over-year growth rates
    growthRates = diff(values) ./ values(1:end-1);

    % Average Annual Growth Rate
    AAGR(i) = mean(growthRates);

    % Compound Annual Growth Rate
    CAGR(i) = (values(end) / values(1))^(1/(nYears-1)) - 1;
end

%% Create results table
resultsTable = table( ...
    meanVals', minVals', maxVals', AAGR', CAGR', ...
    'RowNames', topicNames, ...
    'VariableNames', {'Mean', 'Min', 'Max', 'AAGR', 'CAGR'});

%% Export to Excel
writetable(resultsTable, ...
           'CS_Research_Growth_Statistics.xlsx', ...
           'WriteRowNames', true);

disp('Excel file generated: CS_Research_Growth_Statistics.xlsx');