close all;
%load data reg_data_set_1
data = load('reg_data_set_1.mat');
x = data.('x');
y = data.('y');

% find weights for polynomial degree 3

weights = polynomial_model(x, y, 3);
disp('Optimal value for the weights')
disp(weights);
r = linspace(0, 1);
figure;
scatter(x,y);
hold on;
plot(r,polyval(transpose(flipud(weights)),r));



