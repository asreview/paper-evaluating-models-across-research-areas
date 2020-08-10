
# set emojis for grid 
check <- function(todo, m, ho, d){
  todo[todo$model %in% m & todo$hyperopt == ho, d] <- emo::ji("check") 
  return(todo)
}

busy <- function(todo, m, ho, d){
  todo[todo$model %in% m & todo$hyperopt == ho, d] <- emo::ji("timer") 
  return(todo)
}

huh <- function(todo, m, ho, d){
  todo[todo$model %in% m & todo$hyperopt == ho, d] <- emo::ji("question") 
  return(todo)
}

not <- function(todo, m, ho, d){
  todo[todo$model %in% m & todo$hyperopt == ho, d] <- emo::ji("x") 
  return(todo)
}

check <- function(x){switch(x, 
       "0" = emo::ji("white square button") , 
       "1" = emo::ji("timer"), 
       "2" = emo::ji("check"), 
       "8" = emo::ji("huh"), 
       "9" = emo::ji("x"))
}
# 0 =  todo
# 1 = busy
# 2 = done
# 8 = not going to do 
# 9 = problems
 
# apply(hpsets[,1,1], check)
# 
# check(hpsets[1,1,1])
# 
# sapply(hpsets, check, FUN.VALUE = hpsets)
