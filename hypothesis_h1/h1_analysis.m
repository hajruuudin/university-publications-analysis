%% Hypothesis 1: Analysing the annual number of research papers per category for the top 100 institutions
close all; clc;

%% Loading Data & Initialisation
% Aggregated data for Graphs 1-4
filenameH1 = 'h1_top_100_trends.csv';
dataH1 = readtable(filenameH1);
data3D = readtable('bonus_3d_categories.csv');

% For Graph 1 and for Graph 2: Increase in research papers and area chart
% for the cumulative number of research papers per year
yearsH1 = dataH1.publication_year;
cs = dataH1.computer_science;
med = dataH1.medicine;
bus = dataH1.business;

% For the last three graphs, the 3D plots
ranks = unique(data3D.rank);
years = unique(data3D.publication_year);

%% Figure 1: Longitudinal increase in publications within top 100 institutions per category
figure('Name', 'Category Growth Analysis', 'Color', 'w', 'Units', 'centimeters', 'Position', [1, 1, 24, 12]);

fontName = 'Helvetica';
fontSize = 10;
lineWidth = 2;

cyanDark  = [0, 0.45, 0.55];  % Deep Teal for CS
cyanMed   = [0, 0.65, 0.75];  % Classic Cyan for Med
cyanLight = [0.3, 0.8, 0.8];  % Aqua for Business

% --- Subplot 1: Computer Science ---
subplot(3,1,1);
h1 = area(yearsH1, cs, 'FaceColor', cyanDark, 'FaceAlpha', 0.3, 'EdgeColor', cyanDark, 'LineWidth', lineWidth);
hold on;
plot(yearsH1, cs, 'o', 'MarkerSize', 4, 'MarkerFaceColor', cyanDark, 'MarkerEdgeColor', 'w');
p = polyfit(yearsH1, cs, 1);
plot(yearsH1, polyval(p, yearsH1), ':', 'Color', [0.2 0.2 0.2], 'LineWidth', 1.2);
title('A. Computer Science: Longitudinal Publication Growth', 'FontSize', 12, 'FontWeight', 'bold');
ylabel('Annual Publications');
grid on; set(gca, 'FontName', fontName, 'FontSize', fontSize, 'Box', 'off');

% --- Subplot 2: Medicine ---
subplot(3,1,2);
h2 = area(yearsH1, med, 'FaceColor', cyanMed, 'FaceAlpha', 0.3, 'EdgeColor', cyanMed, 'LineWidth', lineWidth);
hold on;
plot(yearsH1, med, 's', 'MarkerSize', 4, 'MarkerFaceColor', cyanMed, 'MarkerEdgeColor', 'w');
p = polyfit(yearsH1, med, 1);
plot(yearsH1, polyval(p, yearsH1), ':', 'Color', [0.2 0.2 0.2], 'LineWidth', 1.2);
title('B. Medicine: Longitudinal Publication Growth', 'FontSize', 12, 'FontWeight', 'bold');
ylabel('Annual Publications');
grid on; set(gca, 'FontName', fontName, 'FontSize', fontSize, 'Box', 'off');

% --- Subplot 3: Business ---
subplot(3,1,3);
h3 = area(yearsH1, bus, 'FaceColor', cyanLight, 'FaceAlpha', 0.3, 'EdgeColor', cyanLight, 'LineWidth', lineWidth);
hold on;
plot(yearsH1, bus, '^', 'MarkerSize', 4, 'MarkerFaceColor', cyanLight, 'MarkerEdgeColor', 'w');
p = polyfit(yearsH1, bus, 1);
plot(yearsH1, polyval(p, yearsH1), ':', 'Color', [0.2 0.2 0.2], 'LineWidth', 1.2);
title('C. Business Science: Longitudinal Publication Growth', 'FontSize', 12, 'FontWeight', 'bold');
ylabel('Annual Publications'); xlabel('Year');
grid on; set(gca, 'FontName', fontName, 'FontSize', fontSize, 'Box', 'off');


linkaxes(findall(gcf,'Type','axes'),'x');

%% Figure 2: Longitudinal Research Composition (Stacked Graph)
figure('Name', 'Comparative Research Volume', 'Color', 'w', 'Units', 'centimeters', 'Position', [1, 1, 24, 16]);

y_stacked = [cs, med, bus]; 

% Create the stacked area plot
h = area(yearsH1, y_stacked, 'LineStyle', '-', 'LineWidth', 0.1);

h(1).FaceColor = [0, 0.4, 0.5];    % Deep Teal (Computer Science)
h(2).FaceColor = [0, 0.6, 0.7];    % Medium Cyan (Medicine)
h(3).FaceColor = [0.4, 0.8, 0.8];  % Aqua (Business)

% Professional Styling
title('Evolution of Research Volume in Top 100 Universities (2006-2025)', ...
      'FontSize', 14, 'FontWeight', 'bold', 'FontName', 'Helvetica');
xlabel('Year', 'FontSize', 12);
ylabel('Cumulative Number of Publications', 'FontSize', 12);

% Legend matching the stack order (Reverse of the matrix order for clarity)
legend({'Computer Science', 'Medicine', 'Business'}, ...
       'Location', 'northwest', 'FontSize', 11, 'Box', 'off');

grid on;
set(gca, 'Layer', 'top');
set(gca, 'Box', 'off', 'TickDir', 'out', 'FontSize', 11);

% Vertical line indicating the appearance and increase of use in AI
% technology
xline(2021, '--w', 'AI Transformer Era', 'LabelVerticalAlignment', 'bottom', 'LineWidth', 1.5, 'HandleVisibility', 'off');

% Shaded area representing the activity of the COVID pandemic
v = patch([2019 2022 2022 2019], [0 0 max(ylim) max(ylim)], [0.9 0.9 0.9]);
v.FaceAlpha = 1.0;
v.EdgeColor = 'none';
set(v, 'HandleVisibility', 'off');
uistack(v, 'bottom');
text(2019, max(ylim)*0.95, 'Pandemic Surge', 'FontWeight', 'bold', 'Color', [0.3 0.3 0.3]);

%% Bonus - Figure 3: 3D Ribbon Analysis of selected UNIS and their research statistics
% Here we take 5 differently ranked universities and asses their
% publication statistics. The unis choosen are based on the ranks 1, 10,
% 25, 50 and 75 which gives us a nice spread of data. THIS GRAPH IS MORE
% FOR SHOWCASE RATHER THAN CONCLUSION

categories = {'computer_science', 'medicine', 'business'};
titles = {'Computer Science', 'Medicine', 'Business'};

cyanMap = [
    0.00, 0.30, 0.40; % Rank 1 (Darkest)
    0.00, 0.50, 0.60; % Rank 10
    0.00, 0.70, 0.80; % Rank 25
    0.20, 0.85, 0.90; % Rank 50
    0.50, 0.95, 1.00  % Rank 75 (Lightest)
];

for k = 1:length(categories)
    Z = zeros(length(years), length(ranks));
    currentCat = categories{k};
    
    for i = 1:length(ranks)
        for j = 1:length(years)
            val = data3D.(currentCat)(data3D.rank == ranks(i) & data3D.publication_year == years(j));
            if ~isempty(val)
                Z(j,i) = val;
            end
        end
    end

    figure('Name', ['3D Ribbon: ' titles{k}], 'Color', 'w', 'Units', 'inches', 'Position', [2, 2, 8, 6]);
    
    % Create ribbons with a slightly slimmer width (0.6) for elegance
    h = ribbon(years, Z, 0.6);
    
    % Loop through each ribbon to apply colors and styles
    for i = 1:length(h)
        set(h(i), 'FaceColor', cyanMap(i,:), ... 
                  'EdgeColor', 'none', ...
                  'FaceAlpha', 0.8);
        
        text(i, years(1), Z(1,i), sprintf('  Rank %d', ranks(i)), ...
            'FontSize', 9, 'FontWeight', 'bold', 'Color', 'black');
    end
    
    title(['Longitudinal Benchmark: ' titles{k}], 'FontSize', 14, 'FontWeight', 'bold');
    ylabel('Year'); 
    zlabel('Annual Publications');
    
    set(gca, 'XTick', []); 
    
    % Set perspective and lighting
    view(-35, 40); 
    grid on;
    camlight headlight; lighting flat;
    set(gca, 'Projection', 'perspective', 'Box', 'off');
end