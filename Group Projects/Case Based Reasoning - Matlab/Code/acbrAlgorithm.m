function [testEstimates, caseBase, caseClasses, goodness] = acbrAlgorithm(caseBase, caseClasses, testData, k, policy)
 
    numClasses = size(unique(caseClasses), 1);
    caseSize = size(caseBase, 1);
    goodness = ones(caseSize, 1)/2; % initial goodness values set to 0.5
    
    testSize = size(testData, 1);
    learnRate = 0.2;
    testEstimates = zeros(size(testData, 1), 1);
    
    oblivion = false;
    
    if (strcmp(policy, 'NRO') || strcmp(policy, 'DDO') || strcmp(policy, 'MGO') || strcmp(policy, 'ARO'))      
        oblivion = true;
    end
    
    for i = 1 : testSize
        newCase = testData(i, :);
        % Retrieval: Find k nearest cases
        kNearest = acbrRetrievalPhase(newCase, caseBase, k);
        % Reuse: Assign the class of the nearest case
        % Revise is omitted because this is a classification problem.
        % estimate is the majority vote among the k nearest
        estimate = acbrReusePhase(caseClasses, kNearest);
        testEstimates(i) = estimate;
        % Review: goodness updated
        goodness = acbrReviewPhase(caseClasses, kNearest, estimate, goodness, learnRate); 
            
        if oblivion
            [caseBase, caseClasses, goodness, kNearest] = acbrOblivionPhase(kNearest, caseBase, caseClasses, goodness);
        end 
        if strcmp(policy, 'DD') || strcmp(policy, 'DDO')
            [caseBase, caseClasses, goodness] = acbrRetentionPhaseDD(newCase, estimate, kNearest, caseBase, caseClasses, numClasses, goodness);
        elseif strcmp(policy, 'MG') || strcmp(policy, 'MGO') 
            [caseBase, caseClasses, goodness] = acbrRetentionPhaseMG(newCase, estimate, kNearest, caseBase, caseClasses, numClasses, goodness);
        elseif strcmp(policy, 'AR') || strcmp(policy, 'ARO')
            [caseBase, caseClasses, goodness] = acbrRetentionPhaseAR(newCase, estimate, caseBase, caseClasses, goodness);
        else % 'NR'
            [caseBase, caseClasses, goodness] = acbrRetentionPhaseNR(caseBase, caseClasses, goodness);
        end
        
    end   
    
    
    
       
end 
