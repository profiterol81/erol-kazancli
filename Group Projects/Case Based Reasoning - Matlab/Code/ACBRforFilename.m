function ACBRforFilename( filename )
%ACBRFORFILENAME Summary of this function goes here
%   Detailed explanation goes here
disp(filename);
dataset=load(filename);
policy = {'DD', 'MG', 'AR', 'NR', 'DDO', 'MGO', 'ARO', 'NRO'};
accuracy = zeros(3,8); % k = 3, 5, 7 and for 8 policies
caseBaseSize = zeros(3, 8); % k = 3, 5, 7 and for 8 policies
executionTime = zeros(3, 8); % k = 3, 5, 7 and for 8 policies
ks = [3, 5, 7];
original=dataset.original;
% for each fold
for foldNum = 1 : 10
    
    train =original{foldNum}.train;
    test =original{foldNum}.test;
        
    caseBase = train.data;
    caseClasses = train.labels;
    
    testData=test.data;
    testClasses=test.labels;
    % for each k
    for i = 1 : size(ks, 2)
        k = ks(i);

        for polNum = 1 : size(policy, 2)
            tic
            [testEstimates, newCaseBase, ~, ~] = acbrAlgorithm(caseBase, caseClasses, testData, k, policy(polNum));
            time = toc;
            acc = sum(testClasses == testEstimates) / size(testData, 1);
            cbSize = size(newCaseBase, 1); 
            % for i'th k and pol'th policy, we add the numbers for 10-fold, later to divide by 10 
            accuracy(i, polNum) = accuracy(i, polNum) + acc;
            executionTime(i, polNum) = executionTime(i, polNum) + time;
            caseBaseSize(i, polNum) = caseBaseSize(i, polNum) + cbSize;
        end
    end
end

% the averages of 10 terations are taken
accuracy = accuracy / 10;
executionTime = executionTime / 10;
caseBaseSize = caseBaseSize / 10;

disp('Accuracies');
disp(accuracy);
disp('Execution Times');
disp(executionTime);
disp('Case base sizes');
disp(caseBaseSize);

end

