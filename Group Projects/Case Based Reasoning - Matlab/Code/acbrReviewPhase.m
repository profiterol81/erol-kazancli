function updatedGoodness = acbrReviewPhase(train_classes, kNearest, estimate, goodness, learnRate)
    updatedGoodness = goodness;  
    k = size(kNearest, 1);
    for j = 1 : k
        if (train_classes(kNearest(j)) == estimate)
            reward = 1;
        else
            reward = 0;
        end
        prevGoodness = goodness(kNearest(j));
        newGoodness = prevGoodness + learnRate * (reward - prevGoodness);
        updatedGoodness(kNearest(j)) = newGoodness;  
    end    
    
end  
  