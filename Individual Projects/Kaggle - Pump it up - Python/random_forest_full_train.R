library(randomForest) # random forest
test.X = read.csv('test.csv')

train.X = read.csv('train.csv')
train.Y = read.csv('train_labels.csv')
train = train.X 
train$status_group = train.Y$status_group # dependent variable: functionality status

total = rbind(train.X, test.X) # necessary to have them together because of the factors
                               # and split theme during training
labels_train = as.character(train.Y$status_group) 
labels_test = rep("functional", nrow(test.X))
labels = as.factor(c(labels_train, labels_test))
total$status_group = labels
train_sub = 1:nrow(train.X)
test_sub = (nrow(train.X) + 1):nrow(total)

# random forest training with all training data
random.fits = randomForest(status_group~amount_tsh+gps_height+longitude+latitude+population+
                             construction_year+extraction_type+management+payment+
                             water_quality+quantity+source+waterpoint_type,
                           data=total, mtry = 5, importance=FALSE, subset = train_sub)
acc_rf = mean(random.cl == total[train_sub,]$status_group) # accuracy of the training

# prediction of the test
random.class=predict(random.fits,total[test_sub, ], type="class") 
test.X$status_group = random.class
pred = test.X[, c(1,41)]
write.csv(pred[, c(1,2)], "pred.csv", row.names=FALSE)
