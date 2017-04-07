%arr: normalised data
%numGroups: number of clusters
function seeds = findInitialSeeds(arr, numGroups)
    sumDist = 0;
    %The iterations are done five times to get the best among the initial
    %seed choices
    for numIterations = 1 : 5
        arrSize = size(arr, 1);    
        r = randi([1,arrSize]);
        seeds = arr(r, :);
        
        %A new seed which is furthest to the previous seeds is found until
        %all the initial seeds are found this way
        for i = 1 : numGroups - 1
            distances = [];
            for x = 1 : arrSize
                prevDist = findDistance(arr(x, :), seeds(1, :));
                minDist = prevDist;
                for j = 2 : i
                    dist = findDistance(arr(x, :), seeds(j, :));
                    if dist < prevDist
                        prevDist = minDist;
                        minDist = dist;
                    end    
                end
                distances = [distances; minDist];
            end
            % The code below is our implementation of kmeans++ algorithm
            % but this did not give the desired optimal initial seeds, we
            % made a change to the algorith as below. 
            % distSqr = distances .* distances;
            % p = distSqr/sum(distSqr);
            % popArr = 1:arrSize;
            % index = randsample(popArr,1,true,p);  
            % randomCentroid = arr(index, :);
            % seeds = [seeds;randomCentroid];
            maxInd = [];
            [maxInd, I] = max(distances); 
            seeds = [seeds;arr(I, :)];
        end 
        prevSum = sumDist;
        sumDist = 0;
        for i = 1 : numGroups
            sumDist = sumDist + findDistance(seeds(i,:), seeds(mod(i, numGroups) + 1, :));
        end    
        if sumDist < prevSum 
            seeds = oldSeeds;
            sumDist = prevSum;
        else
            oldSeeds = seeds;
        end    
    end
   
end