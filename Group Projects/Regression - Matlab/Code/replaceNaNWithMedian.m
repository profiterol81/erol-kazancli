function [d3]  = replaceNaNWithMedian(x, y)
    d3 = x;
    for i = 1: size(x, 2)
        dim = x(:, i); % mean of dimension i for y == 1 class
        medianDim1 = nanmedian(dim(y == 1)); % mean of dimension i for y == -1 class
        medianDim2 = nanmedian(dim(y == -1)); % replace NaN values with the corrsponding mean
        nanInd = isnan(dim);
        dim(y == 1 & nanInd == 1) = medianDim1; 
        dim(y == -1 & nanInd == 1) = medianDim2; 
        d3(:, i) = dim;     
    end  
end
