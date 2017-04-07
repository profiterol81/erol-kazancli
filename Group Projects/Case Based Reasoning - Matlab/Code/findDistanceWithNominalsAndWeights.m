function distance = findDistanceWithNominalsAndWeights(point1, point2, weight)

    sumSquares = 0;
    numVariables = size(point1);

    for i = 1 : numVariables(2)
        
        if weight(i) == 1 % if weight is zero the attribute is not taken into account
        
            val1 = point1(i);
            val2 = point2(i);
            % nominal values with NaN values
            if (val1 == -1) || (val2 == -1)
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
            
        end
    end;

    distance = sqrt(sumSquares);