function [ error ] = error_rate( labels,my_labels )

error=size(labels(labels~=my_labels),1)/size(labels,1);
end

