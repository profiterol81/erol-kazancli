function [caseBase, caseClasses, goodness] = acbrRetentionPhaseMG(newCase, estimate, kNearest, caseBase, caseClasses, numClasses, goodness)
    k = size(kNearest, 1);
    % find the maximum goodness value among the majority class later to
    % compare with the threshold value. If this value is lower than the
    % threshold the case will be kept
    newGoodness = -10;
    for j = 1 : k
        if (caseClasses(kNearest(j)) == estimate)
            if (goodness(kNearest(j)) > newGoodness)
                newGoodness = goodness(kNearest(j));
            end    
        end
    end   
    
    % find the max and min in the case base among the same group with the
    % found estimate
    maxGoodness = max(goodness(caseClasses==estimate));
    minGoodness = min(goodness(caseClasses==estimate));
    threshold = (maxGoodness + minGoodness) / 2;
    
    % if the goodness value is below the threshold found then keep the case
    % this threshold helps to increase the diversity if we have low
    % goodness values, prevents the increase of the cases if we have high
    % goodness values
    if newGoodness <= threshold
        caseBase = vertcat(caseBase, newCase);
        caseClasses = vertcat(caseClasses, estimate);
        goodness = vertcat(goodness, newGoodness);
    end    
    
end  