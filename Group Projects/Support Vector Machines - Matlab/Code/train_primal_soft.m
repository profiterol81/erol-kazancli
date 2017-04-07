function [ model ] = train_primal_soft(data, labels, lambda)
    d = size(data, 2);
    n = size(data, 1);
    % u are slack variables
    % w are weights
    % b is bias
    cvx_begin
        variables w(d) u(n) b
        minimize( 0.5 * w' * w + lambda * sum(u))
        subject to
            labels .* (data * w + b)  >= 1 - u
            u >= 0
    cvx_end
    
    model.weights = w;
    model.u = u;
    model.bias = b;
end





