function translatedSeq = translateSeq(sequence)
    first = sequence(1, :);
    
    for i = 1: size(sequence, 1)
        sequence(i, :) = sequence(i, :) - first;  
    end    

    translatedSeq = sequence;
end