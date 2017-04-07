function db = findDaviesBoldinIndex(m, centroids, numGroups)
    distCentroids = zeros(numGroups, numGroups);
    internalDistances = zeros(numGroups, 1);
    for i = 1 : numGroups
        for j = i + 1 : numGroups
            dist = findDistance(centroids(i), centroids(j));
            distCentroids(i, j) = dist;
            distCentroids(j, i) = dist;
        end   
        
        %cluster=m(m==i);
        cluster = m{i};
        dist = 0;
        sizeCl = size(cluster, 1);
        for k = 1 : sizeCl
            dist = dist + findDistance(cluster(k), centroids(i));
        end    
        internalDistances (i) = dist / sizeCl;
          
    end   
    
    davies_bouldin = zeros(numGroups, numGroups); 
    for i = 1 : numGroups
        for j = i + 1 : numGroups
            index = (internalDistances(i) + internalDistances(j)) / distCentroids(i, j);
            davies_bouldin(i, j) = index;
            davies_bouldin(j, i) = index;
        end   
    end   
     
    sumMax = 0;
    for i = 1 : numGroups
        sumMax = sumMax + max(davies_bouldin(i, :));
    end
    
    db = sumMax / numGroups;
end 