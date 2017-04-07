function [arr, results] = normalizer(structData)

fields = fieldnames(structData);
data = rmfield(structData,fields);

for i = 1 : numel(fields) - 1
    
    y = structData.(fields{i});
    
    if (strcmp(structData.(fields{i}).kind, 'numeric') | strcmp(structData.(fields{i}).kind, 'REAL'))
        
        maxim = max(y.values);
        minim = min(y.values);
        
        % we replace NaN values with the mean of that attribute
        dim = y.values;
        meanDim = nanmean(dim); % mean of dimension i excluding NaNs 
        dim(isnan(dim)) = meanDim; % replace NaN values with the mean
        y.values = dim;
        
        for j = 1:numel(y.values)
            
            z = y.values(j);   
            data.(fields{i}).values(j) = (z - minim)/(maxim - minim);
            
        end
        
    else
        %for nominal values integers greater than one are used. If the
        %value is Nan, the value -1 is assigned. 
        kind = structData.(fields{i}).kind;
        for j = 1:numel(y.values)
            z = y.values(j);
            if strcmp(z{1}, ('NaN'))
                data.(fields{i}).values(j) = -1;
            else    
                data.(fields{i}).values(j) = 1 + find(ismember(kind, z)); 
            end
        end
    end
    
end

results=structData.(fields{numel(fields)}).values;
arr=struct_to_matrix(data)';
