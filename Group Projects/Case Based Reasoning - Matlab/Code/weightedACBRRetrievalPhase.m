function [kNearest] = weightedACBRRetrievalPhase(newCase, caseBase, k, weight)
    
    caseSize = size(caseBase, 1);
    
    % find all distances from casebase to the newcase
    distances = zeros(caseSize, 1);
    for i = 1 : caseSize
        dist = findDistanceWithNominalsAndWeights(newCase, caseBase(i, :), weight);
        distances(i) = dist;
    end 
    % sort distances
    [~,I] = sort(distances);
    
    % get the best k distances
    kNearest = I(1:k);
end       