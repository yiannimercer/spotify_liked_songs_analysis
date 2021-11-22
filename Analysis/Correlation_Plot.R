library(tidyverse)

library(ggplot2)

library(ggcorrplot)

install.packages("ggcorrplot")

df <- read.csv("spotify_liked_final_df.csv")

df <- df %>%
  select(-X) %>%
  select_if(is.numeric)

corr <- cor(df)

ggcorrplot(corr,type = 'lower',lab = TRUE,title = "Pearson Correlation of Audio Features (Focusing on Liked variable)")
