function [d1]  = replaceNaNWithMean(x)
    d1 = x;
    for i = 1: size(x, 2)
        dim = x(:, i);
        meanDim = nanmean(dim); % mean of dimension i excluding NaNs 
        dim(isnan(dim)) = meanDim; % replace NaN values with the mean
        d1(:, i) = dim;      
    end 
end    