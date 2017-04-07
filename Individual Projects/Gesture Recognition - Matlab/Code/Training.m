% In this file the aligned.mat file prepared before is used and the maximum and 
% average distances for each gesture is found. 

avgAlignedSequencesFile = load('aligned.mat');
alignedSequences = avgAlignedSequencesFile(1).alignedSequences;

maxDistances = zeros(12, 1);
avgDistances = zeros(12, 1);

maxDist = 0;
for i = 1:12
    sequences = alignedSequences{i};
    maxDist = 0;
    avg = 0;
    count = 0;
    for j = 1: size(sequences, 1)
        sequence1 = squeeze(sequences(j, :, :));
        for k = j+1:size(sequences, 1)
            sequence2 = squeeze(sequences(k, :, :));
            [dist, DTW, shortestPath] = findDistanceDTW(sequence1, sequence2);
           
            avg = avg + dist;
            count = count + 1;
            if dist > maxDist
                maxDist = dist;
            end 
        end    
    end 
    
    maxDistances(i) = maxDist;
    avgDistances(i) = avg / count;
end
 
maxDistances
avgDistances
