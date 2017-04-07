function [ model] = train_dual_soft(x, y, lambda)
    K = x * x';
    n = size(x, 1);
    cvx_begin
        variables s(n)
        minimize(0.5 * (s .* y)' * K * (s .* y) - sum(s))
        subject to
            s >= 0
            s <= lambda
            sum(s .* y) == 0
    cvx_end
    % find weights
    w = x' * (s .* y);
    model.weights = w;
    % the threshold above zero to find support vectors
    eps=0.0001;
    % find support vectors
    temp = find(s > eps & s < lambda);
    if isempty(temp)
        model.bias = 0;
    else   
        %using support vectors find the bias using yi(aTxi - b) = 1.
        model.bias = (1/length(temp)) * sum((y(temp) .* (x(temp, :) * w) - ones(length(temp), 1)) ./ y(temp));
    end
    
    model.u = s;
   
end





