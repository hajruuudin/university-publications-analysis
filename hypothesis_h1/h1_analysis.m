%% 1. Load Data
% Aggregated data for Graphs 1-4
filenameH1 = 'h1_top_100_trends.csv';
dataH1 = readtable(filenameH1);

% Specific benchmark data for Bonus Graph
data3D = readtable('bonus_3d_categories.csv');

% Extract variables for H1
yearsH1 = dataH1.publication_year;
cs = dataH1.computer_science;
med = dataH1.medicine;
bus = dataH1.business;

%% Graph 1-3: Individual Trends
figure('Name', 'Individual Category Trends', 'Color', 'w');

subplot(3,1,1);
plot(yearsH1, cs, '-o', 'Color', 'b', 'LineWidth', 2);
title('Computer Science Publication Growth (Top 100)');
grid on; ylabel('Records');

subplot(3,1,2);
plot(yearsH1, med, '-o', 'Color', 'r', 'LineWidth', 2);
title('Medicine Publication Growth (Top 100)');
grid on; ylabel('Records');

subplot(3,1,3);
plot(yearsH1, bus, '-o', 'Color', 'g', 'LineWidth', 2);
title('Business Publication Growth (Top 100)');
grid on; ylabel('Records'); xlabel('Year');

%% Graph 4: Comparison Graph (The "Story" Graph)
figure('Name', 'Comparative Analysis', 'Color', 'w');
hold on;
plot(yearsH1, cs, '-b', 'LineWidth', 2.5, 'DisplayName', 'Computer Science');
plot(yearsH1, med, '-r', 'LineWidth', 2.5, 'DisplayName', 'Medicine');
plot(yearsH1, bus, '-g', 'LineWidth', 2.5, 'DisplayName', 'Business');

xlabel('Year');
ylabel('Total Publications');
title('H1: Comparison of Research Categories in Top 100 Universities');
legend('Location', 'northwest');
grid on;
set(gca, 'FontSize', 12);
hold off;

%% Bonus Graph: 3D Comparison for Selected Benchmarks
% We need to pivot the data for the 3D plot
ranks = unique(data3D.rank);
years = unique(data3D.publication_year);
categories = {'computer_science', 'medicine', 'business'};
titles = {'Computer Science', 'Medicine', 'Business'};
colors = { 'winter', 'autumn', 'summer'}; % Different color themes for each

for k = 1:length(categories)
    % Pre-allocate Z matrix for current category
    Z = zeros(length(years), length(ranks));
    
    % Fill the matrix for the specific category
    currentCat = categories{k};
    for i = 1:length(ranks)
        for j = 1:length(years)
            val = data3D.(currentCat)(data3D.rank == ranks(i) & data3D.publication_year == years(j));
            if ~isempty(val)
                Z(j,i) = val;
            end
        end
    end

    % Create a new figure for each category
    figure('Name', ['3D Trend: ' titles{k}], 'Color', 'w');
    
    % Create the ribbon plot
    ribbon(years, Z);
    
    % Formatting
    title(['3D Evolution of ' titles{k} ' Research']);
    xlabel('University Rank');
    ylabel('Year');
    zlabel('Publications');
    
    % Set the rank labels
    set(gca, 'XTick', 1:5);
    set(gca, 'XTickLabel', {'Rank 1', 'Rank 10', 'Rank 25', 'Rank 50', 'Rank 75'});
    
    colormap(colors{k});
    grid on;
    view(45, 30);
end