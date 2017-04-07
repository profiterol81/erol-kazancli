function estimate = acbrReusePhase(baseClasses, kNearest)
     C = zeros(2, 1);
     k = size(kNearest, 1);
     % if more than 1 majority votes repeat decreasing k
     while size(C, 1) > 1
         kNearest = kNearest(1:k, :); 
         [estimate, ~, C2] = mode(baseClasses(kNearest));
         C = cell2mat(C2);
         k = k - 1; % if more than one majority votes decrease k
     end
end  
  