function [caseBase, caseClasses, goodness] = acbrRetentionPhaseAR(newCase, estimate, caseBase, caseClasses, goodness)
    % always retain strategy((the new case is allways kept))
    caseBase = vertcat(caseBase, newCase);
    caseClasses = vertcat(caseClasses, estimate);
    goodness = vertcat(goodness, 0.5);  
end  