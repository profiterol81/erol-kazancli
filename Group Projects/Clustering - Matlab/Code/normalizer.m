function arr = normalizer(structData)

fields = fieldnames(structData);
data = rmfield(structData,fields);

for i = 1 : numel(fields) - 1
    
    y = structData.(fields{i});
    
    if (strcmp(structData.(fields{i}).kind, 'numeric'))
        
        maxim = max(y.values);
        minim = min(y.values);
        
        for j = 1:numel(y.values)
            
            z = y.values(j);
            data.(fields{i}).values(j) = (z - minim)/(maxim - minim);
            
        end
        
    else
        
        warning('The attribute %s is not numeric. Clustering algorithms may not work properly',fields{i});
        %TODO: normalize nominal attributes
        
    end
    
end

arr=struct_to_matrix(data)';
