function distance = findDistance(point1, point2)

    sumSquares = 0;
    numVariables = size(point1);

    for i = 1 : numVariables(2)
        
        val1 = point1(i);
        val2 = point2(i);
        diff = val2 - val1;
        sumSquares = sumSquares + diff * diff;
    
    end;

    distance = sqrt(sumSquares);