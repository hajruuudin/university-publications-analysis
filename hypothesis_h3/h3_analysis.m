%% Hypothesis 3: Revised
filename = 'h3_trends_1990_2025.csv'; 
data = readtable(filename);

year = data.publication_year;

Y_filtered = [data.se, data.mldm, data.nlp, data.cn, data.cc, data.sec];
Y_smooth = movmean(Y_filtered, 3, 1);
labels_filtered = {'Software Eng.', 'ML & Disc. Math', 'Neural Nets & NLP', 'Networking', 'Cloud Computing', 'Cybersecurity'};

colors_filtered = [
    0.00, 0.15, 0.30;
    0.00, 0.40, 0.60;
    0.00, 1.00, 1.00;
    0.00, 0.55, 0.45;
    0.00, 0.45, 0.50;
    0.00, 0.50, 0.55;
];

%% Figure 1: Streamgraph to visualise cumulative research of individual topics as well as their share inside the total
figure('Color', 'w', 'Name', 'Revised CS Streamgraph');
total_per_year = sum(Y_filtered, 2);
baseline = -total_per_year / 2;

hold on;
curr_base = baseline;
for i = 1:size(Y_filtered, 2)
    fill([year; flipud(year)], [curr_base; flipud(curr_base + Y_filtered(:,i))], ...
         colors_filtered(i,:), 'EdgeColor', 'none', 'FaceAlpha', 0.85);
    curr_base = curr_base + Y_filtered(:,i);
end
title('Evolution of CS Specialty Fields', 'FontSize', 14);
xlabel('Year'); ylabel('Thematic Volume');
legend(labels_filtered, 'Location', 'southoutside', 'Orientation', 'horizontal');
grid on; set(gca, 'YTickLabel', []);
hold off;

%% Figure 2: 100% Stacked Bar Chart to visualise the percentage share of research topics
figure('Color', 'w', 'Name', 'Market Share');
Y_percent = (Y_filtered ./ sum(Y_filtered, 2)) * 100;

b = bar(year, Y_percent, 'stacked', 'EdgeColor', 'none');
for k = 1:length(b)
    b(k).FaceColor = colors_filtered(k,:);
end
title('Topic Displacement of CS research topics', 'FontSize', 14);
ylabel('Market Share (%)'); xlabel('Year');
legend(labels_filtered, 'Location', 'eastoutside');