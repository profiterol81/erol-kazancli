function matrix = struct_to_matrix( data )
%STRUCT_TO_MATRIX Summary of this function goes here
%   Detailed explanation goes here
fields = fieldnames(data);
    n=numel(fields);
    [m1,m]=size(data.(fields{1}).values);
    matrix=zeros(n,m);
    for i = 1 : numel(fields)
    
        y = data.(fields{i});
    
            for j = 1:numel(y.values)
            
                matrix(i,j) = y.values(j);
               % data_wo_mean.(fields{i}).values(j) = z-avg;
            end
    end

end

