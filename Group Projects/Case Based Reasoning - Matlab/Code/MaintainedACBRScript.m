clear;
clc;
close all;
disp('ACBR Algorithm with reduced data sets');
MaintainedACBRforFilename('HypothyroidSet.mat', 3, 'NR', 'DDO');
MaintainedACBRforFilename('kr-vs-kpSet.mat', 5, 'NR','MG');