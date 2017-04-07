% arr: normalized array data
% numGroups: number of groups
function [indexes,centroids,m, WGV, BGV] = fuzzycmeans(arr, numGroups)

    numFields = size(arr, 2);    

    m = cell(numGroups, 1);

    arrSize = size(arr, 1);
    
    indexes=zeros(size(arr,1),1);
    % First membership values randomly assigned
    membership = randi([1 1000], arrSize, numGroups);
    sumOfWeights = repmat(sum(membership, 2), 1, numGroups);
    membership = membership ./ sumOfWeights;
    
    %centroids are found (sum(weights * points) / sum(weights))
    sumWithWeights = arr' * membership;
    sumOfWeights = sum(membership, 1);
    centroids = (sumWithWeights ./ repmat(sumOfWeights, numFields, 1))'; 

    noChange = false;
    numberStep = 0;
    while ~noChange && numberStep < 100
        prevMembership = membership;
        
        distance = zeros(arrSize, numGroups);
        for i = 1 : arrSize
            currentRow = arr(i, :);
            for j = 1 : numGroups
                distance(i, j) = findDistance(currentRow, centroids(j, :));
            end
        end  
        
        for i = 1 : arrSize
            
            distDivided = zeros(numGroups, numGroups);
            
            dist = distance(i, :);
            
            % m = 1.5
            for j = 1 : numGroups
                for k = 1 : numGroups
                    distDivided(j, k) = (dist(j) / dist(k))^4;
                end
            end
            
            %change membership according to specified rule
            membership(i, :) = (1 ./ sum(distDivided, 2))';

        end
        
        %after all the assignments calculate the centroids again
        sumWithWeights = arr' * membership;
        sumOfWeights = sum(membership, 1);
        centroids = (sumWithWeights ./ repmat(sumOfWeights, numFields, 1))';
        
        numberStep = numberStep + 1;
        %check if the changes have become very small to end the program
        diff = abs(prevMembership - membership);
        maxDiff = max(diff(:));   
        if maxDiff < 0.01
            noChange = true;
        end 
    end
    
    %assign points to groups according to max memberships
    for i = 1 : arrSize
        [M,I] = max(membership(i, :));
        m{I} = [m{I}; arr(i, :)];
        indexes(i,:)=I;
    end    
    
    distance = zeros(arrSize, numGroups);
    for i = 1 : arrSize
        currentRow = arr(i, :);
        for j = 1 : numGroups
            distance(i, j) = findDistance(currentRow, centroids(j, :));
        end
    end  
    
    % Within group variability
    WGV = 0;
    for i = 1 : arrSize
        WGV = WGV + membership(1, :) * (distance(1, :).^2)';
    end   
    
    distCent = zeros(k, 1);
    meanPoints = mean(arr, 1);
    for i = 1 : k
        dist = findDistance(centroids(i, :), meanPoints);
        distCent(i) = dist;
    end   
    
    %Between group variability
    BGV = 0;
    for i = 1 : arrSize
        BGV = BGV + membership(1, :) * (distCent.^2);
    end   
    
    %The mean centroids are calculated to be able to be used in future
    %index analysis. These centroids are differen than the ones used above
    %in the algorithm.
    for i = 1 : numGroups
        if size(m{i}, 1) ~= 0  
            centroids(i, :) = mean(m{i}, 1);
        end
    end      
    
end