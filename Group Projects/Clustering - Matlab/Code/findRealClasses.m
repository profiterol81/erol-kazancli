function [real_class_indexes] = findRealClasses(true_indexes, indexes, numGroups)
    
    dataSize = size(indexes, 1);
    real_class_indexes = zeros(dataSize, 1);
    
    temp = indexes;
    for i=1 : numGroups
        [row, col, a] = find(temp(true_indexes==i));
        j=mode(a);
        temp(temp==j) = 0;
        real_class_indexes(indexes==j) = i;   
    end
    
end