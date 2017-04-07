data = load('diabetes.mat');
x = data.('x');
y = data.('y');
x = x';
x = [ones(length(x),1) x];

disp('Question block 5');
fprintf(['Repeat the process in block 4 changing the order of some of the steps. i.e.  \n' ...
    'Preprocess the data replacing the NaN with the method D2, this time using \n' ...
    'only the data corresponding to the training set.\n']);

len = size(x, 1);
divPoint = round((len / 5) * 4); 
% 4 / 5 of the points form the training set, 
% the rest form the test set

xTr = x(1:divPoint, :);
yTr = y(1:divPoint, :);

xTest = x(divPoint:len, :);
yTest = y(divPoint:len, :);

[trainingX, testX]  = replaceNaNWithMeanTrainingSameClass(xTr, yTr, xTest, yTest);

% error and error percentage for training and test
[weights]  = thresholdRegression(trainingX, yTr);
[errorTr, errorPercentageTr] = findError(trainingX, yTr, weights);
[errorTest, errorPercentageTest] = findError(testX, yTest, weights);

disp('Weights:');
disp(weights');

disp('Training Error:');
disp(errorTr);

disp('Test Error:');
disp(errorTest);

