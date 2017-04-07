function [caseBase, caseClasses, samplesPerClass] = maintenanceAlgorithmAllknn(caseBase, caseClasses)

dataSize = size(caseBase, 1);

% find distances between data points and put them in an array
distances = zeros(dataSize, dataSize);
for i = 1 : dataSize
    for j = i : dataSize
        dist = findDistanceWithNominals(caseBase(i, :), caseBase(j, :));
        distances(i, j) = dist;
        distances(j, i) = dist;
    end
end

flaggedIndexes = zeros(dataSize, 1);
for k = 1 : 6
    % flaggedIndexes are accumulated by each round of k
    [flaggedIndexes] = ENN(caseBase, caseClasses, distances, k, flaggedIndexes);
end
% flaggedIndexes = 1 are deleted
caseBase = caseBase(flaggedIndexes == 0, :);
caseClasses = caseClasses(flaggedIndexes == 0, :);
uClasses=unique(caseClasses);
samplesPerClass=zeros(1,length(uClasses));
for i=1:length(uClasses)
    samplesPerClass(i)=length(caseClasses(caseClasses==uClasses(i)));
end

end
