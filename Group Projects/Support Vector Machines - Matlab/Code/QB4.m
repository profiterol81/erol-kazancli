clc;
clear;
close all;

data = load('example_dataset_2.mat');
x = data.('data');
y = data.('labels');
x = x';

class1 = x(y == 1, :);
class2 = x(y == -1, :);

figure;
scatter(class1(:, 1), class1(:, 2), 'x');
hold on;
scatter(class2(:, 1), class2(:, 2), 'o');
% lambda = 0.001;
lambda=1e-2;
% lambda= exp(1) - 2;
% lambda= exp(1)^2;
[model] = train_dual_soft(x, y, lambda);
plot_data(model,y,x',strcat('Dual problem for soft margin, lambda: ', num2str(lambda)));



lambda= 1;
% lambda= exp(1) - 2;
% lambda= exp(1)^2;
[model] = train_dual_soft(x, y, lambda);
plot_data(model,y,x',strcat('Dual problem for soft margin, lambda: ', num2str(lambda)));

lambda=1e2;
% lambda= exp(1) - 2;
% lambda= exp(1)^2;
[model] = train_dual_soft(x, y, lambda);
plot_data(model,y,x',strcat('Dual problem for soft margin, lambda: ', num2str(lambda)));

lambda=10;
% lambda= exp(1) - 2;
% lambda= exp(1)^2;
[model] = train_dual_soft(x, y, lambda);
plot_data(model,y,x',strcat('Dual problem for soft margin, lambda: ', num2str(lambda)));

disp('Values of u')
disp(horzcat(model.u,(roundn( y.* (x * model.weights + model.bias),-3)<=1)));
