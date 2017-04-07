data = load('diabetes.mat');
x = data.('x');
y = data.('y');
x = x';
x = [ones(length(x),1) x];

disp('Question block 6');
fprintf(['Repeat the process in Block 5 changing the percentage of the data for training and testing. \n' ...
'Plot a graph with the training and test error rates for each splitting percentage point. \n']);

trainingError = zeros(5, 1);
testError = zeros(5, 1);
eUpperBound = zeros(5, 1);

for i = 1 : 5
    len = size(x, 1);
    divPoint = round((len / (10)) * (10-i)); 
    % (10 - i) / 10 of the points form the training set, 
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

    dVC = (size(trainingX, 2) - 1) + 1; % d + 1
    n = size(trainingX, 1);

    trainingError(i) = errorTr;
    testError(i) = errorTest;
    eUpperBound(i) = errorTr + sqrt(((dVC * (log(2*n / dVC) + 1)) + log(2/0.05))/(2*n));
    
end;

percentages = [50;60;70;80;90];
trainingError = flipud(trainingError);
testError = flipud(testError);
eUpperBound = flipud(eUpperBound);

figure;

train=plot(percentages, trainingError, 'b');
xlabel('Training Percentage');
ylabel('Error');
hold on;
scatter(percentages, trainingError,'bo');
test=plot(percentages, testError, 'r');
scatter(percentages, testError, 'rx');
legend([train,test],'Traning error','Test error');

fprintf(['Add to the plot the upper bound on the generalization error using the equation \n' ...
'of the slides for VC dimension equal to d + 1. \n']);

figure;
train2=plot(percentages, trainingError, 'b');
xlabel('Training Percentage');
ylabel('Error');
hold on;
scatter(percentages, trainingError,'bo');
test2=plot(percentages, testError, 'r');
scatter(percentages, testError, 'rx');
upper=plot(percentages, eUpperBound, 'c');
scatter(percentages, testError, 'cd');

legend([train2,test2, upper],'Traning error','Test error', 'Upper bound');

disp('How many samples does the bound predict?');

prob = 0.05; % confidence 95%
errVar = 0.01; % variance 1%

% note that the error equation here seems different than the one used above
% but it is the same function converted using the log addition and
% multiplication properties. This had to be done, because the other
% equation was not resolved by matlab but this one was. And with this equation
% solve function gave the correct answers to the equation. 
syms n; 
sol1 = solve(errVar == sqrt((log((2*n*exp(1) / dVC)^dVC * (2/prob)))/(2*n)), n) ;

prob = 0.5; % confidence 50%
errVar = 0.01; % variance 1%

syms n; 
sol2 = solve(errVar == sqrt((log((2*n*exp(1) / dVC)^dVC * (2/prob)))/(2*n)), n) ;

prob = 0.05; % confidence 95%
errVar = 0.05; % variance 5%

syms n; 
sol3 = solve(errVar == sqrt((log((2*n*exp(1) / dVC)^dVC * (2/prob)))/(2*n)), n) ;

prob = 0.05; % confidence 95%
errVar = 0.1; % variance 10%

syms n; 
sol4 = solve(errVar == sqrt((log((2*n*exp(1) / dVC)^dVC * (2/prob)))/(2*n)), n) ;  

disp('Confidence:95% Error Variance:1%');
disp('Minimum Sample Size:');
disp(round(sol1));

disp('Confidence:50% Error Variance:1%');
disp('Minimum Sample Size:');
disp(round(sol2));

disp('Confidence:95% Error Variance:5%');
disp('Minimum Sample Size:');
disp(round(sol3));

disp('Confidence:95% Error Variance:10%');
disp('Minimum Sample Size:');
disp(round(sol4));


