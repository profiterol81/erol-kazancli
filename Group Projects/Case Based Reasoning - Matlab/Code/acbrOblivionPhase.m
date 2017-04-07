function [caseBase, caseClasses, goodness, newKnearest] = acbrOblivionPhase(kNearest, caseBase, caseClasses, goodness)
    k = size(kNearest, 1);
    initialGoodness = 0.5;
    newKnearest = [];
    
    sortedKnearest = sort(kNearest, 'descend');
    %if the goodness of a point among the knearest has fallen below its
    %initial value, then discard it.
    for j = 1 : k
        if (goodness(sortedKnearest(j)) < initialGoodness)
           caseBase(sortedKnearest(j), :) = [];
           caseClasses(sortedKnearest(j), :) = [];
           goodness(sortedKnearest(j), :) = [];
           % when we delete one point we need to push down the bigger
           % indices, which is newKnearest
           if size(newKnearest, 1) > 0
               newKnearest = newKnearest - 1;
           end
        else
           % this is neceassary because since we forget some points in the knearest 
           % we do not want them to be considered in the retention phase 
           newKnearest = vertcat(newKnearest, sortedKnearest(j));
        end  
    end      
    
end  