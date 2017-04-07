function [kNearest] = acbrRetrievalPhase(newCase, caseBase, k)
    
    caseSize = size(caseBase, 1);
    
    % find all distances from casebase to the newcase
    distances = zeros(caseSize, 1);
    for i = 1 : caseSize 
        dist = findDistanceWithNominals(newCase, caseBase(i, :));
        distances(i) = dist;
    end 
    % sort distances
    [~,I] = sort(distances);
    
    % get the best k distances
    kNearest = I(1:k);
end       