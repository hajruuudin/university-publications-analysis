filename = 'h1_top_100_trends.csv';
data = readtable(filename);

% 2. Calculate Growth Rates (Year-over-Year)
% We calculate the percentage change between rows for the numeric columns
numericData = data{:, 2:end}; % Exclude publication_year
growthRates = diff(numericData) ./ numericData(1:end-1, :);
avgGrowth = mean(growthRates) * 100; % Convert to percentage

% 3. Calculate Basic Stats
minVals = min(numericData);
maxVals = max(numericData);
meanVals = mean(numericData);

% CAGR calculation: (Ending Value / Beginning Value)^(1/years) - 1
years = height(data) - 1;
cagr = ((numericData(end,:) ./ numericData(1,:)) .^ (1/years)) - 1;
cagrPercentage = cagr * 100;

% 4. Create a Summary Table
rowNames = {'Minimum'; 'Maximum'; 'Mean'; 'AAGR %'; 'CAGR &'};
summaryTable = table(rowNames, ...
    [minVals(1); maxVals(1); meanVals(1); avgGrowth(1); cagrPercentage(1)], ...
    [minVals(2); maxVals(2); meanVals(2); avgGrowth(2); cagrPercentage(2)], ...
    [minVals(3); maxVals(3); meanVals(3); avgGrowth(3); cagrPercentage(3)], ...
    'VariableNames', data.Properties.VariableNames);

% 5. Export to Excel with the summary at the bottom
filename = 'Research_Analysis_Report.xlsx';
writetable(data, filename, 'Sheet', 1, 'Range', 'A1');


% Determine where the data ends to place the summary
startRow = height(data) + 3;
writetable(summaryTable, filename, 'Sheet', 1, 'Range', ['A' num2str(startRow)]);

fprintf('Analysis complete. Report saved to %s\n', filename);