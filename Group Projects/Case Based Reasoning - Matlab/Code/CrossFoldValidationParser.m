function CrossFoldValidationParser( datasetname )
fprintf(strcat('\t ',datasetname,'\n'))
dataset=cell(1,10);
for k=0:9
    disp(strcat('train',num2str(k)));
    [trainData, trainClasses] = parser_arff_file(strcat('datasetsCBR/',datasetname,'/',datasetname,'.fold.00000',num2str(k),'.train.arff'));
    fprintf(strcat('\t Number of samples: ',num2str(size(trainData,1)),'\n'))
    fprintf(strcat('\t Number of features per sample: ',num2str(size(trainData,2)),'\n'));
    uClasses=unique(trainClasses);
    fprintf(strcat('\t Number of classes: ',num2str(length(uClasses)),'\n'))
    trainSamplesPerClass=zeros(1,length(uClasses));
    for i=1:length(uClasses)
        trainSamplesPerClass(i)=length(trainClasses(trainClasses==uClasses(i),:));
        fprintf(strcat('\t\t Class: ',num2str(uClasses(i)),'\t NumSamples: ',num2str(trainSamplesPerClass(i)),'\n'));
        
    end
    train.data=trainData;
    train.labels=trainClasses;
    train.classes=uClasses;
    train.samplesPerClass=trainSamplesPerClass;
    dataset{k+1}.train=train;
    disp(strcat('test',num2str(k)));
    
    [testData, testClasses] = parser_arff_file(strcat('datasetsCBR/',datasetname,'/',datasetname,'.fold.00000',num2str(k),'.test.arff'));
    fprintf(strcat('\t Number of samples: ',num2str(size(testData,1)),'\n'))
    fprintf(strcat('\t Number of features per sample: ',num2str(size(testData,2)),'\n'));
    uClasses=unique(testClasses);
    fprintf(strcat('\t Number of classes: ',num2str(length(uClasses)),'\n'))
    testSamplesPerClass=zeros(1,length(uClasses));
    for i=1:length(uClasses)
        testSamplesPerClass(i)=length(testClasses(testClasses==uClasses(i),:));
        fprintf(strcat('\t\t Class: ',num2str(uClasses(i)),'\t NumSamples: ',num2str(testSamplesPerClass(i)),'\n'));
        
    end
    test.data=testData;
    test.labels=testClasses;
    test.classes=uClasses;
    test.samplesPerClass=testSamplesPerClass;
    dataset{k+1}.test=test;
    
end
filename=strcat(datasetname,'Set.mat');
file= matfile(filename,'Writable',true);
file.original=dataset;

end

