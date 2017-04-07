function [error, errorPercentage]  = findError(x, y, weights)

    fx = sign(x * weights);
    errorVector = y ~= fx;
    error = sum(errorVector) / size(x, 1);
    errorPercentage = (error / size(x, 1)) * 100 ;
      
end    