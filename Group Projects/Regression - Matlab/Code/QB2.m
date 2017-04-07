data = load('diabetes.mat');
x = data.('x');
y = data.('y');
x = x';
x = [ones(length(x),1) x];

disp('Question block 2');

disp('Create d1, replacing NaN for the average of that attribute');
[d1] = replaceNaNWithMean(x);
meansXd1 = mean(d1, 1);

disp('D1 mean');
disp(meansXd1(1, 2:size(meansXd1, 2)));

disp('Create d2, replacing NaN for the average of the attribute for that class');
[d2] = replaceNaNWithMeanSameClass(x, y);
meansXd2 = mean(d2, 1);

disp('D2 mean');
disp(meansXd2(1, 2:size(meansXd2, 2)));

disp('Create d3, replacing NaN for the median of the attribute for that class');
[d3] = replaceNaNWithMedian(x, y);
meansXd3 = mean(d3, 1);

disp('D3 mean');
disp(meansXd3(1, 2:size(meansXd3, 2)));


