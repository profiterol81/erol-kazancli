function  IB2ForDataset( filename )
mymatfile= matfile(filename,'Writable',true);
original=mymatfile.original;
ib2=cell(10,1);
for i=1:length(original)
    train=original{i}.train;
    data=train.data;
    labels=train.labels;
    classes=train.classes;
    tic;
    [newData, newClasses, samplesPerClass]=MaintenanceAlgorithmIB2(data, labels);
    ib2{i}.executionTime=toc;
    fprintf(strcat('\t Execution time: ',num2str(ib2{i}.executionTime),'\n'))
    fprintf(strcat('\t Number of samples: ',num2str(size(newData,1)),'\n'))
    ib2{i}.data=newData;
    ib2{i}.labels=newClasses;
    ib2{i}.samplesPerClass=samplesPerClass;
    for j=1:length(classes)
        fprintf(strcat('\t\t Class: ',num2str(classes(j)),'\t NumSamples: ',num2str(samplesPerClass(j)),'\n'));
    end
end
mymatfile.IB2=ib2;

end

