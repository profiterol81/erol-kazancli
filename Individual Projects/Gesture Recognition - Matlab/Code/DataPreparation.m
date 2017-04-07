% In this file the raw data is preprocessed and stored in a matrix, and
% later in aligned.mat file.

addpath('./MicrosoftGestureDataset-RC/data');
alignedSequences = cell(12, 1);
% uncomment this commenting the line below to increase the number of gestures from different people
% persons = [19 21 22 28]; 
persons = [19];
for gest = 1 : 12
 
    sequences = zeros(100, 150, 80);
    k = 1;
    for pers = 1:size(persons, 2)
        fileName = strcat(strcat(strcat('P1_1_', num2str(gest)), '_p'), num2str(persons(pers)));
        [X, Y] = load_file(fileName);
        [gestures, nGestures] = gestureCuts(X, Y);

         for j = 1:nGestures
            start1 = gestures(j, 2); % start of the sequence of first gesture 
            end1 = gestures(j, 3);  % end of the sequence of first gesture 

            sequence = X(start1:end1, :);
            sequence = imresize(sequence, [150, 80]);
                 
            sequences(k, :, :) = sequence;
            k = k + 1;
            
         end
    end  
    sequences(k:100, :, :) = []; 
    alignedSequences{gest} = sequences;
end    

filename = 'aligned.mat';
save(filename, 'alignedSequences');

