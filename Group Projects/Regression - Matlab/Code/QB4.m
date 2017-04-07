data = load('diabetes.mat');
x = data.('x');
y = data.('y');
x = x';
x = [ones(length(x),1) x];

disp('Question block 4');
fprintf(['Repeat the learning process in block 3 using just D2 but holding-out the \n' ... 
'last fifth of the data set for testing purposes, i.e. use the first 4/5-th for \n' ...
'training and the last 1/5-th for testing.\n' ]);

[d2] = replaceNaNWithMeanSameClass(x, y);

len = size(d2, 1);
divPoint = round((len / 5) * 4); 
% 4 / 5 of the points form the training set, 
% the rest form the test set

trainingX = d2(1:divPoint, :);
trainingY = y(1:divPoint, :);

testX = d2(divPoint:len, :);
testY = y(divPoint:len, :);

% error and error percentage for training and test
[weights]  = thresholdRegression(trainingX, trainingY);
[errorTr, errorPercentageTr] = findError(trainingX, trainingY, weights);
[errorTest, errorPercentageTest] = findError(testX, testY, weights);

disp('Weights:');
disp(weights');

disp('Training Error:');
disp(errorTr);

disp('Test Error:');
disp(errorTest);
