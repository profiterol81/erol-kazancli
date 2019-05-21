library(MASS) # linear discriminant analysis 
library(e1071)  # linear svm
library(class) # k-nn
library(rpart) # tree
library(randomForest) # random forest

train.X = read.csv('train.csv')
train.Y = read.csv('train_labels.csv')
train = train.X
train$status_group = train.Y$status_group # dependent variable: functionality status

# shuffle the data
train <- train[sample(nrow(train)),]

# Missing values:
# I am not going to use the following variables since the number of missing values are huge, 
# or the number of classes is huge, or there is only a single value, nevertheless I 
# fill the missing values with a new value, other alternative would be to take the mode since
# these are qualitative features

# train.data$funder = ifelse(is.na(train.data$funder), "NoFunder", train.data$funder)
# train.data$installer = ifelse(is.na(train.data$installer), "NoInstaller", train.data$installer)
# train.data$subvillage = ifelse(is.na(train.data$subvillage), "NoSubVillage", train.data$subvillage)
# train.data$public_meeting = ifelse(is.na(train.data$public_meeting), "NoPm", train.data$public_meeting)
# train.data$scheme_management = ifelse(is.na(train.data$scheme_management), "NoSm", train.data$scheme_management)
# train.data$permit = ifelse(is.na(train.data$permit), "NoPermit", train.data$permit)

# standardize the numerical values, amount_tsh, longitude, latitude, population, gps_height
# standardized data will be used with some models like svm
stand_train = train[,]
stand_train[ , c(2,5,7,8,18)] = scale(stand_train[ , c(2,5,7,8,18)]) 


sum_lda = 0
sum_knn = 0
sum_svm = 0
sum_tree = 0
sum_rf = 0

k = 5
split_data = dim(train)[1] / k
# k-fold cross validation
for (cv_num in 0:(k-1)){
# train_sub = sample(59400, 50000) # for random sampling 
  train_all = 1:dim(train)[1]
  test_sub = (split_data*cv_num+1):(split_data * (cv_num + 1) ) 
  train_sub = train_all[-test_sub]  
  
  test_data = train[-train_sub, ]
  
  test_std = stand_train[-train_sub, ]
  
  # linear discriminant analysis, I use standardized data
  # these features seem to have some effect on the dependent variable from several trials
  print("fitting linear discriminant classifier")
  lda.fit = lda(status_group~amount_tsh+gps_height+longitude+latitude+district_code+population+
                  extraction_type+management+payment+water_quality+
                  quantity+source+waterpoint_type, data=stand_train, subset=train_sub)
  
  lda.pred=predict(lda.fit, test_std)
  lda.class = lda.pred$class
  acc_lda = mean(lda.class == test_std$status_group)
  sum_lda = sum_lda + acc_lda
  print(paste("Lda acc, step", cv_num, ": ", acc_lda))
  print(table(lda.class, test_std$status_group)) 
  
  # linear svm, I use standardized data
  print("fitting svm classifier")
  svm.fit = svm(formula = status_group~amount_tsh+gps_height+longitude+latitude+district_code+
                   population+management+payment+water_quality+quantity+source, data=stand_train,type = 'C-classification', kernel = 'linear')
  svm.class = predict(svm.fit, newdata = test_std)
  acc_svm = mean(svm.class == test_std$status_group)
  sum_svm = sum_svm + acc_svm
  print(paste("Svm acc, step", cv_num, ": ", acc_svm))
  print(table(svm.class, test_std$status_group)) 
  
  # knn classification, the best k I found is 5 empirically 
  print("fitting knn classifier")
  train_k = as.factor(stand_train$extraction_type)
  train_k = cbind(train_k, as.factor(stand_train$payment))
  train_k = cbind(train_k, as.factor(stand_train$water_quality))
  train_k = cbind(train_k, as.factor(stand_train$quantity))
  train_k = cbind(train_k, as.factor(stand_train$source))
  train_k = cbind(train_k, as.factor(stand_train$waterpoint_type))
  train_k = cbind(train_k, as.factor(stand_train$lga))
  train_k = cbind(train_k, as.factor(stand_train$region_code))
  train_k = cbind(train_k, stand_train$amount_tsh)
  train_k = cbind(train_k, stand_train$longitude)
  train_k = cbind(train_k, stand_train$latitude)
  train_k = cbind(train_k, stand_train$gps_height)
  train_k = cbind(train_k, as.factor(stand_train$status_group))
  test_k = train_k[-train_sub, -13]
  k.class = knn(train = train_k[train_sub, -13],
              test = test_k,
              cl = train_k[train_sub, 13],
              k = 5,
              prob = TRUE, use.all = T)
  
  acc_knn = mean(k.class == train_k[-train_sub, 13])
  sum_knn = sum_knn + acc_knn
  print(paste("Knn acc, step", cv_num, ": ", acc_knn))
  
  print(table(k.class, train_k[-train_sub, 13]))
  
  # using the non standardized data for tree
  print("fitting tree classifier")
  tree.fits = rpart(status_group~amount_tsh+gps_height+longitude+latitude+population+construction_year+extraction_type+management+payment+water_quality+quantity+source+waterpoint_type, method="class", data=train, subset = train_sub)
  # tree.fits = tree(status_group~amount_tsh+gps_height+longitude+latitude+population+construction_year+extraction_type+management+payment+water_quality+quantity+source+waterpoint_type, data=train, subset = train_sub)
  tree.class=predict(tree.fits,test_data,type="class")
  acc_tree = mean(tree.class == test_data$status_group)
  sum_tree = sum_tree + acc_tree
  print(paste("Tree acc, step", cv_num, ": ", acc_tree))
  print(table(tree.class, test_data$status_group))
  
  # random forest, i tried a few mtry and ntree values, mtry= 5 and ntree=500 gave the best results
  # I use the non standardized data for random forest
  print("fitting random forest classifier")
  random.fits = randomForest(status_group~amount_tsh+gps_height+longitude+latitude+population+
                               construction_year+extraction_type+management+payment+
                               water_quality+quantity+source+waterpoint_type,
                               data=train, mtry = 5, importance=FALSE, subset = train_sub)
  random.class=predict(random.fits, test_data, type="class")
  acc_rf = mean(random.class == test_data$status_group)
  sum_rf = sum_rf + acc_rf
  print(paste("Random forest acc, step", cv_num, ": ", acc_rf))
  print(table(random.class, test_data$status_group))
}

print (paste("Avg lda accuracy: ", sum_lda / k))
print (paste("Avg knn accuracy: ", sum_knn / k))
print (paste("Avg svm accuracy: ", sum_svm / k))
print (paste("Avg tree accuracy: ", sum_tree / k))
print (paste("Avg random forest accuracy: ", sum_rf / k))








