# condition grid
# classifier
c <- c("B", 
       "R", 
       "S", 
       "L", 
       "N")

# query strategy
q <- c("C" # certainty
       #"U" # uncertainty
)

# feature extraction method
f <- c("T", # tf-idf
       "D" # Doc2Vec
       #"S", # sbert 
       #"E" # embeddingIdf
) 

# balance strategy
b <- c(#"S",# simple, no reblancing 
       "D" # double (dynamic supersampling)
       #"U" # undersampling (as a bonus!)
)

conditiongrid <- tibble(condition = do.call(paste0, expand.grid(c, q, f, b)))

#conditiongrid$stage <- factor(c(rep(1:2, each = 5), rep(3,10)), labels = c("classifier", "doc2vec")) #, "AU"))
# stage 1 = all classifiers + tfidf, stage 2 is repeat with doc2vec, stage 3 is repeat with agressive undersampling. 

saveRDS(conditiongrid, file = "R/00_conditiongrid.RDS")
saveRDS(c("ace", "nudging", "ptsd", "software", "virus", "wilson"), file = "R/00_datasets.RDS")

        