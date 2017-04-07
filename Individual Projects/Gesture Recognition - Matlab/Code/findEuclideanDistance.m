function dist = findEuclideanDistance(coor1, coor2)
    size1 = size(coor1, 2);
    dist = 0;
    for i=1:size1
        diff = coor2(1, i) - coor1(1, i);
        dist = dist + diff * diff;
    end    
    dist = sqrt(dist);
end
