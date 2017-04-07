clear;
clc;
close all;
disp('ACBR Algorithm with reduced data sets');
ACBRWeightedforFilename('HypothyroidSet.mat', 3, 'DDO');
ACBRWeightedforFilename('kr-vs-kpSet.mat', 5, 'MG');