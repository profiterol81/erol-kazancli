function ACBRWeightedforFilename( filename, k, retention )

accuracyReliefF = 0;
caseBaseSizeReliefF = 0;
timeReliefF = 0;
accuracyRankF = 0;
caseBaseSizeRankF = 0;
timeRankF = 0;

disp(filename);
dataset=load(filename);
original=dataset.original;

for foldNum = 1 : 10
    
    train =original{foldNum}.train;
    test =original{foldNum}.test;
            
    caseBase = train.data;
    caseClasses = train.labels;
    
    testData=test.data;
    testClasses=test.labels;
    
    if strcmp(filename, 'hypothroid')
        caseBase(:, 28) = []; % all values are null for this column in this data set
        testData(:, 28) = []; % so deleted here for this data set, otherwise relieff does not work
    end    

    tic;
    [testEstimatesReliefF, caseBaseReliefF, ~, ~] = weightedACBRAlgorithm(caseBase, caseClasses, testData, k,  retention, 'relieff');
    timeReliefF = timeReliefF + toc;
    accuracyReliefF = accuracyReliefF + sum(testClasses == testEstimatesReliefF) / size(testData, 1);
    caseBaseSizeReliefF = caseBaseSizeReliefF + size(caseBaseReliefF, 1);

    tic;
    [testEstimatesRankF, caseBaseRankF, ~, ~] = weightedACBRAlgorithm(caseBase, caseClasses, testData, k,  retention, 'correlation');
    timeRankF = timeRankF + toc;
    accuracyRankF = accuracyRankF + sum(testClasses == testEstimatesRankF) / size(testData, 1);
    caseBaseSizeRankF = caseBaseSizeRankF + size(caseBaseRankF, 1);
    
end

accuracyReliefF = accuracyReliefF / 10;
caseBaseSizeReliefF = caseBaseSizeReliefF / 10;
timeReliefF = timeReliefF / 10;

accuracyRankF = accuracyRankF / 10;
caseBaseSizeRankF = caseBaseSizeRankF / 10;
timeRankF = timeRankF / 10;

disp(strcat('Accuracy DDO with Correlation Based FS:', num2str(accuracyRankF)));
disp(strcat('Accuracy DDO with ReliefF FS:', num2str(accuracyReliefF)));

disp(strcat('Execution Time DDO with Correlation Based FS:', num2str(timeRankF)));
disp(strcat('Execution Time DDO with ReliefF FS:', num2str(timeReliefF)));

disp(strcat('Case base DDO with Correlation Based FS:', num2str(caseBaseSizeRankF)));
disp(strcat('Case base DDO with ReliefF FS:', num2str(caseBaseSizeReliefF)));

end