function AllKNNForDataset( filename )
mymatfile= matfile(filename,'Writable',true);
original=mymatfile.original;
knn=cell(10,1);
for i=1:length(original)
    train=original{i}.train;
    data=train.data;
    labels=train.labels;
    classes=train.classes;
    tic;
    [newData, newClasses, samplesPerClass]=maintenanceAlgorithmAllknn(data, labels);
    knn{i}.executionTime=toc;
    fprintf(strcat('\t Execution time: ',num2str(knn{i}.executionTime),'\n'))
    fprintf(strcat('\t Number of samples: ',num2str(size(newData,1)),'\n'))
    knn{i}.data=newData;
    knn{i}.labels=newClasses;
    knn{i}.samplesPerClass=samplesPerClass;
    for j=1:length(samplesPerClass)
        fprintf(strcat('\t\t Class: ',num2str(classes(j)),'\t NumSamples: ',num2str(samplesPerClass(j)),'\n'));
    end
    
    
end
mymatfile.AllKnn=knn;

end

