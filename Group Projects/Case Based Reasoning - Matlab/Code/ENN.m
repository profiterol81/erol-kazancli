function [flaggedIndexes] = ENN(caseBase, caseClasses, distances, k, flaggedIndexes)

    dataSize = size(caseBase, 1);
    
    % find k-nearest neighbours for each x and check their classes, if the majority class is not the same
    % as the class of x, then flag x to be deleted from the caseBase
    for i = 1 : dataSize
        distRow = distances(i, :);
        [~,I] = sort(distRow);
        C = zeros(2, 1);
        a = k + 1;
         % if more than 1 majority votes repeat decreasing k
        while size(C, 1) > 1
            kclasses = caseClasses(I(2:a)); % start from 2 because the first one is the distance to itself
            [majorityEst, ~, C2] = mode(kclasses);
            C = cell2mat(C2);
            a = a - 1; % if more than one majority votes decrease k
        end
            
        if caseClasses(i) ~= majorityEst
            % points flagged as 1 will be deleted
            flaggedIndexes(i) = 1;
        end      
    end 

end       