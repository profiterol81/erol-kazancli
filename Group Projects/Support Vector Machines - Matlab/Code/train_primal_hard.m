function [model] = train_primal_hard(data, labels)

    d = size(data, 2);
    cvx_begin
        variable w(d)
        variable b
        minimize( w' * w )
        subject to
            (data * w + b).* labels >= 1
    cvx_end
    
    model.weights = w;
    model.bias=b;
end





