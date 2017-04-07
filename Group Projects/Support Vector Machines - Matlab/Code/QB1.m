clc;
clear;
close all;
data = load('example_dataset_1.mat');
x = data.('data');
y = data.('labels');
x = x';

class1 = x(y == 1, :);
class2 = x(y == -1, :);

[model] = train_primal_hard(x, y);
w=model.weights;
b=model.bias;
disp('Model obtained');
disp('w');
disp(model.weights);
disp('b');
disp(model.bias);
%Plot the dataset and the separating hyperplane
plot_data(model,y,x','Primal problem for hard margin');
