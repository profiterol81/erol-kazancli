library(MASS) # linear discriminant analysis 
library(e1071)  # linear svm
# library(class) # k-nn
# library(rpart) # tree
library(randomForest) # random forest

# read data
flights = read.csv('data/flights.csv', sep = ";")
airlines = read.csv('data/airlines.csv', sep = ";")
airports = read.csv('data/airports.csv', sep = ";")
planes = read.csv('data/planes.csv', sep = ";")
weather = read.csv('data/weather.csv', sep = ";")

# left merge 
merged = merge(x = flights, y = airlines, by = "carrier", all.x = TRUE)

# flight numbers based on the hour of the day
c_hourly = aggregate(flights$year, by=list(hour = flights$hour), FUN=length)
plot(c_hourly$hour, c_hourly$x)

# flight numbers based on the day of the month
c_daily = aggregate(flights$year, by=list(day = flights$day), FUN=length)
plot(c_daily$day, c_daily$x)

# flight numbers based on the month
c_monthly = aggregate(flights$year, by=list(month = flights$month), FUN=length)
plot(c_monthly$month, c_monthly$x)

# flight numbers based on carrier
c_carrier = aggregate(flights$year, by=list(carrier = flights$carrier), FUN=length)
newdata <- c_carrier[order(-c_carrier$x),] 

# flight numbers based on origin
c_origin = aggregate(flights$year, by=list(origin = flights$origin), FUN=length)
newdata <- c_origin[order(-c_origin$x),] 

# flight numbers based on destination
c_dest = aggregate(flights$year, by=list(origin = flights$dest), FUN=length)
newdata <- c_dest[order(-c_dest$x),] 

# bar plot flight number per carrier
c_carrier <- table(flights$carrier)
barplot(c_carrier, main="Flight Distribution with Carrier", 
        xlab="Number of Flights")

# bar plot flight number per origin
c_origin <- table(flights$origin)
barplot(c_origin, main="Flight Distribution with Origin", 
        xlab="Number of Flights")

# bar plot flight number per destination
c_dest <- table(flights$dest)
barplot(c_dest, main="Flight Distribution with Destination", 
        xlab="Number of Flights")

# summarise data
summary(flights)

# flight number per origin and time 
c_origin_time = aggregate(flights$year, by=list(origin = flights$origin, time_hour=flights$time_hour), FUN=length)

# merge with the weather data
merged = merge(x = c_origin_time, y = weather, by = c("origin","time_hour"))

# linear regression - month and hour could have been left numerical but the result 
# is quite poor in that case 
merged$month = as.factor(merged$month)
merged$hour = as.factor(merged$hour)
linear_model = lm(x ~ origin + month + hour + temp + dewp + humid + wind_dir 
                  + wind_speed + wind_gust + precip + pressure + visib, data=merged)
summary(linear_model)

# dicretization starts
flights_over_zero = subset(flights, dep_delay > 0)
flights_under_equal_zero = subset(flights, dep_delay <= 0)
flights_null = subset(flights, is.na(dep_delay))

ApplyDeciles <- function(x) {
  cut(x, breaks=c(quantile(flights_over_zero$dep_delay, probs = seq(0, 1, by = 0.10))), 
      labels=c("0-10","10-20","20-30","30-40","40-50","50-60","60-70","70-80","80-90","90-100"
      ), include.lowest=TRUE)
}
flights_over_zero$dep_delay_cat <- sapply(flights_over_zero$dep_delay, ApplyDeciles)
flights_under_equal_zero$dep_delay_cat <- "under_zero"
flights_null$dep_delay_cat <- "null_value"

flights_all = rbind(flights_over_zero, flights_under_equal_zero, flights_null)

# aa = subset(flights_all, day > 0)
# aa = sum(is.na(merged$dep_delay_cat))

merged = merge(x = flights_all, y = weather, by = c("origin","time_hour"))

size_f = nrow(flights_all)
trainIndex = sample(1:size_f, size = round(0.8*size_f), replace=FALSE)

merged$month = as.factor(merged$month)
merged$hour = as.factor(merged$hour)
# fit random forest classifier
random.fits = randomForest(dep_delay_cat ~ origin + month.x + hour.x + temp + dewp + humid + wind_dir 
                           + wind_speed + wind_gust + precip + pressure + visib,
                           data=merged, mtry = 5, importance=TRUE, subset = trainIndex,na.action=na.roughfix)
random.class = predict(random.fits,merged[trainIndex, ], type="class") 

# training accuracy
acc_rf = mean(random.class == merged[trainIndex,]$dep_delay_cat, na.rm = TRUE) # accuracy of the training
random.test = predict(random.fits,merged[-trainIndex, ], type="class")
# test accuracy
acc_rf_test = mean(random.test == merged[-trainIndex,]$dep_delay_cat, na.rm = TRUE) 

# fit svm classifier 
# svm.fit = svm(formula = dep_delay_cat ~ origin + month.x + hour.x + temp + dewp + humid 
#              + wind_dir + wind_speed + wind_gust + precip + pressure + visib,
#              data=merged, subset = trainIndex, type = 'C-classification', kernel = 'linear')
# svm.class = predict(svm.fit, newdata = merged[trainIndex,])
# summary(svm.class)
# acc_svm = mean(svm.class == merged[trainIndex,]$dep_delay_cat)

# fit lda classifier
lda.fit = lda(formula = dep_delay_cat ~ origin + month.x + hour.x + temp + dewp + 
                humid+ wind_dir + wind_speed + wind_gust + precip + pressure + visib, data=merged, subset=trainIndex)

lda.pred=predict(lda.fit, merged[trainIndex,])
lda.class = lda.pred$class
acc_lda = mean(lda.class == merged[trainIndex,]$dep_delay_cat, na.rm = TRUE)

ldatest.pred=predict(lda.fit, merged[-trainIndex,])
ldatest.class = ldatest.pred$class
acc_lda_test = mean(ldatest.class == merged[-trainIndex,]$dep_delay_cat, na.rm = TRUE)
