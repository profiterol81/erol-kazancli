function MaintainedACBRforFilename( filename, k, protocol1, protocol2)

disp(filename);
dataset=load(filename);
allKnn=dataset.AllKnn;
ib2=dataset.IB2;
original=dataset.original;

accuracyIB2 = 0;
caseBaseSizeIB2 = 0;
timeIB2 = 0;
accuracyAllknn = 0;
caseBaseSizeAllknn = 0;
timeAllknn = 0;
accuracyAllknnDDO = 0;
caseBaseSizeAllknnDDO = 0;
timeAllknnDDO = 0;
accuracyIb2DDO = 0;
caseBaseSizeIb2DDO = 0;
timeIb2DDO = 0;

% for each fold
for foldNum = 1 : 10
    
    trainKnn =allKnn{foldNum};
    trainIB2 =ib2{foldNum};
    test =original{foldNum}.test;
        
    knnCaseBase = trainKnn.data;
    knnCaseClasses = trainKnn.labels;
    
    ib2CaseBase = trainIB2.data;
    ib2CaseClasses = trainIB2.labels;
    
    testData=test.data;
    testClasses=test.labels;
    tic;
    [testEstimatesAllknn, caseBaseAllknnNew, ~, ~] = acbrAlgorithm(knnCaseBase, knnCaseClasses, testData, k,  protocol1);
    timeAllknn =timeAllknn+ toc;
    accuracyAllknn = accuracyAllknn + sum(testClasses == testEstimatesAllknn) / size(testData, 1);
    caseBaseSizeAllknn = caseBaseSizeAllknn + size(caseBaseAllknnNew, 1);    
    
    
    tic;
    [testEstimatesIB2, caseBaseIB2New, ~, ~] = acbrAlgorithm(ib2CaseBase, ib2CaseClasses, testData, k,  protocol1);
    timeIB2 = timeIB2 + toc;
    accuracyIB2 = accuracyIB2 + sum(testClasses == testEstimatesIB2) / size(testData, 1);
    caseBaseSizeIB2 = caseBaseSizeIB2 + size(caseBaseIB2New, 1);
    
    tic;
    [testEstimatesAllknnDDO, caseBaseAllknnDDO, ~, ~] = acbrAlgorithm(knnCaseBase, knnCaseClasses, testData, k,  protocol2);
    timeAllknnDDO = timeAllknnDDO + toc;
    accuracyAllknnDDO = accuracyAllknnDDO + sum(testClasses == testEstimatesAllknnDDO) / size(testData, 1);
    caseBaseSizeAllknnDDO = caseBaseSizeAllknnDDO + size(caseBaseAllknnDDO, 1);
    
    
    tic;
    [testEstimatesIb2DDO, caseBaseIb2DDO, ~, ~] = acbrAlgorithm(ib2CaseBase, ib2CaseClasses, testData, k,  protocol2);
    timeIb2DDO = timeIb2DDO + toc;
    accuracyIb2DDO = accuracyIb2DDO + sum(testClasses == testEstimatesIb2DDO) / size(testData, 1);
    caseBaseSizeIb2DDO = caseBaseSizeIb2DDO + size(caseBaseIb2DDO, 1);
    
    
end

accuracyIB2 = accuracyIB2 / 10;
caseBaseSizeIB2 = caseBaseSizeIB2 / 10;
timeIB2 = timeIB2 / 10;

accuracyAllknnDDO = accuracyAllknnDDO / 10;
caseBaseSizeAllknnDDO = caseBaseSizeAllknnDDO / 10;
timeAllknnDDO = timeAllknnDDO / 10;

accuracyAllknn = accuracyAllknn / 10;
caseBaseSizeAllknn = caseBaseSizeAllknn / 10;
timeAllknn = timeAllknn / 10;

accuracyIb2DDO=accuracyIb2DDO / 10;
caseBaseSizeIb2DDO=caseBaseSizeIb2DDO/10;
timeIb2DDO = timeIb2DDO / 10;


disp(strcat('Accuracy IB2:',protocol1,':', num2str(accuracyIB2)));
disp(strcat('Accuracy Allknn:',protocol1,':', num2str(accuracyAllknn)));
disp(strcat('Accuracy All KNN ',protocol2,':', num2str(accuracyAllknnDDO)));
disp(strcat('Accuracy IB2 ',protocol2,':', num2str(accuracyIb2DDO)));

disp(strcat('Execution Time IB2 ',protocol1,':',protocol1,':', num2str(timeIB2)));
disp(strcat('Execution Time Allknn ',protocol1,':', num2str(timeAllknn)));
disp(strcat('Execution Time All KNN ',protocol2,':', num2str(timeAllknnDDO)));
disp(strcat('Execution Time IB2 with ',protocol2,':', num2str(timeIb2DDO)));

disp(strcat('Case base IB2 ',protocol1,':', num2str(caseBaseSizeIB2)));
disp(strcat('Case base Allknn ',protocol1,':', num2str(caseBaseSizeAllknn)));
disp(strcat('Case base All KNN ',protocol2,':', num2str(caseBaseSizeAllknnDDO)));
disp(strcat('Case base IB2 with ',protocol2,':', num2str(caseBaseSizeIb2DDO)));

end

