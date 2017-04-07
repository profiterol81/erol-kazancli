function [distDTW, DTW, shortestPath] = findDistanceDTW(sequence1, sequence2)
    size1 = size(sequence1, 1);
    size2 = size(sequence2, 1);
    distEuc = zeros(size1, size2);
    DTW = zeros(size1, size2);
    for i=1:size1
        for j=1:size2
            distEuc(i, j) = findEuclideanDistance(sequence1(i, :), sequence2(j, :));
        end
    end   
    
    DTW(1, 1) = distEuc(1, 1);
    for i=1:size1
        if i == 1
            startJ = 2;
        else
            startJ = 1;
        end    
        for j=startJ:size2
            valueTop = Inf;
            valueLeft = Inf;
            valueDiag = Inf;
            if i > 1
                valueTop = DTW(i-1,j);
            end    
            if j > 1
                valueLeft = DTW(i,j-1);
            end 
            if i > 1 && j > 1
                valueDiag = DTW(i-1,j-1);
            end    
            minValue = min([valueTop valueLeft valueDiag]);
            DTW(i, j) = distEuc(i, j) + minValue;
        end
    end
    % find the shortest distance
    distDTW = DTW(size1, size2);
    % find the shortest path with backtracking
    i = size1;
    j = size2;
%     shortestPath = DTW(i, j);
    shortestPath = zeros(size1, size2);
    shortestPath(i, j) = 1;
    while i > 1 || j > 1
        adjUp = Inf; % adjacent up infinity if i = 1
        adjLeft = Inf; % adjacent left infinity if j = 1
        adjDiag = Inf; % adjacent diag infinity if i = 1 and j = 1
        if i > 1
            adjUp = DTW(i - 1, j);
        end 
        if j > 1
            adjLeft = DTW(i, j - 1);
        end
        if i > 1 && j > 1
            adjDiag = DTW(i - 1, j - 1);
        end  
        if adjUp < adjLeft
            if adjDiag <= adjUp
                i = i - 1;
                j = j - 1;
            else
                i = i - 1;
            end    
        else
            if adjDiag <= adjLeft
                i = i - 1;
                j = j - 1;
            else
                j = j - 1;
            end   
        end  
%         shortestPath = [DTW(i, j) shortestPath];
        shortestPath(i, j) = 1;
    end  
end    