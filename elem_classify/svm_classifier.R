library("e1071")

# Attach the Data

attach(iris)

# Divide Iris data to x (containt the all features) and y only the classes

x <- subset(iris, select=-Species)
y <- Species

svm_model <- svm(Species ~ ., data=iris, kernel="radial", cost=1, gamma=0.5)


write.svm(svm_model, "file.svm", "file.scale")
