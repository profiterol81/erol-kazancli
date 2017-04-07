% arr: normalized array data
% numGroups: number of clusters
function [indexes, seeds,m, WGV, BGV] = my_kmeans(arr, numGroups)
    
    previousSeeds = zeros (numGroups, size(arr,2));
    seeds = zeros (numGroups, size(arr,2));
    indexes=zeros(size(arr,1),1);
    
    %Find optimal initial seeds by an algorithm similar to kmeans++
    [seeds] = findInitialSeeds(arr, numGroups);
    
    arrSize = size(arr, 1);
    
    %The code below is an alternative to the above line, but produces less
    %optimal results because of poor initial seed choice
 
    %indiceSeeds =  randperm(size(arr, 1), numGroups);    
    %for i = 1 : numGroups
    %   for j = 1 : size(arr,2)      
    %       seeds(i,j) = arr(indiceSeeds(i), j);      
    %   end 
    %end
    
    % Check if the previous seeds are different than the new ones
    while not(isequal(seeds, previousSeeds))
        
        % Initializes clusters and distance array
        dist = zeros(1, numGroups);
        m = cell(numGroups, 1); 
        % Calculate the distance of each point to each seed
        for i = 1 : arrSize

            point = arr (i,:);
            for j = 1 : numGroups
                dist(j) = findDistance(point, seeds(j, :));
            end
            
            % Retrieves the minimum distance array index
            minDist = find(dist == min(min(dist)) , 1);
            
            % Adds the point to the closest cluster
            m{minDist} = vertcat(m{minDist}, point);
            indexes(i,:)=minDist;
            
        end

        previousSeeds = seeds;
        
        % Calculate the new seeds
        for i = 1 : numGroups
            if size(m{i}, 2) ~= 0
                seeds(i, :) = mean(m{i}, 1);
            end
        end 
        
        % Within group variability
        distances = zeros(arrSize, 1);
        for i = 1 : arrSize
            currentRow = arr(i, :);
            distances(i, 1) = findDistance(currentRow, seeds(indexes(i), :));
        end 
        WGV = sum(distances.^2);
        
        %Between Group variability
        generalMean = mean(arr, 1);
        BGV = 0;
        for i = 1 : numGroups
            dist = findDistance(seeds(i, :), generalMean);
            BGV = BGV + dist^2*size(m{i}, 1);
        end 
        
    end

end