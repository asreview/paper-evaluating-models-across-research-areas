conditiongrid <- readRDS("R/00_conditiongrid.RDS")

# stage - which trials to take? (1, 2, 3)
#st <- c("classifier", "doc2vec")

# only select conditions from stage. 
# conditiongrid <- 
#   conditiongrid %>% 
#   filter(stage %in% st)

# datasets (D)
D <- readRDS("R/00_datasets.RDS")

# add datsets? 
conditiongrid %>% add_column(ace = 0L,
                             nudging = 0L,
                             ptsd = 0L,
                             software = 0L,
                             wilson = 0L) 

# optimize hyperparameters (11 sets (1+2*5)) 
opt <- c("one", "four", "all")

# 300 sets of hyperparameters in total 
# 75 for stage 1
# hyperparametersets <- expand.grid(model = conditiongrid$condition, hyperopt = opt) 
# hyperparametersets <- hyperparametersets %>% 
#   add_column(ace = 0L,
#              nudging = 0L,
#              ptsd = 0L,
#              software = 0L,
#              wilson = 0L)
# save 
#saveRDS(hyperparametersets, file = "R/01_hyperparameter_sets.RDS")

dims <- list(condition = conditiongrid$condition, data = D, hyper = opt)

# 3d array to track hyperparameter optimization
hpsets <- 
  array(0, 
       dim = c(length(conditiongrid$condition), length(D), length(opt)), 
       dimnames = dims)

saveRDS(hpsets, file = "R/01_hyperparameter_sets.RDS")
