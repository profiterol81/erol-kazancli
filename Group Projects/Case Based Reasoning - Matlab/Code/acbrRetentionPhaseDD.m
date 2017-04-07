function [caseBase, caseClasses, goodness] = acbrRetentionPhaseDD(newCase, estimate, kNearest, caseBase, caseClasses, numClasses, goodness)
    k = size(kNearest, 1);
    % we found the estimate based on the majority voting
    % therefore now it is enough to count the ones which are equal to
    % estimate
    majority = sum(caseClasses(kNearest) == estimate);
    remaining = k - majority;
    disagreement = remaining / ((numClasses - 1) * majority);
    threshold = 0.2;
    % find the maximum goodness value among the majority class later to
    % assign this value to the goodness of the new case if retained
    newGoodness = -10;
    for j = 1 : k
        if (caseClasses(kNearest(j)) == estimate)
            if (goodness(kNearest(j)) > newGoodness)
                newGoodness = goodness(kNearest(j));
            end    
        end
    end   
    % if there is a high disagreement as to the class of the new case add
    % it to the case base. i.e retain it
    if disagreement > threshold
        caseBase = vertcat(caseBase, newCase);
        caseClasses = vertcat(caseClasses, estimate);
        goodness = vertcat(goodness, newGoodness);
    end    
    
end  