clear; close all; clc;
load 'diabetes.mat';

disp('Question block 1')
disp('Cardinality')
cardinality=size(x,2);
disp(cardinality);
disp('Dimensionality')
dimensionality=size(x,1);
disp(dimensionality);
disp('Mean Y');
disp(mean(y));
disp('Mean X');
disp((nanmean(x, 2))');