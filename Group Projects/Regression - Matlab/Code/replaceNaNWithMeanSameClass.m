function [d2]  = replaceNaNWithMeanSameClass(x, y)
    d2 = x;
    for i = 1: size(x, 2)
        dim = x(:, i); % mean of dimension i for y == 1 class
        meanDim1 = nanmean(dim(y == 1)); % mean of dimension i for y == -1 class
        meanDim2 = nanmean(dim(y == -1)); % replace NaN values with the corrsponding mean
        nanInd = isnan(dim);
        dim(y == 1 & nanInd == 1) = meanDim1; 
        dim(y == -1 & nanInd == 1) = meanDim2; 
        d2(:, i) = dim;     
    end  
     
end    