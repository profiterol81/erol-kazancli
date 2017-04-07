function distance = findDistanceWithNominals(point1, point2)

    sumSquares = 0;
    numVariables = size(point1);

    for i = 1 : numVariables(2)
        val1 = point1(i);
        val2 = point2(i);
        % nominal values with NaN values
        if (val1 == -1) || (val2 == -1)  || isnan(val2) || isnan(val1) 
            diff = 1;
        % nominal values    
        elseif val1 > 1
            if val1 == val2
                diff = 0;
            else
                diff = 1;
            end
        % numeric values    
        else    
            diff = val2 - val1;
        end
        sumSquares = sumSquares + diff * diff;
    end;

    distance = sqrt(sumSquares);