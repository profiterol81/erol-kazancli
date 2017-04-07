function [ theta,historic_cost ]  = modified_gradient_descent(x,y,theta,t,tau)
%data size
N = length(y);
format long;
historic_cost = zeros(tau, 1);
for k = 1:tau
    
    
    H = (x * theta - y)';
    
    % Updating weights
    grad=(1/N) * H * x(:, 1);
    theta(1) = theta(1) - t *grad/norm(grad);
    grad1=(1/N) * H * x(:, 2);
    theta(2) = theta(2) - t * grad1/norm(grad1);
    
    % Storing cost
    historic_cost(k) =(x * theta - y)' * (x * theta - y) / (2 * N);
    
end

figure;
%Convergence curve
plot(1:tau,historic_cost);
title('Convergence curve')
%Final approximation
figure;
regressor=x*theta;
scatter(x(:, 2),y,'x');
hold on;
plot(x(:, 2),regressor)
title(strcat(strcat('w0=', num2str(theta(1)),', w1=', num2str(theta(2)))))
hold off;

end

