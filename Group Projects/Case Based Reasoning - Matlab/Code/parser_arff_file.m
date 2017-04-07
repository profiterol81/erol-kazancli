function [data, classes] = parser_arff_file(filename)
    unnormalized=arffparser(filename);
    data=normalizer(unnormalized);
    % some NaN values are set to zero, but another method may be considered
    data(isnan(data)) = 0;

    numGroups=size(unnormalized.class.kind, 2);
    classes=zeros(size(data, 1),1);

    % find true classes for training
    for i = 1 : numGroups
        if iscell(unnormalized.class.kind)
            class=unnormalized.class.kind{i};
            classes(strcmp(unnormalized.class.values,class))=i;
        else
            class=unnormalized.class.kind(i);
            classes(unnormalized.class.values == class)=i;
        end    
    end

end  