function [weights] = polynomial_model(x, y, power)
    
    %turn into augmented x with the powered values 
    polyX = [ones(length(x),1)];
    for i = 1 : power  
        polyX = [polyX polyX(:, i).*x];
    end
    
    weights = inv(transpose(polyX)*polyX) * (transpose(polyX))*y;
      
end    