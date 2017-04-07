function [weights]  = thresholdRegression(x, y)

    weights = inv(x'*x) * (x')*y;
      
end    