close all
%load data reg_data_set_2
data = load('reg_data_set_2.mat');
x = data.('x');
y = data.('y');
r = linspace(0, 1);

middle = idivide(int32(length(x)), int32(2));
len = length(x);

xTrain = x(1:middle, 1);
yTrain = y(1:middle, 1);

xTest = x(middle:len, 1);
yTest = y(middle:len, 1);

errorTest = zeros(6, 1);
errorTrain = zeros(6, 1);
figure('Name', strcat('Polynomial - Validation Data'));
leg = cell(12,1);
for i = 1 : 6
    subplot(2,3,i);

    % find weights for polynomial degree i
    weights = polynomial_model(xTrain, yTrain, i);
    
    % plot the found polynomial and the validation data
    %figure('Name', strcat('Degree ', num2str(i), ' polynomial - Validation Data'));
    scatter(xTest, yTest,'rx');
    hold on;
    plot(r,polyval(transpose(flipud(weights)),r), 'k');
    title(strcat('Degree ', num2str(i)));
    % find the error calculated with the polynomial found using the
    % validation data
    yTestPol = polyval(transpose(flipud(weights)),xTest);
    diffTest = yTestPol - yTest;
    error = sqrt(transpose(diffTest) * diffTest);
    errorTest(i) = error;
        axis([0 1 -2 8])

end
hold off;
figure('Name', strcat('Polynomial - Training Data'));
for i = 1 : 6
        subplot(2,3,i);
     weights = polynomial_model(xTrain, yTrain, i);
    % plot the found polynomial and the training data
    %figure('Name', strcat('Degree ', num2str(i), ' polynomial - Training Data'));
    scatter(xTrain, yTrain,'bo');
    hold on;
    plot(r,polyval(transpose(flipud(weights)),r),'k');
    title(strcat('Degree ', num2str(i)));
        % find the error calculated with the polynomial found using the

    % find the error calculated with the polynomial found using the
    % tarining data
    yTrainPol = polyval(transpose(flipud(weights)),xTrain);
    diffTrain = yTrainPol - yTrain;
    error = sqrt(transpose(diffTrain) * diffTrain);
    errorTrain(i) = error;
            axis([0 1 -2 8])

end

figure('Name', strcat('Error vs. polynomial degree'));
r = [1; 2; 3; 4; 5; 6];
train=plot(r, errorTrain, 'b');
hold on;
scatter(r, errorTrain,'bo');
test=plot(r, errorTest, 'r');
scatter(r, errorTest, 'rx');
legend([train,test],'Traning data','Test data');
set(gca,'xtick',0:6)
