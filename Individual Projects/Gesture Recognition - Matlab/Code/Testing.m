% In this file the aligned.mat file prepared before is used and the average
% and minimum distances to training data set from the test data set is
% found. 

alignedSequencesFile = load('aligned.mat');
alignedSequences = alignedSequencesFile(1).alignedSequences;

% avgAlignedSequences = zeros(12, 150, 80);  

fileName = 'P1_1_1_p06'; % change this for a different person or for a different gesture
[X, Y] = load_file(fileName);
[gestures, nGestures] = gestureCuts(X, Y);

avgDistances = zeros(nGestures, 12);
minDistances = zeros(nGestures, 12);
% do for each sample in the test
for j = 1:nGestures
    start1 = gestures(j, 2); % start of the sequence of first gesture 
    end1 = gestures(j, 3);  % end of the sequence of first gesture 

    sequence = X(start1:end1, :);
    sequence = imresize(sequence, [150, 80]);
    sequence = translateSeq(sequence); % translate the sequence to starting position (0,0)

    % calculate the distances to each class
    for k = 1 : 12
        sequencesTr = alignedSequences{k};
        avgDist = 0;
        minDist = 1000;
        for l = 1:size(sequencesTr, 1)
            nextSeq = squeeze(sequencesTr(l, :, :));
            nextSeq = translateSeq(nextSeq); % translate the sequence to starting position (0,0)
            [dist, DTW, shortestPath] = findDistanceDTW(sequence, nextSeq);
            avgDist = avgDist + dist;
            if dist < minDist
                minDist = dist;
            end    
        end
        avgDistances(j, k) = round(avgDist/size(sequencesTr, 1));
        minDistances(j, k) = round(minDist);
    end
end 

avgDistances
minDistances