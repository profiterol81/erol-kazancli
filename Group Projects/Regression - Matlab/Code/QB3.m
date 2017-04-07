data = load('diabetes.mat');
x = data.('x');
y = data.('y');
x = x';
x = [ones(length(x),1) x];

[d1] = replaceNaNWithMean(x);
[d2] = replaceNaNWithMeanSameClass(x, y);
[d3] = replaceNaNWithMedian(x, y);

disp('Question block 3')

disp('Report the normal vector of the separating hyperplane for each data set D1, D2, D3.');
[weightsD1]  = thresholdRegression(d1, y);
[errorD1, ~] = findError(d1, y, weightsD1);

normalVectorD1=weightsD1(2:size(weightsD1,1));
thresholdD1= -weightsD1(1);

disp('Normal vector for D1')
disp(normalVectorD1');
disp('Threshold for D1')
disp(thresholdD1);

[weightsD2]  = thresholdRegression(d2, y);
[errorD2, ~] = findError(d2, y, weightsD2);

normalVectorD2=weightsD2(2:size(weightsD2,1));
thresholdD2= -weightsD2(1);

disp('Normal vector for D2')
disp(normalVectorD2');
disp('Threshold for D2')
disp(thresholdD2);

[weightsD3]  = thresholdRegression(d3, y);
[errorD3, ~] = findError(d3, y, weightsD3);

normalVectorD3=weightsD3(2:size(weightsD3,1));
thresholdD3= -weightsD3(1);

disp('Normal vector for D3')
disp(normalVectorD3');
disp('Threshold for D3')
disp(thresholdD3);

fprintf(['Compute the error rates achieved on the training data. Are there significant differences? \n' ...
'Report the method used and their parameters. \n']);

disp('Error Rate(D1):');
disp(errorD1);

disp('Error Rate(D2):');
disp(errorD2);

disp('Error Rate(D3):');
disp(errorD3);



