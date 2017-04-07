load('reg_data_set_1.mat')
%Exercise B.
%Linear regression
%X*w=Y w={w0,w1} w0+x*w1=y
w=polynomial_model(x,y,1);
 X = [ones(length(x),1) x];
% %w is the optimal value
% w = X\y;
disp('Optimal w values');
disp(w);

regressor=X*w;
scatter(x,y,'x');
hold on;
%2) Plot the data set and the line learned by the model.
plot(x,regressor)
title(strcat(strcat('w0=', num2str(w(1)),', w1=', num2str(w(2)))))
hold off;
%Calculate cost
cost=sum((regressor-y).^2)/size(y,1);

disp('Cost');
disp(cost);