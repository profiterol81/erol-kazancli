clc;
clear;
close all;
data = load('example_dataset_1.mat');
x = data.('data');
y = data.('labels');
x = x';

lambda=0;
disp(strcat('Lambda: ',num2str(lambda)));
[model] = train_primal_soft(x, y, lambda);

disp('Model obtained');
disp('w');
disp(model.weights);
disp('b');
disp(model.bias);
%Plot the dataset and the separating hyperplane
plot_data(model,y,x',strcat('Primal problem for soft margin, lambda: ', num2str(lambda)));

load('toy_dataset.mat');

lambda=0;
data=data';
%Training
model=train_primal_soft(data,labels,lambda);

disp('Model obtained');
disp('w');
disp(model.weights);
disp('b');
disp(model.bias);
%Plot the dataset and the separating hyperplane

plot_data(model,labels,data', strcat('Primal problem for soft margin, lambda: ', num2str(lambda)));


data = load('example_dataset_1.mat');
x = data.('data');
y = data.('labels');
x = x';

class1 = x(y == 1, :);
class2 = x(y == -1, :);
lambda=1e-2;

disp(strcat('Lambda: ',num2str(lambda)));
[model] = train_primal_soft(x, y, lambda);

disp('Model obtained');
disp('w');
disp(model.weights);
disp('b');
disp(model.bias);
%Plot the dataset and the separating hyperplane
plot_data(model,y,x',strcat('Primal problem for soft margin, lambda: ', num2str(lambda)));


lambda=1;

disp(strcat('Lambda: ',num2str(lambda)));
[model] = train_primal_soft(x, y, lambda);

disp('Model obtained');
disp('w');
disp(model.weights);
disp('b');
disp(model.bias);
%Plot the dataset and the separating hyperplane
plot_data(model,y,x',strcat('Primal problem for soft margin, lambda: ', num2str(lambda)));


lambda=1e2;

disp(strcat('Lambda: ',num2str(lambda)));
[model] = train_primal_soft(x, y, lambda);

disp('Model obtained');
disp('w');
disp(model.weights);
disp('b');
disp(model.bias);
%Plot the dataset and the separating hyperplane
plot_data(model,y,x',strcat('Primal problem for soft margin, lambda: ', num2str(lambda)));

disp('Values of u')
disp(horzcat(model.u,(roundn( y.* (x * model.weights + model.bias),-3)<=1)));