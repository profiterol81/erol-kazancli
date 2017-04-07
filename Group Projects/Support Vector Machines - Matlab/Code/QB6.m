clc;
close all;
clear;
%Load dataset
load('example_dataset_3.mat');
data=data';
disp('Data size');
disp(size(data));
lambdas=[0,1e-2,1,10,1e2,1e3];
error_rates=zeros(1,size(lambdas,2));
weighted_error_rates=zeros(1,size(lambdas,2));
disp('Class 1');
pos=data(labels==1,:);
disp(size(pos));
disp('Class -1');
neg=data(labels==-1,:);
disp(size(neg));
for i=1 : size(lambdas,2)
    model=train_primal_soft_unbalanced(data,labels,lambdas(i));
    my_labels=test_primal_soft(model,data);
    error_rates(i)=error_rate(labels,my_labels);
    weighted_error_rates(i)=weighted_error_rate(labels,my_labels);
    plot_data( model, labels, data',strcat('Primal problem for soft margin, lambda: ', num2str(lambdas(i))));
end
disp('Error rates vs lambdas')
disp(vertcat(lambdas,error_rates));
figure;
plot(lambdas,error_rates, 'r');
hold on;
scatter(lambdas,error_rates, 'x','r');

title('Lambda value vs error rate');

disp('Weighted error rates vs lambdas')
disp(vertcat(lambdas,weighted_error_rates));
figure;
plot(lambdas,weighted_error_rates, 'r');
hold on;
scatter(lambdas,weighted_error_rates, 'x','r');

title('Lambda value vs weighted error rate');

best_lambda=lambdas(error_rates==min(error_rates));
best_lambda=best_lambda(1);
disp(strcat('Best lambda: ',num2str(best_lambda),', with error rate: ',num2str(min(error_rates))));

best_lambda=lambdas(weighted_error_rates==min(weighted_error_rates));
best_lambda=best_lambda(1);
disp(strcat('Best lambda: ',num2str(best_lambda),', with weighted error rate: ',num2str(min(weighted_error_rates))));
