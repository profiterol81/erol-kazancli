clc;
clear;
close all;
data = load('example_dataset_2.mat');
x = data.('data');
y = data.('labels');
x = x';


lambda=1e-2;

disp(strcat('Lambda: ',num2str(lambda)));
[model] = train_primal_soft(x, y, lambda);

disp('Model obtained');
disp('w');
disp(model.weights);
disp('b');
disp(model.bias);
%Plot the dataset and the separating hyperplane
plot_data(model,y,x', strcat('Primal problem for soft margin, lambda: ', num2str(lambda)));


lambda=1;

disp(strcat('Lambda: ',num2str(lambda)));
[model] = train_primal_soft(x, y, lambda);

disp('Model obtained');
disp('w');
disp(model.weights);
disp('b');
disp(model.bias);
%Plot the dataset and the separating hyperplane
plot_data(model,y,x', strcat('Primal problem for soft margin, lambda: ', num2str(lambda)));


lambda=1e2;

disp(strcat('Lambda: ',num2str(lambda)));
[model] = train_primal_soft(x, y, lambda);

disp('Model obtained');
disp('w');
disp(model.weights);
disp('b');
disp(model.bias);
%Plot the dataset and the separating hyperplane
plot_data(model,y,x', strcat('Primal problem for soft margin, lambda: ', num2str(lambda)));


lambda= 10;
% lambda= exp(1) - 2;
% lambda= exp(1)^2;
[model] = train_primal_soft(x, y, lambda);
w=model.weights;
b=model.bias;
plot_data(model,y,x', strcat('Primal problem for soft margin, lambda: ', num2str(lambda)));
disp('Values of u')
disp(horzcat(model.u,(roundn( y.* (x * model.weights + model.bias),-3)<=1)));