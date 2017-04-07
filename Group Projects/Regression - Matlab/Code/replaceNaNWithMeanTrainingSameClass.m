function [trainingX, testX]  = replaceNaNWithMeanTrainingSameClass(xTr, yTr, xTest, yTest)
    trainingX = xTr;
    testX = xTest;
    for i = 1: size(xTr, 2)
        dimTr = xTr(:, i);
        dimTest = xTest(:, i);
        % mean of dimension i for y == 1 class
        meanDim1 = nanmean(dimTr(yTr == 1));
        % mean of dimension i for y == -1 class
        meanDim2 = nanmean(dimTr(yTr == -1));
        % replace NaN values with the corrsponding mean
        nanIndTr = isnan(dimTr);
        dimTr(yTr == 1 & nanIndTr == 1) = meanDim1; 
        dimTr(yTr == -1 & nanIndTr == 1) = meanDim2; 
        trainingX(:, i) = dimTr;
        
        nanIndTest = isnan(dimTest);
        dimTest(yTest == 1 & nanIndTest == 1) = meanDim1; 
        dimTest(yTest == -1 & nanIndTest == 1) = meanDim2; 
        testX(:, i) = dimTest;       
    end  
     
end    