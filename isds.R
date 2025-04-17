library(readxl)
library(MASS)
library(pscl)
library(AER)

regular <- function(X, y) {
  model <- glm(y ~., data=X, family='poisson')
  print(summary(model))
  print(vif(model))
  print(dispersiontest(model))
}

zeroinflated <- function(X, y) {
  model <- zeroinfl(y ~ .|., dist='poisson', data=X)
  print(summary(model))
}

df <- read_xlsx(path = "C:/CJIL/features.xlsx")
y <- unlist(df[2])
X1 = df[3:length(df)]
X2 = df[3:11]
regular(X1, y)
regular(X2, y)
zeroinflated(X1, y)
zeroinflated(X2, y)
